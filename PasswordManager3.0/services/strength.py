# services/strength.py
from zxcvbn import zxcvbn

def strength(password: str) -> dict:
    """
    Retourne un dict zxcvbn: {score: 0..4, crack_time_display: str, feedback: {warning, suggestions}}
    """
    return zxcvbn(password)

def score_to_label(score: int) -> str:
    return ["Très faible", "Faible", "Moyen", "Bon", "Excellent"][max(0, min(4, score))]
