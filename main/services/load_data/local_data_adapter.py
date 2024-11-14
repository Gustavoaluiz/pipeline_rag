from data_port import DataPort
import pandas as pd
from pandas import DataFrame


class LocalDataAdapter(DataPort):
    def __init__(self, path: str):
        self.path = path

    def load_dataset(self) -> DataFrame:
        dataset = pd.read_csv(self.path)
        dataset['nivels_e_conteudo'] = dataset.apply(self._get_nivel_conteudos, axis=1)

        return dataset
    