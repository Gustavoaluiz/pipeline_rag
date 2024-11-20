from abc import ABC, abstractmethod
from pandas import DataFrame


class DataPort(ABC):

    @abstractmethod
    def load_dataset(self) -> DataFrame:
        pass

    @staticmethod
    def _get_nivel_conteudos(row) -> str:
        """Gera o texto hierárquico com contexto explícito."""
        full_text = ''
        nivels = [f'nivel_{n}' for n in range(1, 6)]
        categoria = row.get('descricao_categoria')
        normativa = row.get('normativa')

        if isinstance(categoria, str):
            full_text = f"Categoria: {categoria}\n"
        if  isinstance(normativa, str):
            full_text += f"Normativa: {normativa}\n"

        for nivel in nivels:
            value = row.get(nivel)
            if isinstance(value, str):
                full_text += f"{nivel}: {value}\n"
        
        # Adiciona o conteúdo principal no final
        full_text += f"{row['conteudo']}"
        
        return full_text