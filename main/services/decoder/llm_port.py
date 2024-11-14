from abc import ABC, abstractmethod
import pandas as pd


class LLMPort(ABC):
    """
    Classe base abstrata para adaptadores de modelos LLM.
    """
    def __init__(
            self, 
            model_name: str, 
            generation_config: dict = None, 
            safety_settings: list = None
    ):
        self.model_name = model_name
        self.generation_config = generation_config if generation_config else {}
        self.safety_settings = safety_settings if safety_settings else []
        self.model = self.load_model()

    @abstractmethod
    def load_model(self):
        """
        Carrega o modelo correspondente ao LLM.
        Deve ser implementado pelas subclasses.
        """
        pass

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Gera uma resposta com base no prompt fornecido.

        Args:
            prompt (str): Texto de entrada para gerar uma resposta.

        Returns:
            str: Resposta gerada pelo modelo.
        """
        pass

    def generate_response_from_chunks(self, chunks: pd.DataFrame, user_prompt: str) -> str:
        """
        Gera uma resposta baseada nos chunks fornecidos
        por uma vectorstore, combinado com o prompt do usuário.

        Args:
            chunks (pd.DataFrame): DataFrame contendo os chunks de texto.
            user_prompt (str): Texto do usuário que será utilizado junto ao contexto.

        Returns:
            str: Resposta gerada pelo modelo.
        """
        context = "\n".join(chunks['content'].tolist())
        combined_prompt = f"Contexto:\n{context}\n\nPergunta do usuário:\n{user_prompt}"
        return self.generate_response(combined_prompt)
