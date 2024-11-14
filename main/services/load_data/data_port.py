from abc import ABC, abstractmethod
from pandas import DataFrame


class DataPort(ABC):

    @abstractmethod
    def load_dataset(self) -> DataFrame:
        pass

    @staticmethod
    def _get_nivel_conteudos(row) -> str:
        """Espera dataset no padrão REGULAÇÃO da equipe de Crawler."""
        
        nivels = [f'nivel_{n}' for n in range(1, 6)]
        full_text = f"{row['descricao_categoria']} - {row['normativa']}:\n"

        for nivel in nivels:
            value = row[nivel]
            if value == 'nan':
                continue
            full_text += f"- {value}\n\n"
        full_text += row['conteudo']

        return full_text
