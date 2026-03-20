# ui/generator_dialog.py
from __future__ import annotations
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QSpinBox, QCheckBox, QPushButton, QRadioButton, QProgressBar
                               )
from PySide6.QtCore import Qt
import secrets, string

from services.strength import strength, score_to_label

# petite liste interne pour passphrases
DEFAULT_WORDS = [
    "lune","pierre","tigre","mer","forêt","orange","neon","pixel","delta","vortex",
    "brise","astro","kilo","sigma","quartz","cobra","opera","ninja","python","foudre"
]

class GeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Générateur")

        # widgets
        self.out = QLineEdit(); self.out.setEchoMode(QLineEdit.Password)
        self.btn_show = QCheckBox("Afficher")

        # mode
        self.rb_pwd = QRadioButton("Mot de passe"); self.rb_pwd.setChecked(True)
        self.rb_phrase = QRadioButton("Passphrase")

        # options mot de passe
        self.spin_len = QSpinBox(); self.spin_len.setRange(8, 128); self.spin_len.setValue(20)
        self.cb_lower = QCheckBox("a-z"); self.cb_lower.setChecked(True)
        self.cb_upper = QCheckBox("A-Z"); self.cb_upper.setChecked(True)
        self.cb_digits = QCheckBox("0-9"); self.cb_digits.setChecked(True)
        self.cb_symbols = QCheckBox("Symboles"); self.cb_symbols.setChecked(True)
        self.cb_ambig = QCheckBox("Éviter ambigus (l/1, O/0)"); self.cb_ambig.setChecked(False)

        # options passphrase
        self.spin_words = QSpinBox(); self.spin_words.setRange(3, 12); self.spin_words.setValue(5)
        self.sep = QLineEdit("-"); self.sep.setMaxLength(3)

        # score
        self.meter = QProgressBar(); self.meter.setRange(0, 4); self.lbl_score = QLabel("Score : –")

        # boutons
        self.btn_generate = QPushButton("Générer")
        self.btn_copy = QPushButton("Copier")
        self.btn_ok = QPushButton("OK"); self.btn_ok.setDefault(True)

        # layout
        L = QVBoxLayout(self)
        L.addWidget(self.rb_pwd); L.addWidget(self.rb_phrase)

        row_len = QHBoxLayout(); row_len.addWidget(QLabel("Longueur:")); row_len.addWidget(self.spin_len)
        row_words = QHBoxLayout(); row_words.addWidget(QLabel("Mots:")); row_words.addWidget(self.spin_words)
        row_sep = QHBoxLayout(); row_sep.addWidget(QLabel("Séparateur:")); row_sep.addWidget(self.sep)

        L.addLayout(row_len)
        L.addWidget(self.cb_lower); L.addWidget(self.cb_upper); L.addWidget(self.cb_digits)
        L.addWidget(self.cb_symbols); L.addWidget(self.cb_ambig)
        L.addLayout(row_words); L.addLayout(row_sep)

        L.addWidget(QLabel("Résultat:"))
        L.addWidget(self.out)
        L.addWidget(self.btn_show)

        row_score = QHBoxLayout(); row_score.addWidget(self.lbl_score); row_score.addWidget(self.meter)
        L.addLayout(row_score)

        row_btns = QHBoxLayout(); row_btns.addWidget(self.btn_generate); row_btns.addWidget(self.btn_copy); row_btns.addStretch(1); row_btns.addWidget(self.btn_ok)
        L.addLayout(row_btns)

        # connexions
        self.btn_generate.clicked.connect(self.generate)
        self.btn_copy.clicked.connect(self.copy_out)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_show.stateChanged.connect(self.toggle_echo)
        self.out.textChanged.connect(self.update_score)

        # état initial
        self.generate()

    def toggle_echo(self, _):
        self.out.setEchoMode(QLineEdit.Normal if self.btn_show.isChecked() else QLineEdit.Password)

    def copy_out(self):
        try:
            import pyperclip
            pyperclip.copy(self.out.text())
        except Exception:
            pass

    def _rand_password(self) -> str:
        alphabet = ""
        if self.cb_lower.isChecked(): alphabet += string.ascii_lowercase
        if self.cb_upper.isChecked(): alphabet += string.ascii_uppercase
        if self.cb_digits.isChecked(): alphabet += string.digits
        if self.cb_symbols.isChecked(): alphabet += "!@#$%^&*()-_=+[]{};:,.?/"

        if self.cb_ambig.isChecked():
            for ch in "l1I|O0":
                alphabet = alphabet.replace(ch, "")
        if not alphabet:
            alphabet = string.ascii_letters + string.digits

        n = self.spin_len.value()
        return "".join(secrets.choice(alphabet) for _ in range(n))

    def _rand_passphrase(self) -> str:
        words = DEFAULT_WORDS
        n = self.spin_words.value()
        sep = self.sep.text() or "-"
        return sep.join(secrets.choice(words) for _ in range(n))

    def generate(self):
        if self.rb_phrase.isChecked():
            pwd = self._rand_passphrase()
        else:
            pwd = self._rand_password()
        self.out.setText(pwd)
        self.update_score()

    def update_score(self):
        pw = self.out.text()
        if not pw:
            self.meter.setValue(0); self.lbl_score.setText("Score : –"); return
        data = strength(pw); sc = int(data["score"])
        self.meter.setValue(sc)
        self.lbl_score.setText(f"Score : {score_to_label(sc)} — {data['crack_times_display']['offline_fast_hashing_1e10_per_second']}")
