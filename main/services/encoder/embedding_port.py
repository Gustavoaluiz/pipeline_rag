import numpy as np
from abc import ABC, abstractmethod
from typing import List, Optional
from numpy.typing import NDArray

class EmbeddingPort(ABC):
    def __init__(
            self,
            model_name: str = None,
            embedding_dim: int = None,
    ):
        self.model_name = model_name
        self.embedding_dim = embedding_dim
        self.embedding_model = self.load_encoder()

    @abstractmethod
    def load_encoder(self):
        """
        Carrega o modelo correspondente ao LLM.
        Deve ser implementado pelas subclasses.
        """
        pass

    @abstractmethod
    def embed_documents(self, documents: List[str], task: Optional[str]) -> NDArray[np.float32]:
        pass

    def embed_query(self, query: str, task: Optional[str]) -> NDArray[np.float32]:
        return self.embed_documents([query], task=task)[0]