from __future__ import annotations

# ══════════════════════════════════════════════════════════════════════
# ║
# ║  🔧 LA LOYAUTÉ - Module Utilitaires
# ║
# ║  Initialisation du package utilitaires
# ║
# ║  📄 Fichier : utilitaires/__init__.py
# ║  👤 Auteur : Latury
# ║  📅 Date : 06/01/2026
# ║  🔖 Version : 0.3.0
# ║
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# ║ 📊 IMPORTS - LOGGER
# ══════════════════════════════════════════════════════════════════════

from .logger import (
    creer_logger,
    nettoyer_anciens_logs,
    obtenir_stats_logs,
    lire_dernieres_lignes
)

# ══════════════════════════════════════════════════════════════════════
# ║ 🛠️ IMPORTS - HELPERS
# ══════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════
# ║ 🎨 IMPORTS - EMBEDS INTERACTIFS (v0.3.0)
# ══════════════════════════════════════════════════════════════════════

from .embeds_interactifs import (
    creer_embed_menu_principal,
    VueMenuPrincipal
)

# ══════════════════════════════════════════════════════════════════════
# ║ 📦 EXPORTS PUBLICS
# ══════════════════════════════════════════════════════════════════════

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

    # Embeds Interactifs (v0.3.0)
    'creer_embed_menu_principal',
    'VueMenuPrincipal'
]

