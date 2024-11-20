import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(project_dir)

from main.domain.embedding_type import EmbeddingType
from main.services.encoder.embedding_port import EmbeddingPort
from main.services.encoder.hf_adapter import EmbeddingHuggingFace
from main.services.encoder.vertexai_adapter import EmbeddingVertexAI

class EmbeddingFactory:

    @staticmethod
    def get_embedding_adapter(
        embedding_type: EmbeddingType, 
        model_name: str = None,
        embedding_dim: int = None
    ) -> EmbeddingPort:
        
        if embedding_type == EmbeddingType.HUGGING_FACE:
            if not os.getenv("HF_TOKEN"):
                raise ValueError("HF_TOKEN doesn't exist.")
            return EmbeddingHuggingFace(model_name)
        
        elif embedding_type == EmbeddingType.VERTEX_AI:
            return EmbeddingVertexAI(model_name=model_name, embedding_dim=embedding_dim)
        
        else:
            raise ValueError(f"Modelo tipo {embedding_type} não reconhecido.")