# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🦁 LA LOYAUTÉ - configuration.py
# ║
# ║ ⚙️ Bot Discord privé développé en Python
# ║ 👨‍💻 Développé par Latury
# ║ 📦 Version : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 📄 FICHIER : configuration.py
# ║ ⚙️ MODULE : Configuration centrale du bot
# ║ 📝 DESCRIPTION : Centralise toutes les variables de configuration, tokens, rôles, couleurs, intents et messages du bot
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15/01/2026
# ║ 🔢 VERSION : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

"""
🦁 LA LOYAUTÉ - Configuration centrale du bot Discord
══════════════════════════════════════════════════════════════════════════════
"""

import os
from dotenv import load_dotenv
# 🔧 Chargement des variables d'environnement depuis secrets.env

load_dotenv('secrets.env')

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔐 SECTION 01 – TOKENS & SECRETS
# ║ 🔑 Variables sensibles chargées depuis secrets.env
# ╚══════════════════════════════════════════════════════════════════════════════

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎮 SECTION 02 – CONFIGURATION DU BOT
# ║ 📋 Paramètres généraux du bot (nom, version, préfixe, debug)
# ╚══════════════════════════════════════════════════════════════════════════════

# Nom du bot
NOM_BOT = "La Loyauté"
VERSION_BOT = "0.2.2"  # Stable
DEVELOPPEUR = "Latury"

# Préfixe des commandes
PREFIXE_BASE = "!"      # Commandes publiques
PREFIXE_ADMIN = "/"     # Commandes administratives (slash commands)

# Mode debug
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 👑 SECTION 03 – RÔLES & PERMISSIONS
# ║ 🛡️ IDs des rôles et salons critiques (chargés depuis secrets.env)
# ╚══════════════════════════════════════════════════════════════════════════════

# IDs des rôles (à configurer dans secrets.env)
ROLE_ADMIN_ID = int(os.getenv('ROLE_ADMIN_ID', 0))
ROLE_MODERATEUR_ID = int(os.getenv('ROLE_MODERATEUR_ID', 0))

# ID du salon de logs Discord (0 = désactivé)
LOGS_CHANNEL_ID = int(os.getenv('LOGS_CHANNEL_ID', '0'))

# Liste des IDs utilisateurs autorisés (développeurs)
DEVELOPPEURS_IDS = [
    # Ajoute ton ID Discord ici
    # Exemple: 123456789012345678,
]

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎨 SECTION 04 – COULEURS DES EMBEDS
# ║ 🌈 Palette de couleurs pour les embeds Discord
# ╚══════════════════════════════════════════════════════════════════════════════

# Couleurs principales
COULEUR_PRINCIPALE = 0x5865F2    # Bleu Discord
COULEUR_SUCCES = 0x57F287        # Vert
COULEUR_ERREUR = 0xED4245        # Rouge
COULEUR_AVERTISSEMENT = 0xFEE75C # Jaune
COULEUR_INFO = 0x5865F2          # Bleu

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📝 SECTION 05 – CONFIGURATION DES LOGS
# ║ 🗂️ Paramètres du système de logging
# ╚══════════════════════════════════════════════════════════════════════════════

# Niveau de logs
NIVEAU_LOG = os.getenv('LOG_LEVEL', 'INFO')

# Dossier des logs
DOSSIER_LOGS = 'logs'

# Format des logs
FORMAT_LOG = '[%(asctime)s] [%(levelname)s] %(message)s'
FORMAT_DATE_LOG = '%d/%m/%Y %H:%M:%S'

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔧 SECTION 06 – PARAMÈTRES AVANCÉS
# ║ ⚙️ Intents Discord et limites système
# ╚══════════════════════════════════════════════════════════════════════════════

# Intents Discord requis
INTENTS_REQUIS = {
    'guilds': True,
    'members': True,
    'messages': True,
    'message_content': True,
    'reactions': True,
    'presences': True,
}

# Timeout pour les commandes (en secondes)
TIMEOUT_COMMANDE = 30

# Nombre maximum de messages à supprimer avec /clear
MAX_MESSAGES_CLEAR = 100

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 💬 SECTION 07 – MESSAGES DU BOT
# ║ 🗨️ Messages standards pour les réponses du bot
# ╚══════════════════════════════════════════════════════════════════════════════

# Messages d'erreur
MSG_ERREUR_PERMISSION = "🚫 Vous n'avez pas la permission d'utiliser cette commande."
MSG_ERREUR_COMMANDE = "❌ Une erreur s'est produite lors de l'exécution de la commande."
MSG_ERREUR_ARGUMENTS = "⚠️ Arguments invalides. Utilisez `!aide` pour plus d'informations."

# Messages de succès
MSG_SUCCES_COMMANDE = "✅ Commande exécutée avec succès !"

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 SECTION 08 – EMOJIS PERSONNALISÉS
# ║ 😎 Emojis utilisés dans tout le bot
# ╚══════════════════════════════════════════════════════════════════════════════

EMOJI_SUCCES = "✅"
EMOJI_ERREUR = "❌"
EMOJI_AVERTISSEMENT = "⚠️"
EMOJI_INFO = "ℹ️"
EMOJI_CHARGE = "⏳"
EMOJI_EN_LIGNE = "🟢"
EMOJI_HORS_LIGNE = "🔴"
EMOJI_ADMIN = "👑"
EMOJI_MODERATEUR = "🛡️"
EMOJI_UTILISATEUR = "👤"

# ═══════════════════════════════════════════════════════════════════════════════
# ║ ✅ FIN DU FICHIER – Configuration chargée
# ║ 📦 Toutes les variables sont maintenant disponibles globalement
# ╚══════════════════════════════════════════════════════════════════════════════
