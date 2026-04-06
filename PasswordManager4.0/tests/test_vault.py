#tests/test_vault.py

"""
Tests unitaires du coffre fort
"""

# ----- IMPORTS -----
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tempfile
from core.vault import Vault
from core.models import Entry
from cryptography.exceptions import InvalidTag



# Test create()
# Créer un coffre temporaire 
tmp = tempfile.mktemp(suffix='.vault')
v = Vault(tmp)
v.create('MonMotDePasse123!')

assert v.exists(), "Le fichier .vault doit exister sur le disque..."
assert v.is_unlocked, "Le coffre est déverrouillé..."
assert v.salt != None, "Un sel doit être généré."
assert v.key != None, "Une clé doit être générée"

try:
    v.create('MonMotDePasse123!')
    assert False, "Coffre déjà existant"
except FileExistsError:
    pass

print("OK - create()")
os.remove(tmp)


# Test unlock()
tmp     = tempfile.mktemp(suffix='.vault')
v       = Vault(tmp)
v.create('SesameOuvreToi123!')
v.lock()

v.unlock('SesameOuvreToi123!')
assert v.is_unlocked, "Le coffre doit être déverrouiller après unlock()"

try: 
    v.unlock('ShazamOuvreToi123!')
    assert False, "Mauvais mot de passe maître"
except InvalidTag:
    pass

wrong_path  = tempfile.mktemp(suffix='.vault')
v2          = Vault(wrong_path)

try:
    v2.unlock('ShazamOuvreToi123!')
    assert False, "Chemin inexistant..."
except FileNotFoundError:
    pass
    
print("OK - unlock()")
os.remove(tmp)


# Test entries()
tmp     = tempfile.mktemp(suffix='.vault')
v       = Vault(tmp)
v.create('SesameMontreToi123!')

entry   = Entry.new("Gmail", "azarkovich@passwordmanager.fr", "Password456")
v.add_entry(entry)
v.list_entries()

assert len(v.list_entries())        == 1, "La liste doit contenir au moins 1 entrée après un add_entry()"
assert v.list_entries()[0].title    == "Gmail", "Le titre doit correspondre à celui entré"

v.delete_entry(entry.id)
assert len(v.list_entries())        == 0, "La liste doit être vide après delete_entry()"

entry2 = Entry.new("PassMan", "azarkovich@passman.fr", "secret123")

v.add_entry(entry2)
v.update_entry(entry2.id, title="Gmail-Pro", username="Azarkovich", password="ImTheBoss", notes="Important")
assert v.list_entries()[0].title == "Gmail-Pro", "Le titre doit être mis à jour après update_entry()"
v.lock()
try:
    v.add_entry(Entry.new("Test", "test@test.fr", "test123"))
    assert False, "Aurait dû lever PermissionError"
except PermissionError:
    pass

print("OK - entries()")
os.remove(tmp)