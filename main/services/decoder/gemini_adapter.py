import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(project_dir)

import google.generativeai as genai
from main.services.decoder.llm_port import LLMPort


class GeminiAdapter(LLMPort):
    """
    Adaptador para o modelo Gemini.
    """
    ALLOWED_CONFIG_PARAMS = ["temperature", "top_p", "top_k", "max_output_tokens", "response_mime_type"]

    def load_model(self):
        filtered_config = {k: v for k, v in self.generation_config.items() if k in self.ALLOWED_CONFIG_PARAMS}

        model = genai.GenerativeModel(
            model_name=self.model_name,
            safety_settings=self.safety_settings,
            generation_config=filtered_config,
        )
        
        return model

    def generate_response(self, prompt: str) -> str:
        """
        Gera uma resposta a partir do modelo Gemini.
        """
        # Filtra apenas os parâmetros permitidos para o modelo Gemini

        response = self.model.generate_content(prompt)
        
        return response.text
