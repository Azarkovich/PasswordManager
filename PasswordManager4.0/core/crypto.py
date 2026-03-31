#/corecrypto.py

"""
Couche cryptographique du gestionnaire de mots de passe 
"""

# ----- IMPORTS -----
import os
import argon2.low_level as argon2_ll
from argon2 import Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM 


# ----- Settings -----
ARGON2_TIME_COST    = 3
ARGON2_MEMORY_COST  = 65536
ARGON2_PARALLELISM  = 4
ARGON2_HASH_LENGTH  = 32
ARGON2_SALT_LENGTH  = 32


# ----- AES-GCM -----
AES_NONCE_LENGTH    = 12



def generate_salt()-> bytes:
    return os.urandom(ARGON2_SALT_LENGTH)


def generate_nonce()->bytes:
    return os.urandom(AES_NONCE_LENGTH)


def derive_key(password: str, salt: bytes)-> bytes:
    return argon2_ll.hash_secret_raw(
        secret          = password.encode('utf-8'),
        salt            = salt,
        time_cost       = ARGON2_TIME_COST,
        memory_cost     = ARGON2_MEMORY_COST,
        parallelism     = ARGON2_PARALLELISM,
        hash_len        =ARGON2_HASH_LENGTH,
        type            = Type.ID
    )


def encrypt(data: bytes, key: bytes)-> tuple[bytes, bytes]:
    nonce = generate_nonce()
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce, ciphertext


def decrypt(nonce: bytes, ciphertext: bytes, key: bytes)-> bytes:
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)