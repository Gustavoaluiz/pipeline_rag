import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(BASE_DIR)

from main.services.decoder.llm_port import LLMPort
from main.services.encoder.embedding_port import EmbeddingPort
from typing import List
from typing import List
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document
from pandas import DataFrame


class Chunker:
    def __init__(
            self, 
            chunks_path: str = None
    ):
        if chunks_path:
            self.chunks_path = chunks_path
        else:
            self.chunks_path = os.path.join(BASE_DIR, 'data', 'chunk')
            
        self.text_splitter = None
        self.chunks_file = os.path.join(self.chunks_path, 'chunks.csv')

    def get_splitter(
            self, 
            separators: List[str] = None,
            chunk_size: int = 256, 
            chunk_overlap: int = 38
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def _update_chunks(self, dataset: pd.DataFrame):
        os.makedirs(self.chunks_path, exist_ok=True)

        if os.path.exists(self.chunks_file):
            chunks = pd.read_csv(self.chunks_file, index_col=0)
            chunks = pd.concat([chunks, dataset], axis=0)
            chunks.drop_duplicates(inplace=True, keep='first')
        else:
            chunks = dataset

        chunks = chunks.reset_index().rename(columns={'index': 'index'})
        chunks.to_csv(self.chunks_file, index=False)

    @staticmethod
    def _enrich_with_metadata(doc: Document) -> str:
        """Adiciona os metadados a cada chunk gerado"""
        text = ''
        for key, value in doc.metadata.items():
            text += f"{key.upper()}: {value}\n"
        text += doc.page_content

        return text

    def _create_chunks(self, dataframe: DataFrame) -> List[Document]:
        nivels = [f"nivel_{n}" for n in range(1, 6)]
        documents = []

        for _, row in dataframe.iterrows():
            # Dicionário para armazenar as informações hierárquicas 
            metadados = {"descricao_categoria": row["descricao_categoria"]}
            for nivel in nivels:
                value = row.get(nivel)
                # Se o nível hierárquico não for nulo, adiciona aos metadados
                if not isinstance(value, float):
                    metadados[nivel] = value

            # Divide o texto em chunks
            split_texts = self.text_splitter.split_text(row['conteudo'])
            
            # Adiciona os metadados a cada chunk gerado
            for chunk in split_texts:
                documents.append(Document(page_content=chunk, metadata=metadados))
        
        return documents


    def chunk(self, dataset: pd.DataFrame) -> pd.DataFrame:
        documents: List[Document] = self._create_chunks(dataset)

        # Tranforma os objetos Document em strings, contendo os metadados
        chunks: List[str] = [self._enrich_with_metadata(doc) for doc in documents]

        chunks = pd.DataFrame(chunks, columns=['nivels_e_conteudo'])
        
        self._update_chunks(chunks)

        return chunks
