from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# ║  💬 LA LOYAUTÉ - Module Commandes
# ║  Initialisation du package commandes
# ═══════════════════════════════════════════════════════════════════════════════

# from .commandes_base import CommandesBase  # ← Commenté
from .commandes_admin import CommandesAdmin
from .commandes_configuration import CommandesConfiguration
from .commandes_menu import CommandesMenu

__all__ = [
    # 'CommandesBase',  # ← COMMENTE CETTE LIGNE AUSSI !
    'CommandesAdmin',
    'CommandesConfiguration',
    'CommandesMenu',
]


