#auth.py

"""
Gestion du mot de passe maître
"""

# ----- IMPORT -----
from core.crypto  import generate_salt,derive_key

def create_master_password(password: str)-> tuple[bytes, bytes]:
    salt = generate_salt()
    key = derive_key(password, salt)
    return salt, key


def verify_master_password(password: str, salt: bytes) -> bytes:
    key = derive_key(password, salt)
    return key