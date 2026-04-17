#main.py

"""
    Fichier principal - point d'entrée de l'application
    Assemble toutes les couches config, storage, vault et lance l'UI
"""

# ----- IMPORTS ----- 
import sys

from PySide6.QtWidgets          import QApplication
from storage.file_storage       import FileStorage
from storage.sqlite_storage     import SQLiteStorage
from core.vault                 import Vault
from ui.login_window            import LoginWindow
from config                     import load_config



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Charger la config
    config = load_config()

    # 2. Créer le bon backend
    if config["backend"] == "sqlite":
        storage = SQLiteStorage(config["vault_path"])
    else:
        storage = FileStorage(config["vault_path"])

    # 3. Créer le vault
    vault = Vault(storage)

    # 4. Lancer le login
    win = LoginWindow(vault)
    win.show()

    sys.exit(app.exec())