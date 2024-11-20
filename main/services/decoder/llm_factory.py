import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(project_dir)

from main.domain.llm_type import LLMType
from main.services.decoder.gemini_adapter import GeminiAdapter

class LLMFactory:
    """
    Fábrica para instanciar adaptadores LLM de diferentes fornecedores.
    """

    @staticmethod
    def get_llm_adapter(llm_type: LLMType, model_name: str, generation_config: dict = None):
        """
        Retorna uma instância do adaptador correspondente ao tipo de LLM.

        Args:
            llm_type (LLMType): Tipo do LLM a ser instanciado.
            model_name (str): Nome do modelo a ser carregado.
            generation_config (dict, optional): Configurações de geração para o modelo.

        Returns:
            LLMBaseAdapter: Instância do adaptador correspondente ao LLM.

        Raises:
            ValueError: Se o tipo de LLM for desconhecido.
        """

        if llm_type == LLMType.GEMINI:
            if not os.getenv("GEMINI_API_KEY"):
                raise ValueError("GEMINI_API_KEY doesn't exist.")
            
            return GeminiAdapter(model_name, generation_config)

        else:
            raise ValueError(f"Unknown LLM type: {llm_type}")
        