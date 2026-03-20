# UI/main_window.py

from __future__ import annotations
from PySide6.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout, QListWidget,
                               QToolBar, QMessageBox, QListWidgetItem, QLineEdit,
                               QFileDialog, QTreeWidget, QTreeWidgetItem)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QTimer, QObject, QEvent
from platformdirs import user_data_dir
import os, secrets, string

from core.vault import Vault
from core.models import Entry
from .dialogs import ask_master_password, ask_new_master_password, ask_entry_fields
from services.clipboard import copy_with_timeout
from UI.generator_dialog import GeneratorDialog
from UI.edit_dialog import EditEntryDialog


APP_NAME = "PassMan" ; APP_AUTHOR = "ChatSnowGPT"

def default_vault_path() -> str:
    base = user_data_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "vault.cbor.vault")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PassMan")
        self.resize(900, 560)
        self.vault_path = default_vault_path()
        self.vault = Vault(self.vault_path)

        self.list = QTreeWidget()
        self.list.setColumnCount(3)
        self.list.setHeaderLabels(["Titre/Site", "Identifiant", "Modifié le"])
        self.list.setAlternatingRowColors(True)
        self.list.setRootIsDecorated(False)
        self.list.setSortingEnabled(True)
        self.list.itemActivated.connect(self.copy_password)

        # --- MAIN LAYOUT --- 
        central = QWidget(self)
        layout = QVBoxLayout(central)
        self.search = QLineEdit()

        self.search.setPlaceholderText("Rechercher (titre, identifiant)…")
        self.search.textChanged.connect(self.refresh_list)
        layout.addWidget(self.search)
        layout.addWidget(self.list)


        self.setCentralWidget(central)
        self.AUTOLOCK_MINUTES = 5 
        self.idle_timer = QTimer(self)
        self.idle_timer.setInterval(self.AUTOLOCK_MINUTES * 60 * 1000)
        self.idle_timer.timeout.connect(self.lock_vault)
        self.installEventFilter(self) 
        self._arm_idle_timer()


        # --- TOOLBAR ---
        tb = QToolBar("Actions", self)
        self.addToolBar(tb)
        self.act_unlock = QAction("Déverouiller", self)
        self.act_add = QAction("Ajouter", self)
        self.act_del = QAction("Supprimer", self)
        self.act_edit = QAction("Modifier", self)
        self.act_copy = QAction("Copier MDP", self)
        self.act_gen = QAction("Générer", self)
        self.act_lock = QAction("Verrouiller", self)

        for a in [self.act_unlock, self.act_add, self.act_del, self.act_edit, self.act_copy, self.act_gen, self.act_lock]:
            tb.addAction(a)

        self.act_sort_title = QAction("Trier par titre", self)
        self.act_sort_user = QAction("Trier par identifiant", self)
        self.act_sort_date = QAction("Trier par date", self)
        tb.addAction(self.act_sort_title); tb.addAction(self.act_sort_user); tb.addAction(self.act_sort_date)


        # --- KEYBOARD SHORTCUTS ---
        self.act_add.setShortcut("Ctrl+N")
        self.act_edit.setShortcut("Ctrl+E")
        self.act_del.setShortcut("Del")
        self.act_copy.setShortcut("Ctrl+C")
        self.act_lock.setShortcut("Ctrl+L")
        
        
        self.search.setClearButtonEnabled(True)
        self.search.setPlaceholderText("Rechercher (Ctrl+F)…")
        find_action = QAction(self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(lambda: (self.search.setFocus(), self.search.selectAll()))
        self.addAction(find_action)


        # --- CONNEXIONS --- 
        self.act_unlock.triggered.connect(self.unlock_flow)
        self.act_add.triggered.connect(self.add_entry)
        self.act_del.triggered.connect(self.delete_selected)
        self.act_edit.triggered.connect(self.edit_selected)
        self.act_copy.triggered.connect(self.copy_password)
        self.act_gen.triggered.connect(self.generate_and_copy)
        self.act_lock.triggered.connect(self.lock_vault)

        self.act_sort_title.triggered.connect(lambda: self.list.sortItems(0, Qt.AscendingOrder))
        self.act_sort_user.triggered.connect(lambda: self.list.sortItems(1, Qt.AscendingOrder))
        self.act_sort_date.triggered.connect(lambda: self.list.sortItems(2, Qt.DescendingOrder))

        # Première fois ? Propose de créer un coffre
        if not self.vault.exists():
            self.first_time_create()


        # --- ACTIONS ---
    def first_time_create(self):
        pwd = ask_new_master_password(self)
        if not pwd:
            QMessageBox.information(self, "Info", "Aucun coffre créé.")
            return
        self.vault.create(pwd)
        QMessageBox.information(self, "OK", "Coffre créé. Garde bien ton mot de passe maître.")


    def unlock_flow(self):
        if self.vault.is_unlocked:
            QMessageBox.information(self, "Info", "Déjà déverrouillé.")
            return
        if not self.vault.exists():
            self.first_time_create(); return
        pwd = ask_master_password(self)
        if not pwd: return
        try:
            self.vault.unlock(pwd)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de déverrouiller : {e}")
            return
        self.refresh_list()
        self._arm_idle_timer()


    def lock_vault(self):
        self.idle_timer.stop()
        if not self.vault.is_unlocked: return
        self.vault.lock(); self.list.clear()
        QMessageBox.information(self, "Verrouillé", "Coffre verrouillé.")


    def refresh_list(self):
        self.list.clear()
        if not self.vault.is_unlocked:
            return
        q = (self.search.text() or "").lower() if hasattr(self, "search") else ""
        for e in self.vault.list_entries():
            if q and (q not in e.title.lower() and q not in e.username.lower()):
                continue
            it = QTreeWidgetItem([e.title, e.username, (e.updated_at or e.created_at or "")])
            it.setData(0, Qt.UserRole, e.id)  # stocker l'id sur la 1ère colonne
            self.list.addTopLevelItem(it)
        self.list.sortItems(0, Qt.AscendingOrder)


    def add_entry(self):
        if not self.vault.is_unlocked:
            self.unlock_flow()
            if not self.vault.is_unlocked: return
        fields = ask_entry_fields(self)
        if not fields: return
        if len(fields) == 4:
            title, username, password, notes = fields
        else:
            title, username, password = fields; notes = ""
        self.vault.add_entry(Entry.new(title, username, password, notes))
        self.refresh_list()


    def delete_selected(self):
        if not self.vault.is_unlocked: return
        item = self.list.currentItem()
        if not item: return
        entry_id = item.data(0, Qt.UserRole)
        self.vault.delete_entry(entry_id)
        self.refresh_list()

    def edit_selected(self):
        if not self.vault.is_unlocked:
            return
        item = self.list.currentItem()
        if not item:
            return
        entry_id = item.data(0, Qt.UserRole)
        e = next((x for x in self.vault.entries if x.id == entry_id), None)
        if not e:
            return

        dlg = EditEntryDialog(self, title=e.title, username=e.username, password=e.password, notes=e.notes)
        if dlg.exec():
            vals = dlg.values()
            # validation minimale
            if not vals["title"]:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Erreur", "Le titre est obligatoire.")
                return
            self.vault.update_entry(entry_id, **vals)
            self.refresh_list()


    def copy_password(self):
        if not self.vault.is_unlocked: return
        item = self.list.currentItem()
        if not item: return
        entry_id = item.data(0, Qt.UserRole)
        entry = next((e for e in self.vault.entries if e.id == entry_id), None)
        if not entry: return
        copy_with_timeout(entry.password, 20)
        QMessageBox.information(self, "Copié", "Mot de passe copié (effacé du presse-papiers dans 20s).")


    def generate_and_copy(self):
        dlg = GeneratorDialog(self)
        if dlg.exec():  # l'utilisateur a cliqué OK
            # Option: si le coffre est déverrouillé, proposer d'ajouter directement l'entrée
            # ici on copie juste le résultat
            from services.clipboard import copy_with_timeout
            copy_with_timeout(dlg.out.text(), 30)


    def _arm_idle_timer(self):
        self.idle_timer.start()


    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        # Dès qu'il y a une activité clavier/souris, on réarme
        if event.type() in (QEvent.MouseMove, QEvent.MouseButtonPress,
                            QEvent.KeyPress, QEvent.Wheel):
            if self.vault.is_unlocked:
                self._arm_idle_timer()
        return super().eventFilter(obj, event)
    
    def _context_menu(self, pos):
        item = self.list.itemAt(pos)
        if not item: return
        entry_id = item.data(Qt.UserRole)
        from PySide6.QtWidgets import QMenu
        m = QMenu(self)
        act_copy = m.addAction("Copier le mot de passe")
        act_edit = m.addAction("Modifier…")
        act_del  = m.addAction("Supprimer")
        chosen = m.exec(self.list.mapToGlobal(pos))
        if chosen == act_copy:
            self.copy_password()
        elif chosen == act_edit:
            self.edit_selected()
        elif chosen == act_del:
            self.delete_selected()

