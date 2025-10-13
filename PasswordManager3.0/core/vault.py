# core/vault.py
from __future__ import annotations
from typing import List, Optional
import os
import cbor2
import shutil

from .hashage import derive_key, encrypt, decrypt
from .models import Entry

class Vault:
    VERSION = 1

    def __init__(self, path: str):
        self.path = path
        self.salt: Optional[bytes] = None
        self.key: Optional[bytes] = None
        self.entries: List[Entry] = []
        self.is_unlocked: bool = False

    def exists(self) -> bool:
        return os.path.exists(self.path)

    # Création d’un coffre vide
    def create(self, master_password: str):
        if self.exists():
            raise FileExistsError("Vault already exists")
        self.salt = os.urandom(16)
        self.key  = derive_key(master_password, self.salt)
        self.entries = []
        self.is_unlocked = True
        self._save_file()

    # Déverrouillage d’un coffre existant
    def unlock(self, master_password: str):
        if not self.exists():
            raise FileNotFoundError("Vault does not exist. Use create().")
        with open(self.path, "rb") as f:
            outer = cbor2.load(f)
        if outer.get("version") != self.VERSION:
            raise ValueError("Unsupported vault version")
        self.salt = outer["salt"]
        self.key  = derive_key(master_password, self.salt)
        plaintext = decrypt(outer["nonce"], outer["ciphertext"], self.key)
        data = cbor2.loads(plaintext)
        self.entries = [Entry.from_dict(e) for e in data.get("entries", [])]
        self.is_unlocked = True

    def lock(self):
        self.key = None
        self.is_unlocked = False

    def add_entry(self, e: Entry):
        self._require_unlocked()
        self.entries.append(e)
        self._save_file()

    def delete_entry(self, entry_id: str):
        self._require_unlocked()
        self.entries = [e for e in self.entries if e.id != entry_id]
        self._save_file()

    def list_entries(self) -> List[Entry]:
        self._require_unlocked()
        return list(self.entries)

    # Écriture atomique sur disque
    def _save_file(self):
        self._require_unlocked()
        data = {"entries": [e.to_dict() for e in self.entries]}
        plaintext = cbor2.dumps(data)
        nonce, ct = encrypt(plaintext, self.key)  # type: ignore
        outer = {"version": self.VERSION, "salt": self.salt, "nonce": nonce, "ciphertext": ct}
        tmp = self.path + ".tmp"
        with open(tmp, "wb") as f:
            cbor2.dump(outer, f)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, self.path)

    def _require_unlocked(self):
        if not self.is_unlocked or self.key is None:
            raise PermissionError("Vault is locked")

    def update_entry(self, entry_id: str, *, title: str, username: str, password: str, notes: str = ""):
        self._require_unlocked()
        changed = False
        for i, e in enumerate(self.entries):
            if e.id == entry_id:
                from datetime import datetime
                e.title = title
                e.username = username
                e.password = password
                e.notes = notes
                e.updated_at = datetime.utcnow().isoformat() + "Z"
                self.entries[i] = e
                changed = True
                break
        if changed:
            self._save_file()
        else:
            raise KeyError("Entry not found")
        
    def export_to(self, dest_path: str):
        """Copie le coffre actuel (chiffré) vers dest_path."""
        if not self.exists():
            raise FileNotFoundError("Vault does not exist")
        # écriture atomique simple via tmp
        tmp = dest_path + ".tmp"
        shutil.copy2(self.path, tmp)
        os.replace(tmp, dest_path)


    def import_from(self, src_path: str):
        """Remplace le coffre courant par le fichier src_path (chiffré)."""
        if not os.path.exists(src_path):
            raise FileNotFoundError("Source file not found")
        tmp = self.path + ".tmp"
        shutil.copy2(src_path, tmp)
        os.replace(tmp, self.path)
        # invalider l'état courant
        self.key = None
        self.is_unlocked = False
        self.entries = []
        self.salt = None
