# ═══════════════════════════════════════════════════════════════════════════════
# ║                                                                             
# ║  🛡️  LA LOYAUTÉ - CONFIGURATION CENTRALE
# ║
# ║  Fichier de configuration principal du bot Discord
# ║  Développé par Latury
# ║  Version : 0.1.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv('secrets.env')

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔐 TOKENS & SECRETS
# ═══════════════════════════════════════════════════════════════════════════════

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎮 CONFIGURATION DU BOT
# ═══════════════════════════════════════════════════════════════════════════════

# Nom du bot
NOM_BOT = "La Loyauté"
VERSION_BOT = "0.1.0"
DEVELOPPEUR = "Latury"

# Prefix des commandes
PREFIX_BASE = "!"       # Commandes publiques
PREFIX_ADMIN = "/"      # Commandes administratives (slash commands)

# Mode debug
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 👑 RÔLES & PERMISSIONS
# ═══════════════════════════════════════════════════════════════════════════════

# IDs des rôles (à configurer dans secrets.env)
ROLE_ADMIN_ID = int(os.getenv('ROLE_ADMIN_ID', 0))
ROLE_MODERATEUR_ID = int(os.getenv('ROLE_MODERATEUR_ID', 0))

# Liste des IDs utilisateurs autorisés (développeurs)
DEVELOPPEURS_IDS = [
    # Ajoute ton ID Discord ici
]

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎨 COULEURS DES EMBEDS
# ═══════════════════════════════════════════════════════════════════════════════

# Couleurs principales
COULEUR_PRINCIPALE = 0x5865F2    # Bleu Discord
COULEUR_SUCCES = 0x57F287        # Vert
COULEUR_ERREUR = 0xED4245        # Rouge
COULEUR_AVERTISSEMENT = 0xFEE75C # Jaune
COULEUR_INFO = 0x5865F2          # Bleu

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📝 CONFIGURATION DES LOGS
# ═══════════════════════════════════════════════════════════════════════════════

# Niveau de logs
NIVEAU_LOG = os.getenv('LOG_LEVEL', 'INFO')

# Dossier des logs
DOSSIER_LOGS = 'logs'

# Format des logs
FORMAT_LOG = '[%(asctime)s] [%(levelname)s] %(message)s'
FORMAT_DATE_LOG = '%d/%m/%Y %H:%M:%S'

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔧 PARAMÈTRES AVANCÉS
# ═══════════════════════════════════════════════════════════════════════════════

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
# ║ 📊 MESSAGES DU BOT
# ═══════════════════════════════════════════════════════════════════════════════

# Messages d'erreur
MSG_ERREUR_PERMISSION = "🚫 Vous n'avez pas la permission d'utiliser cette commande."
MSG_ERREUR_COMMANDE = "❌ Une erreur s'est produite lors de l'exécution de la commande."
MSG_ERREUR_ARGUMENTS = "⚠️ Arguments invalides. Utilisez `!aide` pour plus d'informations."

# Messages de succès
MSG_SUCCES_COMMANDE = "✅ Commande exécutée avec succès !"

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 EMOJIS PERSONNALISÉS
# ═══════════════════════════════════════════════════════════════════════════════

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
