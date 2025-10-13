# core/hashage.py

from __future__ import annotations
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import Type, hash_secret_raw
import os

# Paramètres par défaut (on ajustera plus tard si besoin)
ARGON2_MEMORY_KIB = 128 * 1024   # 128 MiB (mémoire-dur)
ARGON2_TIME_COST  = 2
ARGON2_PARALLELISM = 1
KEY_LEN = 32  # 256 bits pour AES-256-GCM


def derive_key(password: str, salt: bytes,
               memory_kib: int = ARGON2_MEMORY_KIB,
               time_cost: int = ARGON2_TIME_COST,
               parallelism: int = ARGON2_PARALLELISM) -> bytes:
    """
    Dérive une clé symétrique (32 octets) depuis un mot de passe via Argon2id.
    """
    if not isinstance(password, str):
        raise TypeError("password must be str")
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes")
    pwd_bytes = password.encode("utf-8")
    key = hash_secret_raw(secret=pwd_bytes, salt=salt,
                          time_cost=time_cost,
                          memory_cost=memory_kib,
                          parallelism=parallelism,
                          hash_len=KEY_LEN,
                          type=Type.ID)
    return key

def encrypt(plaintext: bytes, key: bytes, aad: Optional[bytes] = None) -> tuple[bytes, bytes]:
    """
    Chiffre en AES-256-GCM. Retourne (nonce, ciphertext).
    """
    if not isinstance(plaintext, (bytes, bytearray)):
        raise TypeError("plaintext must be bytes")
    if len(key) != KEY_LEN:
        raise ValueError("key must be 32 bytes")
    nonce = os.urandom(12)  # 96 bits recommandé pour GCM
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, plaintext, aad)
    return nonce, ct

def decrypt(nonce: bytes, ciphertext: bytes, key: bytes, aad: Optional[bytes] = None) -> bytes:
    """
    Déchiffre AES-256-GCM.
    """
    if len(key) != KEY_LEN:
        raise ValueError("key must be 32 bytes")
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, aad)
