#test_auth.py

"""
Tests unitaires de connexion 
"""

# ----- IMPORTS -----
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cryptography.exceptions import InvalidTag
from core.crypto import generate_salt, derive_key
from core.auth import create_master_password, verify_master_password


mot_de_passe    = "MonSuperMotDePasse"
wrong_password  = "password123"

salt, key = create_master_password(mot_de_passe)
key_verify = verify_master_password(mot_de_passe, salt)

wrong_key_verify = verify_master_password(wrong_password, salt)

assert isinstance(salt, bytes), "Doit retourner des bytes."
assert isinstance(key, bytes), "Doit retourner des bytes."
assert len(key)     == 32, "La taille de la clé doit faire 32 bytes."

assert key          == key_verify, "Les deux clés doivent être égales"
assert  key_verify  != wrong_key_verify, "Les deux clés sont différentes "

print("OK - auth()")



