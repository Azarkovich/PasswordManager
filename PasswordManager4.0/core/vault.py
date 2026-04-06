#core/vault.py

"""
    Chiffre, déverouille et structure les entrées du coffre fort.
"""

# ----- IMPORTS -----
import os
import cbor2

from datetime import datetime, timezone
from core.crypto import (
    encrypt, decrypt, derive_key, generate_salt, generate_nonce
)
from core.models import Entry


class Vault: 
    VERSION = 1 

    def __init__(self, path: str):
        self.path           = path
        self.salt           = None
        self.key            = None
        self.entries        = []
        self.is_unlocked    = False


    def exists(self):
        return os.path.exists(self.path)
    

    def create(self, master_password: str):
        # Vérifier si le coffre existe déjà
        if self.exists():
            raise FileExistsError("Un coffre fort existe déjà à ce chemin...")
        
        self.salt           = generate_salt()
        self.key            = derive_key(master_password, self.salt)
        self.entries        = []
        self.is_unlocked    = True
        self._save_file()


    def _save_file(self):
        self._require_unlocked
        # Sérialiser les entrées
        plaintext = cbor2.dumps({"entries": [e.to_dict() for e in self.entries]})

        nonce, ciphertext = encrypt(plaintext, self.key)
        outer = {
            "version"       : self.VERSION,
            "salt"          : self.salt, 
            "nonce"         : nonce,
            "ciphertext"    : ciphertext
        }

        # Écriture atomique
        tmp = self.path + ".tmp"
        with open(tmp, "wb") as f:
            cbor2.dump(outer, f)
        os.replace(tmp, self.path)

    
    def unlock(self, master_password):
        if not self.exists():
            raise FileNotFoundError("Le fichier .tmp n'existe pas...")
        
        with open(self.path, "rb") as f:
            outer = cbor2.load(f)
        
        self.salt       = outer["salt"]
        nonce           = outer["nonce"]
        ciphertext      = outer["ciphertext"]
        self.key        = derive_key(master_password, self.salt)
        decrypted       = decrypt(nonce, ciphertext, self.key)
        plaintext       = cbor2.loads(decrypted)
        self.entries    = [Entry.from_dict(e) for e in plaintext["entries"]]

        self.is_unlocked = True


    def lock(self):
        if not self.is_unlocked:
            return 
        self.salt           = None
        self.key            = None
        self.entries        = []
        self.is_unlocked    = False 


    def _require_unlocked(self):
        if not self.is_unlocked:
            raise PermissionError("Le coffre fort est verrouillé...")
        
    
    def add_entry(self, entry: Entry):
        self._require_unlocked()
        self.entries.append(entry)
        self._save_file()


    def delete_entry(self, entry_id: str):
        self._require_unlocked()
        self.entries    = [e for e in self.entries if e.id != entry_id]
        self._save_file()
        

    def update_entry(self, entry_id: str, *, title: str, username: str, password: str, notes: str = ""):
        self._require_unlocked()
        for e in self.entries:
            if e.id             == entry_id:
                e.title         = title
                e.username      = username
                e.password      = password
                e.notes         = notes
                e.updated_at    = datetime.now(timezone.utc).isoformat()
            break
        self._save_file()

    def list_entries(self):
        self._require_unlocked()
        return list(self.entries)
    



        




    
    
