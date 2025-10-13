# services/clipboard.py

from PySide6.QtGui import QGuiApplication, QClipboard
from PySide6.QtCore import QTimer

def copy_with_timeout(text: str, timeout_seconds: int = 20):
    """
    Copie dans le presse-papiers via Qt et efface après timeout_seconds.
    """
    cb = QGuiApplication.clipboard()
    cb.setText(text, mode=QClipboard.Clipboard)

    # (Optionnel) aussi la "selection" primaire sous X11
    try:
        cb.setText(text, mode=QClipboard.Selection)
    except Exception:
        pass

    # Effacer après le délai
    def clear():
        cb.setText("", mode=QClipboard.Clipboard)
        try:
            cb.setText("", mode=QClipboard.Selection)
        except Exception:
            pass

    QTimer.singleShot(timeout_seconds * 1000, clear)
