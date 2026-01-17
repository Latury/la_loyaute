# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🦁 LA LOYAUTÉ - principal.py
# ║
# ║ 🤖 Bot Discord privé développé en Python
# ║ 👨‍💻 Développé par Latury
# ║ 📦 Version : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 📄 FICHIER : principal.py
# ║ ⚙️ MODULE : Point d'entrée principal du bot
# ║ 📝 DESCRIPTION : Initialise le logger, vérifie la configuration, crée le bot, charge les extensions et démarre le bot Discord
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15/01/2026
# ║ 🔢 VERSION : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

"""
🦁 LA LOYAUTÉ - Bot Discord privé développé par Latury
══════════════════════════════════════════════════════════════════════════════
"""

import discord
from discord.ext import commands
import asyncio
import sys
import os
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# ║ Importations des modules internes
# ╚══════════════════════════════════════════════════════════════════════════════

import configuration as config

from noyau.gestionnaire_bot import LoyauteBot
from utilitaires.logger import creer_logger

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🛠️ FONCTION 01 – initialiser_logger
# ║ 🔧 Initialise le système de logs du bot
# ╚══════════════════════════════════════════════════════════════════════════════

def initialiser_logger():
    """Initialise le système de logs du bot"""
    logger = creer_logger("principal", config.NIVEAU_LOG)
    return logger

# ═══════════════════════════════════════════════════════════════════════════════
# ║ ✅ FONCTION 02 – verifier_configuration
# ║ 🔍 Vérifie que la configuration est correcte et valide
# ╚══════════════════════════════════════════════════════════════════════════════

def verifier_configuration(logger):
    """Vérifie que la configuration est correcte"""
    # Vérification du token Discord
    if not config.DISCORD_TOKEN:
        logger.error("Le token Discord n'est pas défini dans secrets.env")
        return False

    if config.DISCORD_TOKEN == "votre_token_ici":
        logger.error("Le token Discord n'a pas été configuré dans secrets.env")
        return False

    logger.info("Configuration valide avec succès")
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🤖 FONCTION 03 – creer_bot
# ║ 🏗️ Crée et configure l'instance du bot LoyauteBot
# ╚══════════════════════════════════════════════════════════════════════════════

def creer_bot(logger):
    """Crée et configure l'instance du bot"""
    # Configuration des intents Discord
    intents = discord.Intents.default()
    for intent_name, intent_value in config.INTENTS_REQUIS.items():
        setattr(intents, intent_name, intent_value)

    # Création de l'instance du bot
    bot = LoyauteBot(
        command_prefix=config.PREFIXE_BASE,
        intents=intents,
        help_command=None,  # Désactive la commande d'aide par défaut
        logger=logger
    )

    logger.info(f"Instance du bot '{config.NOM_BOT}' créée avec succès")
    return bot

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📦 FONCTION 04 – charger_extensions
# ║ 🔄 Charge toutes les extensions (cogs) du bot
# ╚══════════════════════════════════════════════════════════════════════════════

async def charger_extensions(bot, logger):
    """Charge toutes les extensions du bot"""
    extensions = [
        # Commandes
        "commandes.commandes_admin",
        "commandes.commandes_configuration",
        "commandes.commandes_menu",
        "commandes.commandes_config_interactive",  # NOUVEAU v0.3.0
        "commandes.commandes_base",  # DOIT AVOIR UN DEVANT !

        # Événements
        "evenements.demarrage",
        "evenements.messages",
        "evenements.evenements_membres",
        "evenements.evenements_messages",
        "evenements.evenements_salons",
    ]

    for extension in extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f"Extension chargée : {extension}")
        except Exception as e:
            import traceback
            logger.error(f"Erreur lors du chargement de {extension}: {e}")
            logger.error(f"Traceback complet: {traceback.format_exc()}")
            return False

    logger.info(f"{len(extensions)} extensions chargées avec succès")
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# ║ ▶️ FONCTION 05 – demarrer_bot
# ║ 🚀 Démarre le bot Discord et gère les erreurs de connexion
# ╚══════════════════════════════════════════════════════════════════════════════

async def demarrer_bot(bot, logger):
    """Démarre le bot Discord"""
    try:
        logger.info("Connexion Discord en cours...")
        await bot.start(config.DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Échec de connexion - Token Discord invalide")
        return False
    except Exception as e:
        logger.error(f"Erreur critique lors du démarrage: {e}")
        return False
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 FONCTION 06 – main
# ║ 📋 Point d'entrée principal du programme
# ╚══════════════════════════════════════════════════════════════════════════════

async def main():
    """Point d'entrée principal du programme"""
    # Initialisation du logger
    logger = initialiser_logger()

    # Affichage du cadre de démarrage
    logger.info("╔" + "═" * 80)
    logger.info("║" + " " * 78 + "║")
    logger.info("║" + " 🦁 LA LOYAUTÉ - BOT DISCORD".center(78) + "║")
    logger.info("║" + " " * 78 + "║")
    logger.info("║" + f"Version {config.VERSION_BOT}".center(78) + "║")
    logger.info("║" + f"Développé par {config.DEVELOPPEUR}".center(78) + "║")
    logger.info("║" + " " * 78 + "║")
    logger.info("╚" + "═" * 80)

    date_demarrage = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logger.info(f"Démarrage: {date_demarrage}")

    # Vérification de la configuration
    if not verifier_configuration(logger):
        logger.error("Arrêt du programme en raison d'erreurs de configuration")
        return

    # Création de l'instance du bot
    bot = creer_bot(logger)

    # Chargement des extensions
    if not await charger_extensions(bot, logger):
        logger.error("Arrêt du programme en raison d'erreurs de chargement")
        return
    logger.info("✅ Chargement des extensions terminé")

    # Démarrage du bot
    await demarrer_bot(bot, logger)

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🚀 POINT D'ENTRÉE - Lancement du bot
# ╚══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt du bot demandé par l'utilisateur")
    except Exception as e:
        print(f"💥 Erreur fatale: {e}")
