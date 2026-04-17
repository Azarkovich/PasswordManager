#ui/login_window.py

"""
    Interface de fenêtre de connexion
"""

# ----- IMPORTS -----
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QLineEdit, QPushButton, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui  import QFont
from ui.theme       import *

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pandora")
        self.setFixedSize(400, 480)
        self.setStyleSheet(f"background-color: {BG_DEEP};")

        # layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(48, 40, 48, 40)
        layout.setSpacing(8)
        layout.addStretch()
        
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())