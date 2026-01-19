# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 📨 LA LOYAUTÉ - ÉVÉNEMENTS DE MESSAGES
# ║ Discord Bot | Gestion des événements liés aux messages Discord
# ║ Développé par Latury
# ║ Version 0.2.2 (CORRIGÉ)
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 📨 FICHIER : events_messages.py
# ║ 📦 MODULE : evenements
# ║ 📝 DESCRIPTION : Gestion des événements liés aux messages Discord
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15 janvier 2026
# ║ 🔖 VERSION : 0.2.2
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from utilitaires import logs_discord

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 📦 CLASSE 01 – EventsMessages
# ║ 🎯 Cog pour gérer tous les événements liés aux messages Discord
# ╚═══════════════════════════════════════════════════════════════════════════════

class EventsMessages(commands.Cog):
    """Gestion des événements de messages Discord"""

    def __init__(self, bot):
        """
        Initialisation du cog EventsMessages

        Args:
            bot: Instance du bot Discord
        """
        self.bot = bot
        self.bot.logger.info("📨 Module EventsMessages chargé")

    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ 🗑️ FONCTION 01 – on_message_delete
    # ║ 📝 Événement déclenché lors de la suppression d'un message
    # ╚═══════════════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        Événement déclenché lors de la suppression d'un message

        Args:
            message: Message supprimé
        """
        try:
            # ── 🔹 ÉTAPE 1 : Vérification du contexte
            # Ignorer les messages en MP (pas de serveur)
            if not message.guild:
                return

            # ── 🔹 ÉTAPE 2 : Filtrage des bots
            # Ignorer les messages des bots pour éviter le spam de logs
            if message.author.bot:
                return

            # ── 🔹 ÉTAPE 3 : Log Discord
            # Envoyer un embed dans le salon de logs Discord
            await logs_discord.log_message_delete(self.bot, message)

            # ── 🔹 ÉTAPE 4 : Log console
            # Afficher l'information dans la console du bot
            channel_name = getattr(message.channel, 'name', 'Inconnu')
            contenu_apercu = message.content[:50] if message.content else "Aucun contenu"

            self.bot.logger.info(
                f"🗑️ Message supprimé | "
                f"Auteur: {message.author} | "
                f"Salon: #{channel_name} | "
                f"Contenu: {contenu_apercu}..."
            )

        except Exception as e:
            # ── ⚠️ Gestion des erreurs
            self.bot.logger.error(f"❌ Erreur dans on_message_delete : {e}")

    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ ✏️ FONCTION 02 – on_message_edit
    # ║ 📝 Événement déclenché lors de la modification d'un message
    # ╚═══════════════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """
        Événement déclenché lors de la modification d'un message

        Args:
            before: Message avant modification
            after: Message après modification
        """
        try:
            # ── 🔹 ÉTAPE 1 : Vérification du contexte
            # Ignorer les messages en MP (pas de serveur)
            if not after.guild:
                return

            # ── 🔹 ÉTAPE 2 : Filtrage des bots
            # Ignorer les messages des bots pour éviter le spam de logs
            if after.author.bot:
                return

            # ── 🔹 ÉTAPE 3 : Vérification du contenu
            # Ignorer si le contenu n'a pas changé
            # (Discord envoie parfois cet événement pour les embeds auto, etc.)
            if before.content == after.content:
                return

            # ── 🔹 ÉTAPE 4 : Log Discord
            # Envoyer un embed dans le salon de logs Discord
            await logs_discord.log_message_edit(self.bot, before, after)

            # ── 🔹 ÉTAPE 5 : Log console
            # Afficher l'information dans la console du bot
            channel_name = getattr(after.channel, 'name', 'Inconnu')

            self.bot.logger.info(
                f"✏️ Message modifié | "
                f"Auteur: {after.author} | "
                f"Salon: #{channel_name}"
            )

        except Exception as e:
            # ── ⚠️ Gestion des erreurs
            self.bot.logger.error(f"❌ Erreur dans on_message_edit : {e}")

# ═══════════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """
    Charge le cog EventsMessages dans le bot

    Args:
        bot: Instance du bot Discord
    """
    await bot.add_cog(EventsMessages(bot))

# ╔══════════════════════════════════════════════════════════════════════════════
# ║  FIN DU FICHIER events_messages.py
# ╚══════════════════════════════════════════════════════════════════════════════
