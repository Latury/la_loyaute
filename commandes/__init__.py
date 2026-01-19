# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🦁 LA LOYAUTÉ - commandes/__init__.py
# ║
# ║ 📦 Initialisation du package commandes
# ║ 👨💻 Développé par Latury
# ║
# ═══════════════════════════════════════════════════════════════════════════════

"""
📦 Package contenant toutes les commandes du bot
══════════════════════════════════════════════════════════════════════════════
"""

# Imports des commandes disponibles
try:
    from .commandes_configuration import CommandesConfiguration
except ImportError:
    CommandesConfiguration = None

try:
    from .commandes_bienvenue import CommandesBienvenue
except ImportError:
    CommandesBienvenue = None

try:
    from .commandes_menu import CommandesMenu
except ImportError:
    CommandesMenu = None

# ⚠️ TEMPORAIREMENT DÉSACTIVÉ - À CORRIGER
# try:
#     from .commandes_interface import CommandesInterface
# except ImportError:
#     CommandesInterface = None

CommandesInterface = None  # ⚠️ Placeholder temporaire

# Liste des exports
__all__ = [
    'CommandesConfiguration',
    'CommandesBienvenue',
    'CommandesMenu',
    # 'CommandesInterface'  # ⚠️ Désactivé temporairement
]
