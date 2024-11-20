import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(project_dir)

from typing import List, Optional
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
import vertexai
from google.cloud import aiplatform
from main.services.encoder.embedding_port import EmbeddingPort
from numpy.typing import NDArray
import numpy as np


class EmbeddingVertexAI(EmbeddingPort):

    def load_encoder(self):
        self.model_name = 'text-multilingual-embedding-002' if not self.model_name else self.model_name
        self.embedding_dim = 768 if not self.embedding_dim else self.embedding_dim
        
        return TextEmbeddingModel.from_pretrained(self.model_name)

    @staticmethod
    def _batch_chunks(chunks: List[str], batch_size: int = 250):
        """A API tem o limite de 250 documentos por request para criar os embeddings"""
        for i in range(0, len(chunks), batch_size):
            yield chunks[i:i + batch_size]

    @staticmethod
    def _batch_inputs(inputs: List[TextEmbeddingInput], batch_size: int = 10):
        for i in range(0, len(inputs), batch_size):
            yield inputs[i:i + batch_size]

    def embed_documents(
            self, 
            chunks: List[str], 
            task: str = 'RETRIEVAL_DOCUMENT',
    ) -> NDArray[np.float32]:
        """Embeds texts with a pre-trained, foundational model.
        Args:
            texts (List[str]): A list of texts to be embedded.
            task (str): The task type for embedding. Check the available tasks in the model's documentation.
            dimensionality (Optional[int]): The dimensionality of the output embeddings.
        Returns:
            List[List[float]]: A list of lists containing the embedding vectors for each input text
        """

        # A API tem o limite de 250 documentos por request para criar os embeddings
        # Então, é necessário dividir os documentos em batches
        batches: List[List[str]] = self._batch_chunks(chunks)
        all_embeddings = []
        for batch in batches:
            # Otimiza os embeddings conforme o tipo de task, melhorando, 
            # segundo a documentação, a qualidade dos embeddings
            inputs = [TextEmbeddingInput(chunk, task) for chunk in batch]
            kwargs = dict(output_dimensionality=self.embedding_dim) if self.embedding_dim else {}
            
            for inputs_batch in self._batch_inputs(inputs):
                embeddings = self.embedding_model.get_embeddings(inputs_batch, **kwargs)
                embeddings = np.array([embedding.values for embedding in embeddings], dtype=np.float32)
                all_embeddings.append(embeddings)

        embeddings = np.concatenate(all_embeddings, axis=0)

        return embeddings
