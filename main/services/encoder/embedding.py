import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(project_dir)

import torch
import numpy as np
from numpy.typing import NDArray
from main.domain.load_type import LoadType
from transformers import AutoTokenizer, AutoModel
from typing import List

class Embedding:
    def __init__(self):
        self.tokenizer = None
        self.embedding_model = None

    def get_encoder(
            self,
            load_type: LoadType,
            hf_repo: str = None,
    ):
        if load_type == LoadType.HUGGING_FACE:
            os.getenv(
                "HF_TOKEN", 
                default=ValueError("HF_TOKEN doesn't exist."))

            
            self.tokenizer = AutoTokenizer.from_pretrained(hf_repo)
            self.embedding_model = AutoModel.from_pretrained(hf_repo)

    def embed_documents(self, documents: List[str]) -> NDArray[np.float32]:        
        inputs = self.tokenizer(documents, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():  
            outputs = self.embedding_model(**inputs)

            # Utiliza o CLS token para representar a sentença
            # já somente modelos encoder serão utilizados
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()

        return embeddings
    
    def embed_query(self, query: str) -> NDArray[np.float32]:
        return self.embed_documents([query])[0]
    