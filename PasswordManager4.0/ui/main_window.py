#ui/main_window.py

"""
    Fenêtre principal
"""

# ----- IMPORTS ----- 
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtWidgets      import (
    QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QPushButton, QLineEdit,
    QListWidget, QInputDialog, QApplication
)
from PySide6.QtCore         import Qt

from ui.theme               import *
from core.models            import Entry


class MainWindow(QMainWindow):
    def __init__(self, vault):
        super().__init__()
        self.vault = vault
        self.setWindowTitle("Pandora")
        self.setMinimumSize(900, 600)
        self.resize(900, 600)
        self.setStyleSheet(f"background-color: {BG_DEEP};")
    
        # Widget Central
        central = QWidget()
        central.setStyleSheet(f"background-color: {BG_DEEP};")
        self.setCentralWidget(central)

        # layout
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(160)
        sidebar.setStyleSheet(f"background-color: {BG_DARK}; border-right: 1px solid {BORDER};")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 16, 8, 16)
        sidebar_layout.setSpacing(2)

       
        def make_side_btn(text, active=False):
            btn = QPushButton(text)
            btn.setFlat(True)
            btn.setFixedHeight(28)
            btn.setCursor(Qt.PointingHandCursor)
            color = VIOLET_LT if active else TEXT_MUT
            bg = f"background-color: {BG_HOVER};" if active else "background: transparent;"
            btn.setStyleSheet(f"""
                QPushButton {{
                    {bg}
                    color: {color};
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                    text-align: left;
                    padding: 0 8px;
                }}
                QPushButton:hover {{
                    background-color: {BG_HOVER};
                    color: {VIOLET_LT};
                }}
            """)
            return btn
        
        # Boutons 
        sidebar_layout.addWidget(make_side_btn("Tout", active=True))
        sidebar_layout.addWidget(make_side_btn("Favoris"))
        sidebar_layout.addWidget(make_side_btn("Réseaux"))
        sidebar_layout.addWidget(make_side_btn("Banque"))

        sidebar_layout.addStretch()

        btn_lock = make_side_btn("Verrouiller")
        btn_lock.setStyleSheet(btn_lock.styleSheet().replace(TEXT_MUT, DANGER))
        sidebar_layout.addWidget(btn_lock)

        main_layout.addWidget(sidebar)

        # ----- ZONE CONTENU -----
        content = QWidget()
        content.setStyleSheet(f"background-color: {BG_DEEP};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        main_layout.addWidget(content)

        # ----- TOPBAR -----
        topbar = QWidget()
        topbar.setFixedHeight(52)
        topbar.setStyleSheet(f"background-color: {BG_DARK}; border-bottom: 1px solid {BORDER};")

        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(16, 0, 16, 0)
        topbar_layout.setSpacing(10)

        # Champ de recherche
        self.search = QLineEdit()
        self.search.setPlaceholderText("Rechercher...")
        self.search.setFixedHeight(32)
        self.search.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_LT};
                border-radius: 6px;
                color: {TEXT_PRI};
                font-size: 13px;
                padding: 0 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {VIOLET};
            }}
        """)

        # Bouton Ajouter
        self.btn_add = QPushButton("+ Ajouter")
        self.btn_add.setFixedSize(100, 32)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setStyleSheet(f"""
            QPushButton {{
                background-color: {VIOLET};
                color: {VIOLET_XLT};
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: #6d28d9; }}
            QPushButton:pressed {{ background-color: #5b21b6; }}
        """)

        topbar_layout.addWidget(self.search)
        topbar_layout.addWidget(self.btn_add)

        content_layout.addWidget(topbar)
        

        # ----- LISTE DES ENTRÉES -----
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {BG_DEEP};
                border: none;
                padding: 8px;
            }}
            QListWidget::item {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER};
                border-radius: 6px;
                color: {TEXT_PRI};
                font-size: 13px;
                padding: 10px 12px;
                margin-bottom: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {BG_HOVER};
                border: 1px solid {VIOLET};
                color: {VIOLET_XLT};
            }}
            QListWidget::item:hover {{
                background-color: {BG_HOVER};
                border: 1px solid {BORDER_LT};
            }}
        """)

        content_layout.addWidget(self.list_widget)

        # Connections
        self.btn_add.clicked.connect(self._on_add)
        btn_lock.clicked.connect(self._on_lock)
        self.search.textChanged.connect(self._on_search)
        
        self.refresh_list()


    def refresh_list(self):
        if self.vault is None:
            return 
        
        self.list_widget.clear()
        entries = self.vault.list_entries()
        for entry in entries:
            self.list_widget.addItem(f"{entry.title} - {entry.username}")

    def _on_lock(self):
        self.vault.lock()
        self.close()
        # TODO: rouvrir LoginWindow

    def _on_search(self, query):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(query.lower() not in item.text().lower())

    def _on_add(self):
        if self.vault is None:
            return

        title, ok = QInputDialog.getText(self, "Nouvelle entrée", "Titre / Site :")
        if not ok or not title:
            return

        username, ok = QInputDialog.getText(self, "Nouvelle entrée", "Identifiant :")
        if not ok:
            return

        password, ok = QInputDialog.getText(self, "Nouvelle entrée", "Mot de passe :")
        if not ok:
            return

        self.vault.add_entry(Entry.new(title, username, password))
        self.refresh_list()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(vault=None)
    win.show()
    sys.exit(app.exec())