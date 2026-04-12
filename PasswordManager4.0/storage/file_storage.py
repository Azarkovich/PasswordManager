#storage/file_storage

"""
    Fichier backend pour le stockage du coffre chiffré

    Sauvegarde et charge le coffre dans un fichier binaire
    au format CBOR avec écriture atomique (.tmp + os.replace)
"""

# ----- IMPORT ----- 
import os
import cbor2

from storage.base import BaseStorage


class FileStorage(BaseStorage):
    
    def __init__(self, path):
        super().__init__()
        self.path   = path

    def exists(self)-> bool:
        return os.path.exists(self.path)

    def save(self, data: dict) -> None:
        tmp = self.path + ".tmp"
        with open(tmp, "wb") as f:
            cbor2.dump(data, f)
        os.replace(tmp, self.path)

    def load(self)-> dict:
        with open(self.path, "rb") as f:
            data = cbor2.load(f)
        return data
        