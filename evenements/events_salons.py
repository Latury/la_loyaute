# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🏗️ LA LOYAUTÉ - ÉVÉNEMENTS DE SALONS
# ║ Discord Bot | Gestion des événements liés aux salons Discord
# ║ Développé par Latury
# ║ Version 0.2.2 (CORRIGÉ)
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from utilitaires import logs_discord

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 📦 CLASSE 01 – EventsSalons
# ║ 🎯 Cog pour gérer tous les événements liés aux salons Discord
# ╚═══════════════════════════════════════════════════════════════════════════════

class EventsSalons(commands.Cog):
    """Gestion des événements de salons Discord"""

    def __init__(self, bot):
        """
        Initialisation du cog EventsSalons

        Args:
            bot: Instance du bot Discord
        """
        self.bot = bot
        self.bot.logger.info("🏗️ Module EventsSalons chargé")

    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ 🏗️ FONCTION 01 – on_guild_channel_create
    # ║ 📝 Événement déclenché lors de la création d'un salon
    # ╚═══════════════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """
        Événement déclenché lors de la création d'un salon

        Args:
            channel: Salon créé (TextChannel, VoiceChannel, CategoryChannel, etc.)
        """
        try:
            # ── 🔹 ÉTAPE 1 : Log Discord
            # Envoyer un embed dans le salon de logs Discord
            await logs_discord.log_channel_create(self.bot, channel)

            # ── 🔹 ÉTAPE 2 : Détermination du type de salon
            channel_type = {
                discord.ChannelType.text: "Textuel",
                discord.ChannelType.voice: "Vocal",
                discord.ChannelType.category: "Catégorie",
                discord.ChannelType.news: "Annonces",
                discord.ChannelType.forum: "Forum",
            }.get(channel.type, "Autre")

            # ── 🔹 ÉTAPE 3 : Log console
            # Afficher l'information dans la console du bot
            channel_name = getattr(channel, 'name', 'Inconnu')
            self.bot.logger.info(
                f"🏗️ Salon créé | "
                f"Nom: #{channel_name} | "
                f"Type: {channel_type} | "
                f"ID: {channel.id}"
            )

        except Exception as e:
            # ── ⚠️ Gestion des erreurs
            self.bot.logger.error(f"❌ Erreur dans on_guild_channel_create : {e}")

    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ 🗑️ FONCTION 02 – on_guild_channel_delete
    # ║ 📝 Événement déclenché lors de la suppression d'un salon
    # ╚═══════════════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """
        Événement déclenché lors de la suppression d'un salon

        Args:
            channel: Salon supprimé (TextChannel, VoiceChannel, CategoryChannel, etc.)
        """
        try:
            # ── 🔹 ÉTAPE 1 : Log Discord
            # Envoyer un embed dans le salon de logs Discord
            await logs_discord.log_channel_delete(self.bot, channel)

            # ── 🔹 ÉTAPE 2 : Détermination du type de salon
            channel_type = {
                discord.ChannelType.text: "Textuel",
                discord.ChannelType.voice: "Vocal",
                discord.ChannelType.category: "Catégorie",
                discord.ChannelType.news: "Annonces",
                discord.ChannelType.forum: "Forum",
            }.get(channel.type, "Autre")

            # ── 🔹 ÉTAPE 3 : Log console
            # Afficher l'information dans la console du bot
            channel_name = getattr(channel, 'name', 'Inconnu')
            self.bot.logger.info(
                f"🗑️ Salon supprimé | "
                f"Nom: #{channel_name} | "
                f"Type: {channel_type} | "
                f"ID: {channel.id}"
            )

        except Exception as e:
            # ── ⚠️ Gestion des erreurs
            self.bot.logger.error(f"❌ Erreur dans on_guild_channel_delete : {e}")

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🔌 FONCTION SETUP – setup
# ║ 📝 Charge le cog EventsSalons dans le bot Discord
# ╚═══════════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """
    Charge le cog EventsSalons dans le bot

    Args:
        bot: Instance du bot Discord
    """
    await bot.add_cog(EventsSalons(bot))

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ FIN DU FICHIER events_salons.py
# ╚══════════════════════════════════════════════════════════════════════════════
