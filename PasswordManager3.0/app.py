# app.py 

"MDP maître: TonMotdePasseSuperSecretIci"

from PySide6.QtWidgets import QApplication
from UI.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
