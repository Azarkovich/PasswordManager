#core/vault.py

"""
    Chiffre, déverouille et structure les entrées du coffre fort.
"""

# ----- IMPORTS -----
from core.crypto import (
    encrypt, decrypt, derive_key, generate_salt, generate_nonce
)
from core.models import Entry


class Vault:
    VERSION = 1

    def __init__(self, path: str):
        self.path = path
        self.salt = None
        self.key = None
        self.entries = []
        self.is_unlocked = False
        