from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🦁 LA LOYAUTÉ - __init__.py
# ║
# ║ 🔧 Bot Discord privé développé en Python
# ║ 👨‍💻 Développé par Latury
# ║ 📦 Version : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

"""
🦁 LA LOYAUTÉ - Package Utilitaires
══════════════════════════════════════════════════════════════════════════════
Initialisation du package utilitaires avec exports publics
"""

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 📝 SECTION 01 – LOGGER
# ║ 📊 Imports du système de logs professionnel
# ╚═══════════════════════════════════════════════════════════════════════════════

from .logger import (
    creer_logger,
    nettoyer_anciens_logs,
    obtenir_stats_logs,
    lire_dernieres_lignes
)

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🛠️ SECTION 02 – HELPERS
# ║ 🔧 Imports des fonctions utilitaires communes
# ╚═══════════════════════════════════════════════════════════════════════════════

from .helpers import (
    formater_date,
    formater_duree,
    creer_embed,
    creer_embed_succes,
    creer_embed_erreur,
    creer_embed_avertissement,
    creer_embed_info,
    formater_nombre,
    creer_barre_progression,
    est_url_valide,
    tronquer_texte,
    obtenir_nom_affichage
)

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🎨 SECTION 03 – EMBEDS INTERACTIFS
# ║ 📋 Imports des menus et vues interactives Discord
# ╚═══════════════════════════════════════════════════════════════════════════════

from .embeds_interactifs import (
    creer_embed_menu_principal,
    VueMenuPrincipal
)

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📦 EXPORTS PUBLICS
# ║ 🔗 Tous les exports disponibles du package utilitaires
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Logger
    'creer_logger',
    'nettoyer_anciens_logs',
    'obtenir_stats_logs',
    'lire_dernieres_lignes',

    # Helpers
    'formater_date',
    'formater_duree',
    'creer_embed',
    'creer_embed_succes',
    'creer_embed_erreur',
    'creer_embed_avertissement',
    'creer_embed_info',
    'formater_nombre',
    'creer_barre_progression',
    'est_url_valide',
    'tronquer_texte',
    'obtenir_nom_affichage',

    # Embeds Interactifs
    'creer_embed_menu_principal',
    'VueMenuPrincipal',
]

# ═══════════════════════════════════════════════════════════════════════════════
# ║ ✅ FIN DU FICHIER – Package utilitaires initialisé
# ╚═══════════════════════════════════════════════════════════════════════════════
