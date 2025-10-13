# ui/dialogs.py


from PySide6.QtWidgets import QInputDialog, QLineEdit, QWidget, QMessageBox, QTextEdit, QDialog, QVBoxLayout, QLabel,QPushButton, QHBoxLayout

def ask_master_password(parent: QWidget, title: str = "Déverrouiller le coffre") -> str | None:
    pwd, ok = QInputDialog.getText(parent, title, "Mot de passe maître:", QLineEdit.Password)
    return pwd if ok else None

def ask_new_master_password(parent: QWidget) -> str | None:
    pwd1, ok1 = QInputDialog.getText(parent, "Créer un coffre", "Choisis un mot de passe maître:", QLineEdit.Password)
    if not ok1 or not pwd1:
        return None
    pwd2, ok2 = QInputDialog.getText(parent, "Créer un coffre", "Confirme ton mot de passe maître:", QLineEdit.Password)
    if not ok2 or not pwd2:
        return None
    if pwd1 != pwd2:
        QMessageBox.warning(parent, "Erreur", "Les mots de passe ne correspondent pas.")
        return None
    return pwd1

def ask_entry_fields(parent: QWidget):
    # mini-dialog custom pour inclure des notes
    class D(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Nouvelle entrée")
            self.t = QLineEdit(); self.u = QLineEdit(); self.p = QLineEdit(); self.p.setEchoMode(QLineEdit.Password)
            self.n = QTextEdit()
            L = QVBoxLayout(self)
            for lab, w in [("Titre / Site:", self.t), ("Identifiant:", self.u), ("Mot de passe:", self.p), ("Notes:", self.n)]:
                L.addWidget(QLabel(lab)); L.addWidget(w)
            hb = QHBoxLayout(); b1 = QPushButton("Annuler"); b2 = QPushButton("OK"); hb.addStretch(1); hb.addWidget(b1); hb.addWidget(b2); L.addLayout(hb)
            b1.clicked.connect(self.reject); b2.clicked.connect(self.accept)
    d = D(parent)
    if d.exec():
        if not d.t.text(): return None
        return d.t.text(), d.u.text(), d.p.text(), d.n.toPlainText()
    return None
