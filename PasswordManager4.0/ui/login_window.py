#ui/login_window.py

"""
    Interface de fenêtre de connexion
"""

# ----- IMPORTS -----
import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QLineEdit, QPushButton, QApplication,
    QMessageBox
)
from PySide6.QtCore             import Qt
from PySide6.QtGui              import QFont
from cryptography.exceptions    import InvalidTag

from ui.theme                   import *
from storage.file_storage       import FileStorage
from core.vault                 import Vault
from ui.main_window             import MainWindow

# ----------


class LoginWindow(QWidget):
    def __init__(self, vault):
        super().__init__()
        self.vault = vault
        self.setWindowTitle("Pandora")
        self.setFixedSize(400, 480)
        self.setStyleSheet(f"background-color: {BG_DEEP};")

        # layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(48, 40, 48, 40)
        layout.setSpacing(8)
        
        # ----- LABEL 
        label_title = QLabel("Pandora")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet(f"color: {TEXT_PRI}; font-size: 22px; font-weight: 500;")
        layout.addWidget(label_title)

        # Sous titre
        label_second = QLabel("Gestionnaire de mots de passe")
        label_second.setAlignment(Qt.AlignCenter)
        label_second.setStyleSheet(f"color: {TEXT_SEC}; font-size: 13px")
        layout.addWidget(label_second)
        layout.addSpacing(20)

        # Mot de passe maître
        label_mdp = QLabel("Mot de passe maître")
        label_mdp.setStyleSheet(f"color: {VIOLET_LT}; font-size: 11px;")
        layout.addWidget(label_mdp)

        # Entrée mdp
        self.input_mdp = QLineEdit()
        self.input_mdp.setEchoMode(QLineEdit.Password)
        self.input_mdp.setPlaceholderText("••••••••••••")
        self.input_mdp.setFixedHeight(38)
        self.input_mdp.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_LT};
                border-radius: 6px;
                color: {TEXT_PRI};
                font-size: 14px;
                padding: 0 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {VIOLET};
            }}
        """)
        layout.addWidget(self.input_mdp)
        layout.addSpacing(8)

        # Déverouiller 
        self.btn_unlock = QPushButton("Déverrouiller")
        self.btn_unlock.setFixedHeight(38)
        self.btn_unlock.setCursor(Qt.PointingHandCursor)
        self.btn_unlock.setStyleSheet(f"""
            QPushButton {{
                background-color: {VIOLET};
                color: {VIOLET_XLT};
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #6d28d9;
            }}
            QPushButton:pressed {{
                background-color: #5b21b6;
            }}
        """)
        layout.addWidget(self.btn_unlock)
        layout.addSpacing(12)

        # Première connexion 
        self.btn_first = QPushButton("Première fois ? Créer un coffre")
        self.btn_first.setFlat(True)
        self.btn_first.setCursor(Qt.PointingHandCursor)
        self.btn_first.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {VIOLET_LT};
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {VIOLET_XLT};
            }}
        """)
        layout.addWidget(self.btn_first)

        # Connecions boutons 
        self.btn_unlock.clicked.connect(self._on_unlock)
        self.btn_first.clicked.connect(self._on_create)


    def _on_unlock(self):
        password = self.input_mdp.text()

        if not password:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un mot de passe.")
            return
        
        try:
            self.vault.unlock(password)
            self.main_window = MainWindow(self.vault)
            self.main_window.show()
            self.close()
        except InvalidTag:
            QMessageBox.critical(self, "Erreur", "Mot de passe incorrect.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Erreur", "Aucun coffre trouvé... Créez-en un d'abord")


    def _on_create(self):
        password = self.input_mdp.text()
        if not password:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un mot de passe maître.")
            return
        try:
            self.vault.create(password)
            QMessageBox.information(self, "Succès", "Coffre créé. Gardez bien votre mot de passe.")
            self.main_window = MainWindow(self.vault)
            self.main_window.show()
            self.close()
        except FileExistsError:
            QMessageBox.warning(self, "Erreur", "Un coffre existe déjà.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    tmp = tempfile.mktemp(suffix='.vault')
    vault = Vault(FileStorage(tmp))
    win = LoginWindow(vault)
    win.show()
    sys.exit(app.exec())