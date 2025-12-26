# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║  👥 LA LOYAUTÉ - ÉVÉNEMENTS MEMBRES
# ║
# ║  Gestion des événements liés aux membres du serveur
# ║  Développé par Latury
# ║  Version : 0.2.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from utilitaires.logs_discord import log_member_join, log_member_leave


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 👥 CLASSE : EventsMembres
# ║ Description : Gestion des événements de membres
# ═══════════════════════════════════════════════════════════════════════════════

class EventsMembres(commands.Cog):
    """Gestion des événements liés aux membres"""

    def __init__(self, bot):
        """Initialise le cog des événements membres"""
        self.bot = bot
        self.bot.logger.info("✅ Cog EventsMembres chargé")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 👋 Événement 01 – Membre rejoint le serveur
    # ║ Description : Appelé quand un membre rejoint le serveur
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_member_join(self, membre: discord.Member):
        """Événement déclenché quand un membre rejoint le serveur"""

        try:
            # ── 🔹 Log console
            self.bot.logger.info(
                f"👋 {membre} (ID: {membre.id}) a rejoint {membre.guild.name}"
            )

            # ── 🔹 Log Discord
            await log_member_join(self.bot, membre)

        except Exception as e:
            self.bot.logger.error(f"❌ Erreur dans on_member_join : {e}")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 👋 Événement 02 – Membre quitte le serveur
    # ║ Description : Appelé quand un membre quitte le serveur
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_member_remove(self, membre: discord.Member):
        """Événement déclenché quand un membre quitte le serveur"""

        try:
            # ── 🔹 Log console
            self.bot.logger.info(
                f"👋 {membre} (ID: {membre.id}) a quitté {membre.guild.name}"
            )

            # ── 🔹 Log Discord
            await log_member_leave(self.bot, membre)

        except Exception as e:
            self.bot.logger.error(f"❌ Erreur dans on_member_remove : {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# ║ ⚙️ FONCTION SETUP
# ║ Description : Charge le cog dans le bot
# ═══════════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """Charge le cog des événements membres"""
    await bot.add_cog(EventsMembres(bot))
