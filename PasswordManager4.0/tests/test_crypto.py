#tests/test_crypto.py

"""
Tests unitaires de la couche cryptographique
"""

# ----- IMPORTS -----
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cryptography.exceptions import InvalidTag
from core.crypto import (
    generate_salt, generate_nonce,
    derive_key, encrypt, decrypt,
    ARGON2_SALT_LENGTH, ARGON2_HASH_LENGTH, AES_NONCE_LENGTH
)


# Test generate_salt()

s1 = generate_salt()
s2 = generate_salt()

assert isinstance(s1, bytes), "generate_salt() doit retourner des bytes"
assert len(s1) == ARGON2_SALT_LENGTH, "Le sel doit faire ARGON2_SALT_LENGTH bytes"
assert s1 != s2, "Deux sels générés ne doivent jamais être identiques"

print("OK - generate_salt()")


# Test generate_nonce()

n1 = generate_nonce()
n2 = generate_nonce()

assert isinstance(n1, bytes), "generate_nonce() doit retourner des bytes"
assert len(n1) == AES_NONCE_LENGTH, "Le nonce doit faire AES_NONCE_LENGTH bytes"
assert n1 != n2, "Nonce = Number used once, ils ne peuvent jamais être identiques"

print("OK - generate_nonce()")


# KDF 
salt    = generate_salt()
salt2   = generate_salt()
mdp     = "MonMotDePasseTest!"
mdp2    = "MotDePasseDifférent!"

key     = derive_key(mdp, salt)
key_bis = derive_key(mdp, salt)     # Même mdp, même sel
key_sel = derive_key(mdp, salt2)    # Même mdp, différent sel
key_mdp = derive_key(mdp2, salt)    # mdp diiférent, même sel

assert isinstance(key, bytes),          "La clé retournée est de type bytes"
assert len(key) == ARGON2_HASH_LENGTH,  "la clé doit faire 32 bytes"

assert key == key_bis,                  "Déterminisme: Même mdp + même sel -> même clé"
assert key != key_sel,                  "même mdp + sel différent -> clé différente"
assert key != key_mdp,                  "mdp différent + même sel -> clé différente"

print("OK - derive_key()")


# Encrypt
salt_encrypt                = generate_salt()
nonce_encrypt               = generate_nonce()
password_encrypt            = "MonMotDePasseSuperSecret"
key_encrypt                 = derive_key(password_encrypt, salt_encrypt)
data_encrypt                = b"Ma Super Phrase a Chiffrer"

nonce , ciphertext_encrypt  = encrypt(data_encrypt,key_encrypt)
nonce2, ciphertext2         = encrypt(data_encrypt, key_encrypt)

assert isinstance(nonce, bytes), "Nonce doit retourner des bytes"
assert len(nonce) == AES_NONCE_LENGTH, "Nonce doit être égal à AES_NONCE_LENGTH bytes"
assert nonce != nonce2, "Deux chiffrement du même plaintext-> deux nonces différents"

assert isinstance(ciphertext_encrypt,bytes), "ciphertext_encrypt doit retourner des bytes"
assert ciphertext_encrypt != data_encrypt, "Le ciphertext_encrypt ne doit pas être égal au plaintext"
assert len(ciphertext_encrypt) == len(data_encrypt) + 16, "Ciphertext = plaintext + 16 bytes (tag GCM)"

print("OK - encrypt()")


# Decrypt
salt_decrypt     = generate_salt()
password_decrypt = "MonSuperMotdePasseADechiffrer"
key_decrypt      = derive_key(password_decrypt, salt_decrypt)
plaintext        = b"Ma Super Phrase a Dechiffrer"

# On chiffre d'abord pour avoir un vrai ciphertext
nonce_decrypt, ciphertext_decrypt = encrypt(plaintext, key_decrypt)

decrypted = decrypt(nonce_decrypt, ciphertext_decrypt, key_decrypt)

assert decrypted == plaintext, "decrypt() doit retrouver exactement le plaintext original"

# 3 cas d'échec
# Mauvais mdp
wrong_password = "OupsMauvaisMdp"
wrong_salt = generate_salt()
wrong_key = derive_key(wrong_password, wrong_salt)

try:
    decrypt(nonce_decrypt, ciphertext_decrypt, wrong_key)
    assert False, "Mauvaise clé"
except InvalidTag:
    pass

# Ciphertext corrompu 
corrupted_ciphertext = bytearray(ciphertext_decrypt)
corrupted_ciphertext[0] ^= 1

try:
    decrypt(nonce_decrypt, bytes(corrupted_ciphertext), key_decrypt)
    assert False, "Aurait dû lever InvalidTag : ciphertext corrompu"
except InvalidTag:
    pass   

# Nonce corrompu
corrupted_nonce = bytearray(nonce_decrypt)
corrupted_nonce[0] ^= 1
try:
    decrypt(bytes(corrupted_nonce), ciphertext_decrypt, key_decrypt)
    assert False, "Aurait dû lever InvalidTag — nonce corrompu"
except InvalidTag:
    pass

print("OK - decrypt()")