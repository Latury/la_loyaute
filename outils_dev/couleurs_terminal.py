# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🎨 LA LOYAUTÉ - COULEURS TERMINAL
# ║ Outils Dev | Module commun pour les couleurs ANSI dans le terminal
# ║ Développé par Latury
# ║ Version 0.2.2
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🎨 FICHIER : couleurs_terminal.py
# ║ 📦 MODULE : outils_dev
# ║ 📝 DESCRIPTION : Module commun pour les couleurs ANSI dans le terminal
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15 janvier 2026
# ║ 🔖 VERSION : 0.2.2
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

"""Module de couleurs pour le terminal."""

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🎨 CLASSE 01 – Couleurs
# ║ 📝 Palette de couleurs optimisée (Bleu intense + Orange)
# ╚═══════════════════════════════════════════════════════════════════════════════

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


# ╔══════════════════════════════════════════════════════════════════════════════
# ║
# ╚══════════════════════════════════════════════════════════════════════════════
