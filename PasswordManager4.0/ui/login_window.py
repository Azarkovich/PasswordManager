#ui/login_window.py

"""
    Interface de fenêtre de connexion
"""

# ----- IMPORTS -----
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
        self.setWindowTitle("Password-Manager")
        self.setFixedSize(400, 480)
        self.setStyleSheet(f"background-color: {BG_DEEP};")

        # layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(48, 40, 48, 40)
        layout.setSpacing(8)
        
        # label
        label_title = QLabel("PassMan")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet(f"color: {TEXT_PRI}; font-size: 22px; font-weight: 500;")
        layout.addWidget(label_title)

        label_second = QLabel("Gestionnaire de mots de passe")
        label_second.setAlignment(Qt.AlignCenter)
        label_second.setStyleSheet(f"color: {TEXT_SEC}; font-size: 13px")
        layout.addWidget(label_second)
        layout.addSpacing(20)

        label_mdp = QLabel("Mot de passe maître")
        label_mdp.setStyleSheet(f"color: {VIOLET_LT}; font-size: 11px;")
        layout.addWidget(label_mdp)