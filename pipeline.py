import os
from main.domain.load_type import LoadDataType
from main.domain.embedding_type import EmbeddingType
from main.services.load_data.data_load_factory import DataLoadFactory
from main.services.chunker.chunker import Chunker
from main.services.encoder.hf_adapter import EmbeddingHuggingFace
from main.services.encoder.embedding_factory import EmbeddingFactory
from main.services.vector_store.vector_store import VectorStoreFaissAdaper
from main.services.decoder.llm_factory import LLMFactory
from main.domain.llm_type import LLMType
from main.services.decoder.prompt import PromptTemplate
from typing import List, Dict
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


dataset = DataLoadFactory().get_dataset(
    load_type=LoadDataType.LOCAL,
    path=os.path.join('crawler', 'output', 'GIAS_Portuguese_IIA.csv')
)

chunker = Chunker()
chunker.get_splitter(
    separators=["\n\n", "."],
    chunk_size=1000,
    chunk_overlap=150,
)
chunks = chunker.chunk(dataset)

encoder = EmbeddingFactory().get_embedding_adapter(
    embedding_type=EmbeddingType.VERTEX_AI,
    model_name="text-multilingual-embedding-002",
)
vector_store = VectorStoreFaissAdaper(
    encoder=encoder,
)

decoder = LLMFactory().get_llm_adapter(LLMType.GEMINI, "gemini-1.5-flash")

vector_store.add_documents(chunks)

query = \
"""
Quais são as implicações de um auditor interno aceitar presentes ou favores, e como a função de auditoria interna pode estabelecer políticas para prevenir esse tipo de situação?
"""

distances, indexes = vector_store.search(query, k=3)
chunks = vector_store.get_chunks(indexes, chunks)

gemini_adapter = LLMFactory.get_llm_adapter(
    LLMType.GEMINI, 
    model_name="gemini-1.5-flash"
)

prompt = PromptTemplate().get_prompt(query, chunks, "auditoria interna")
response = gemini_adapter.generate_response(prompt)
print(response)
