#config.py

"""
    Fichier de configuration de l'utilisateur

    Stocke les préférences (backend, chemin du coffre) dans un fichier config.json
    dans le repertoire utilisateur
"""

# ----- IMPORTS -----
import os
import json

from platformdirs import user_data_dir


APP_NAME = "Password-Manager"


def get_app_dir() -> str:
    path = user_data_dir(APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

def get_default_vault_path() -> str:
    return os.path.join(get_app_dir(), "vault.vault")

def load_config()-> dict:
    chemin = os.path.join(get_app_dir(), "config.json")
    if not os.path.exists(chemin):
        return {
            "backend"    : "file",
            "vault_path" : get_default_vault_path()
        }
    with open(chemin, "r") as f:
        return json.load(f)
    
def save_config(config: dict)-> None:
    path = os.path.join(get_app_dir(), "config.json")
    with open(path, "w") as f:
        json.dump(config, f, indent=4)