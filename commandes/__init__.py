from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 💬 LA LOYAUTÉ - __init__.py
# ║
# ║ 🤖 Bot Discord privé développé en Python
# ║ 👨‍💻 Développé par Latury
# ║ 📦 Version : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 📄 FICHIER : __init__.py
# ║ 💬 MODULE : Initialisation du package commandes
# ║ 📝 DESCRIPTION : Expose les cogs des commandes pour l'importation
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15/01/2026
# ║ 📦 VERSION : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

from .commandes_admin import CommandesAdmin
from .commandes_configuration import CommandesConfiguration
from .commandes_menu import CommandesMenu

__all__ = [
    'CommandesAdmin',
    'CommandesConfiguration',
    'CommandesMenu',
]


