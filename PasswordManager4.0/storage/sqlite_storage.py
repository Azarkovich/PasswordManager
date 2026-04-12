#storage/sqlite_storage.py

"""
    fichier backend pour le stockage SQLite du coffre chiffré

    Sauvegarde et charge le coffre dans un fichier sqlite
"""

# ----- IMPORT ----- 
import os
import sqlite3

from storage.base import BaseStorage


class SQLiteStorage(BaseStorage):
    
    def __init__(self, path):
        super().__init__()
        self.path   = path

    def exists(self):
        return os.path.exists(self.path)

    def save(self, data):
        with sqlite3.connect(self.path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS vault(" \
            "version        INTEGER," \
            "salt           BLOB," \
            "nonce          BLOB," \
            "ciphertext     BLOB)")

            conn.execute("INSERT OR REPLACE INTO vault VALUES(?,?,?,?)", (
                data["version"], 
                data["salt"], 
                data["nonce"], 
                data["ciphertext"]))


    def load(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute("SELECT version, salt, nonce, ciphertext FROM vault LIMIT 1")
            row = cursor.fetchone()
            return {
                "version"       :row[0],
                "salt"          :row[1],
                "nonce"         :row[2],
                "ciphertext"    :row[3]
            }