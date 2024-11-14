import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(project_dir)

from hugging_face_adapter import HuggingFaceAdapter
from local_data_adapter import LocalDataAdapter
from main.domain.load_type import LoadType
from typing import List


class DataLoadFactory:
    
    @staticmethod
    def get_dataset(
        load_type: LoadType, 
        path: str = None,
        hf_repo: str = None, 
        splits: List[str] = None
    ):
        if load_type == LoadType.HUGGING_FACE:
            os.getenv(
                "HF_TOKEN", 
                default=ValueError("HF_TOKEN doesn't exist."))

            return HuggingFaceAdapter(hf_repo, splits).load_dataset()

        elif load_type == LoadType.LOCAL:
            return LocalDataAdapter(path).load_dataset()
        else:
            raise ValueError(f"Unknown storage type: {load_type}")
