# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🛡️ LA LOYAUTÉ - POINT D'ENTRÉE PRINCIPAL
# ║
# ║ Bot Discord privé développé en Python
# ║ Développé par Latury
# ║ Version : 0.2.1
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
import asyncio
import sys
import os
from datetime import datetime

# Importation de la configuration
import configuration as config

# Importation des gestionnaires
from noyau.gestionnaire_bot import LoyauteBot
from utilitaires.logger import creer_logger


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🚀 FONCTION 01 – Initialisation du logger
# ║ Description : Configure le système de logs avant le démarrage
# ╚══════════════════════════════════════════════════════════════════════════════

def initialiser_logger():
    """Initialise le système de logs du bot"""
    return creer_logger('principal', config.NIVEAU_LOG)


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 FONCTION 02 – Vérification de la configuration
# ║ Description : Vérifie que toutes les variables obligatoires sont définies
# ╚══════════════════════════════════════════════════════════════════════════════

def verifier_configuration(logger):
    """Vérifie que la configuration est correcte"""
    # ── 🔹 Vérification du token Discord
    if not config.DISCORD_TOKEN:
        logger.error("❌ Le token Discord n'est pas défini dans secrets.env")
        return False

    # ── 🔹 Vérification de la validité du token
    if config.DISCORD_TOKEN == "votre_token_ici":
        logger.error("❌ Le token Discord n'a pas été configuré dans secrets.env")
        return False

    logger.info("✅ Configuration validée avec succès")
    return True


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🏗️ FONCTION 03 – Création de l'instance du bot
# ║ Description : Instancie le bot avec les intents et la configuration
# ╚══════════════════════════════════════════════════════════════════════════════

def creer_bot(logger):
    """Crée et configure l'instance du bot"""
    # ── 🔹 Configuration des intents Discord
    intents = discord.Intents.default()
    for intent_name, intent_value in config.INTENTS_REQUIS.items():
        setattr(intents, intent_name, intent_value)

    # ── 🔹 Création de l'instance du bot
    bot = LoyauteBot(
        command_prefix=config.PREFIX_BASE,
        intents=intents,
        help_command=None,  # Désactive la commande d'aide par défaut
        logger=logger
    )

    logger.info(f"🤖 Instance du bot '{config.NOM_BOT}' créée avec succès")
    return bot


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📦 FONCTION 04 – Chargement des extensions
# ║ Description : Charge tous les cogs (commandes, événements)
# ╚══════════════════════════════════════════════════════════════════════════════

async def charger_extensions(bot, logger):
    """Charge toutes les extensions du bot"""
    extensions = [
        # ── 📝 COMMANDES
        'commandes.commandes_base',
        'commandes.commandes_admin',
        'commandes.commandes_configuration',  # ← NOUVEAU (v0.2.1)

        # ── 🎉 ÉVÉNEMENTS
        'evenements.demarrage',
        'evenements.messages',
        'evenements.events_membres',
        'evenements.events_messages',         # ← NOUVEAU (v0.2.1)
        'evenements.events_salons',           # ← NOUVEAU (v0.2.1)
    ]

    # ── 🔹 Chargement de chaque extension
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f"📦 Extension chargée : {extension}")
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement de {extension} : {e}")
            return False

    logger.info(f"✅ {len(extensions)} extensions chargées avec succès")
    return True


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🎬 FONCTION 05 – Démarrage du bot
# ║ Description : Lance le bot et gère les erreurs de connexion
# ╚══════════════════════════════════════════════════════════════════════════════

async def demarrer_bot(bot, logger):
    """Démarre le bot Discord"""
    try:
        # ── 🔹 Connexion au serveur Discord
        logger.info("🔌 Connexion à Discord en cours...")
        await bot.start(config.DISCORD_TOKEN)

    except discord.LoginFailure:
        logger.error("❌ Échec de connexion : Token Discord invalide")
        return False

    except Exception as e:
        logger.error(f"❌ Erreur critique lors du démarrage : {e}")
        return False

    return True


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 FONCTION 06 – Point d'entrée principal
# ║ Description : Fonction principale qui orchestre le démarrage
# ╚══════════════════════════════════════════════════════════════════════════════

async def main():
    """Point d'entrée principal du programme"""
    # ── 🔹 Initialisation du logger
    logger = initialiser_logger()

    # ── 🔹 Affichage du cadre de démarrage
    logger.info("═" * 80)
    logger.info("║" + " " * 78 + "║")
    logger.info("║" + f"🛡️ LA LOYAUTÉ - BOT DISCORD".center(78) + "║")
    logger.info("║" + " " * 78 + "║")
    logger.info("║" + f"Version : {config.VERSION_BOT}".center(78) + "║")
    logger.info("║" + f"Développé par {config.DEVELOPPEUR}".center(78) + "║")
    logger.info("║" + " " * 78 + "║")
    logger.info("═" * 80)

    # ── 🔹 Affichage de la date et heure de démarrage
    date_demarrage = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    logger.info(f"📅 Démarrage : {date_demarrage}")
    logger.info("")

    # ── 🔹 Vérification de la configuration
    if not verifier_configuration(logger):
        logger.error("🛑 Arrêt du programme en raison d'erreurs de configuration")
        return

    # ── 🔹 Création de l'instance du bot
    bot = creer_bot(logger)

    # ── 🔹 Chargement des extensions
    if not await charger_extensions(bot, logger):
        logger.error("🛑 Arrêt du programme en raison d'erreurs de chargement")
        return

    logger.info("")

    # ── 🔹 Démarrage du bot
    await demarrer_bot(bot, logger)


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🚀 LANCEMENT DU PROGRAMME
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        # Lancement de la boucle asynchrone
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du bot demandé par l'utilisateur")

    except Exception as e:
        print(f"\n\n❌ Erreur fatale : {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# FIN DU FICHIER principal.py
# ═══════════════════════════════════════════════════════════════════════════════
