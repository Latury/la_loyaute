# ══════════════════════════════════════════════════════════════════════
# ║
# ║  🎨 LA LOYAUTÉ - COULEURS TERMINAL
# ║
# ║  Module commun pour les couleurs ANSI dans le terminal
# ║
# ║  📄 Fichier : couleurs_terminal.py
# ║  👤 Auteur : Latury
# ║  📅 Date : 13/01/2026
# ║  🔖 Version : 0.2.2
# ║
# ══════════════════════════════════════════════════════════════════════

"""Module de couleurs pour le terminal."""

class Couleurs:
    """Palette de couleurs optimisée (Bleu intense + Orange)"""

    # ── 🔵 BLEU INTENSE
    BLEU_INTENSE = "\033[1;34m"
    BLEU_TITRE = "\033[1;36m"

    # ── 🟠 ORANGE
    ORANGE = "\033[38;5;208m"
    ORANGE_CLAIR = "\033[38;5;214m"

    # ── ✅ AUTRES
    VERT = "\033[92m"
    JAUNE = "\033[93m"
    ROUGE = "\033[91m"
    GRIS = "\033[90m"

    # ── 🔧 STYLES
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
