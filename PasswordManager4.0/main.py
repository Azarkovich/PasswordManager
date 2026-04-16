#main.py

"""
    Fichier principal - point d'entrée de l'application
    Assemble toutes les couches config, storage, vault et lance l'UI
"""

# ----- IMPORTS ----- 
import config
from storage.file_storage       import FileStorage
from storage.sqlite_storage     import SQLiteStorage
from core.vault                 import Vault


if __name__ == "__main__":
    # 1. Charger la config
    configuration = config.load_config()

    # 2. Créer le bon backend
    if configuration["backend"] == "sqlite":
        storage = SQLiteStorage(configuration["vault_path"])
    else:
        storage = FileStorage(configuration["vault_path"])

    # 3. Créer le Vault avec le backend
    vault = Vault(storage)

    # UI
    print("Vault prêt. UI à venir")