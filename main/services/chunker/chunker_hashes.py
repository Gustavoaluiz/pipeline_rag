import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(current_dir, '..', "..", ".."))
sys.path.append(BASE_DIR)

import pandas as pd
import hashlib
from pandas import DataFrame

class ChunksHashes:
    def __init__(self, path: str = None):
        hashes_path = os.path.join(BASE_DIR, 'data', 'chunk', 'chunks_hashes.csv')
        self.path = path if path else hashes_path
        self.hash = None
        
    def _update(self, new_hashes: DataFrame):
        self.hash = pd.concat([self.hash, new_hashes])
        self.hash.to_csv(self.path, index=False)

    def _read_hashes(self) -> DataFrame:
        if os.path.exists(self.path):
            self.hash = pd.read_csv(self.path)
        else:
            self.hash = pd.DataFrame(columns=['hash'])

    def hash_document(self, text: str):
        """
        Gera um hash único para um documento de texto.
        """
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def get_deduplicated_chunks(self, chunks: DataFrame) -> DataFrame:
        chunks = chunks.assign(
            hash=chunks.iloc[:, 0].apply(self.hash_document)
        )
        self._read_hashes()
        chunks = chunks[~chunks['hash'].isin(self.hash['hash'])]
        self._update(chunks[['hash']])

        return chunks
