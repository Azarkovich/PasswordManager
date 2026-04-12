#storage/base.py

"""
    Interface abstraite commune à tous les backends

    Tous les backends (fichier, SQLite) doit implémenter:
    - exists()
    - save()
    - load()
"""

# ----- IMPORT ----- 
from abc import ABC, abstractmethod


class BaseStorage(ABC):

    @abstractmethod
    def exists(self)-> bool:
        pass

    @abstractmethod
    def save(self, data: dict) -> None:
        pass

    @abstractmethod
    def load(self)-> dict:
        pass
