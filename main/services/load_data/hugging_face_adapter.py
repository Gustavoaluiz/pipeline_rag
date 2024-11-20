import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(project_dir)

from main.services.load_data.data_port import DataPort
from typing import List
from datasets import load_dataset, concatenate_datasets
from pandas import DataFrame


class HuggingFaceAdapter(DataPort):
    def __init__(
        self, 
        hf_repo: str,
        splits: List[str]
    ):  
        self.hf_repo = hf_repo
        self.splits = splits

    def load_dataset(self) -> DataFrame:
        dataset = load_dataset(self.hf_repo, split=self.splits)
        # Carrega somente as partições especificadas ou todo o dataset
        dataset =  concatenate_datasets(dataset) if self.splits else dataset
        dataset = dataset.to_pandas()

        dataset['nivels_e_conteudo'] = dataset.apply(self._get_nivel_conteudos, axis=1)

        return dataset