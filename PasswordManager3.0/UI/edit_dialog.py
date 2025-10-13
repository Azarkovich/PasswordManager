from __future__ import annotations
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QTextEdit, QPushButton, QCheckBox)
from PySide6.QtCore import Qt

class EditEntryDialog(QDialog):
    def __init__(self, parent=None, *, title="", username="", password="", notes=""):
        super().__init__(parent)
        self.setWindowTitle("Entrée")
        self.setModal(True)

        self.in_title = QLineEdit(title)
        self.in_user  = QLineEdit(username)
        self.in_pass  = QLineEdit(password); self.in_pass.setEchoMode(QLineEdit.Password)
        self.chk_show = QCheckBox("Afficher le mot de passe")
        self.in_notes = QTextEdit(notes)

        self.btn_ok = QPushButton("Enregistrer"); self.btn_cancel = QPushButton("Annuler")

        L = QVBoxLayout(self)
        def row(label, widget):
            h = QHBoxLayout(); h.addWidget(QLabel(label)); h.addWidget(widget); L.addLayout(h)

        row("Titre / Site :", self.in_title)
        row("Identifiant  :", self.in_user)
        row("Mot de passe :", self.in_pass)
        L.addWidget(self.chk_show)
        L.addWidget(QLabel("Notes :"))
        L.addWidget(self.in_notes)

        hb = QHBoxLayout(); hb.addStretch(1); hb.addWidget(self.btn_cancel); hb.addWidget(self.btn_ok)
        L.addLayout(hb)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.chk_show.stateChanged.connect(self.toggle_show)

    def toggle_show(self):
        self.in_pass.setEchoMode(QLineEdit.Normal if self.chk_show.isChecked() else QLineEdit.Password)

    def values(self):
        return {
            "title": self.in_title.text(),
            "username": self.in_user.text(),
            "password": self.in_pass.text(),
            "notes": self.in_notes.toPlainText(),
        }
