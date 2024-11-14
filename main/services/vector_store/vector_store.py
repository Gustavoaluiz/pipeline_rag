import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(BASE_DIR)

import faiss
from pandas import DataFrame
import numpy as np
from typing import Tuple
from numpy import ndarray
from main.services.encoder.embedding import Embedding
from main.services.chunker.chunker_hashes import ChunksHashes

class VectorStoreFaissAdaper:

    def __init__(
            self, 
            encoder: Embedding, 
            embedding_dim: int,
            index_path: str = None,
            index_type: str = 'flat', 
    ):
        if index_path:
            self.index_path = index_path
        else:
            self.index_path = os.path.join(BASE_DIR, 'data', 'vectorstore')

        self.encoder = encoder
        self.vector_store = None
        self.index_type = index_type
        self.index_file = os.path.join(self.index_path, 'index.faiss')
    
        if os.path.exists(self.index_file):
            self.index = self._read_index()
        else:
            self.index = self._create_index(embedding_dim)

    def _create_index(self, embedding_dim: int):
        os.makedirs(self.index_path, exist_ok=True)

        if self.index_type == 'flat':
            return faiss.IndexFlatIP(embedding_dim)
        else:
            raise ValueError(f"Unknown index type: {self.index_type}")
        
    def _read_index(self):
        return faiss.read_index(self.index_file)
        
    def _save_index(self):
        faiss.write_index(self.index, self.index_file)

    def add_documents(self, chunks: DataFrame):
        chunks = ChunksHashes().get_deduplicated_chunks(chunks=chunks)
        chunks = chunks.iloc[:, 0].tolist()
        
        if not chunks:
            print('No new chunks to add.')
            return
        
        embeddings = self.encoder.embed_documents(chunks)
        # Garantir que os dados sejam armazenados de forma contígua
        # na memória
        embeddings = np.ascontiguousarray(embeddings)
        faiss.normalize_L2(embeddings)

        if not self.index.is_trained:
            self.index.train(embeddings)

        self.index.add(embeddings)
        self._save_index()

    def search(self, query_text: str, k: int = 5) -> Tuple[ndarray, ndarray]:
        query_embedding = self.encoder.embed_query(query_text)
        query_embedding = query_embedding.reshape(1, -1)
        distances, indexes = self.index.search(query_embedding, k)

        return distances, indexes
    
    def get_chunks(self, indexes: ndarray, chunks: DataFrame) -> DataFrame:
        return chunks.iloc[indexes[0], :]
        