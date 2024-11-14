import os, sys
from dataclasses import dataclass

project_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(project_dir)

from regulacao_domain.categoria_regulacao import CategoriaRegulacao


@dataclass
class RegistroHierarquico:
    normativa: str | None = None
    url: str = None
    categoria: CategoriaRegulacao = None
    descricao_categoria: str = None
    nivel_1: str = None
    nivel_2: str | None = None
    nivel_3: str | None = None
    nivel_4: str | None = None
    nivel_5: str | None = None
    conteudo: str = None
