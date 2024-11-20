import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(project_dir)

import torch
import numpy as np
from numpy.typing import NDArray
from main.domain.load_type import LoadDataType
from main.services.encoder.embedding_port import EmbeddingPort
from transformers import AutoTokenizer, AutoModel
from typing import List

class EmbeddingHuggingFace(EmbeddingPort):

    def load_encoder(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.embedding_model = AutoModel.from_pretrained(self.model_name)
        self.embedding_dim = self.embedding_model.config.hidden_size

    def embed_documents(self, documents: List[str]) -> NDArray[np.float32]:        
        inputs = self.tokenizer(documents, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():  
            outputs = self.embedding_model(**inputs)
            # Utiliza o CLS token para representar a sentença
            # já somente modelos encoder serão utilizados
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()

        return embeddings
