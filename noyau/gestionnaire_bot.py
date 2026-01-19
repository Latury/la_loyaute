# ═══════════════════════════════════════════════════════════════
# ║
# ║ 🦁 LA LOYAUTÉ - gestionnaire_bot.py
# ║
# ║ 🤖 Bot Discord privé développé en Python
# ║ 👨💻 Développé par Latury
# ║ 📦 Version : 0.3.0 (CORRIGÉ)
# ║
# ═══════════════════════════════════════════════════════════════

"""
🦁 LA LOYAUTÉ - Gestionnaire principal du bot
══════════════════════════════════════════════════════════════
Classe principale du bot Discord avec gestion des événements
"""

import discord
from discord.ext import commands
from typing import Optional
import configuration as config
from noyau.gestionnaire_configuration import GestionnaireConfiguration

# ═══════════════════════════════════════════════════════════════
# 🤖 CLASSE PRINCIPALE - LoyauteBot
# ═══════════════════════════════════════════════════════════════

class LoyauteBot(commands.Bot):
    """Classe principale du bot La Loyauté"""

    def __init__(self, command_prefix: str, intents: discord.Intents, logger, **kwargs):
        """
        Initialise le bot La Loyauté

        Args:
            command_prefix: Préfixe des commandes
            intents: Intents Discord requis
            logger: Instance du logger
            **kwargs: Arguments supplémentaires pour commands.Bot
        """
        super().__init__(command_prefix=command_prefix, intents=intents, **kwargs)

        # ── 🔹 Stockage du logger
        self.logger = logger

        # ── 🔹 Initialisation du gestionnaire de configuration
        self.config_manager = GestionnaireConfiguration(self.logger)
        self.logger.info("⚙️ Gestionnaire de configuration initialisé")

        # ── 🔹 Variables d'état
        self.ready_called = False

    # ═══════════════════════════════════════════════════════════
    # 🔧 FONCTION 01 – setup_hook
    # ═══════════════════════════════════════════════════════════

    async def setup_hook(self):
        """
        Hook appelé avant la connexion du bot
        Utilisé pour la synchronisation des commandes
        """
        try:
            self.logger.info("🔧 Exécution du setup_hook...")
            self.logger.info("🔄 Synchronisation des commandes slash en cours...")

            # Récupérer GUILD_ID depuis la configuration
            guild_id = config.GUILD_ID

            # Synchroniser avec le serveur de test si configuré
            if guild_id and guild_id != 0:
                try:
                    guild = discord.Object(id=guild_id)
                    self.tree.copy_global_to(guild=guild)
                    synced = await self.tree.sync(guild=guild)
                    self.logger.info(f"✅ {len(synced)} commandes synchronisées avec le serveur {guild_id}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Sync serveur échouée : {e}")
                    synced = await self.tree.sync()
                    self.logger.info(f"✅ {len(synced)} commandes synchronisées globalement")
            else:
                self.logger.warning("⚠️ GUILD_ID non configuré, synchronisation globale")
                synced = await self.tree.sync()
                self.logger.info(f"✅ {len(synced)} commandes synchronisées globalement")

        except Exception as e:
            self.logger.error(f"❌ Erreur dans setup_hook : {e}")
            import traceback
            self.logger.error(f"Traceback : {traceback.format_exc()}")

    # ═══════════════════════════════════════════════════════════
    # ✅ FONCTION 02 – on_ready
    # ═══════════════════════════════════════════════════════════

    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""

        # Éviter les appels multiples
        if self.ready_called:
            return
        self.ready_called = True

        # Vérification de sécurité
        if not self.user:
            self.logger.error("❌ Erreur : self.user est None")
            return

        # Calcul du nombre total de membres
        total_membres = sum(guild.member_count or 0 for guild in self.guilds)

        # Log de connexion
        self.logger.info("═" * 80)
        self.logger.info(f"✅ Bot connecté : {self.user.name} (ID: {self.user.id})")
        self.logger.info(f"📊 Serveurs : {len(self.guilds)}")
        self.logger.info(f"👥 Membres : {total_membres}")
        self.logger.info("═" * 80)

    # ═══════════════════════════════════════════════════════════
    # ❌ FONCTION 03 – on_command_error
    # ═══════════════════════════════════════════════════════════

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Gère les erreurs des commandes"""

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Argument manquant : `{error.param.name}`")
            return

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Vous n'avez pas les permissions nécessaires.")
            return

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ Je n'ai pas les permissions nécessaires.")
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ Veuillez attendre {error.retry_after:.1f} secondes.")
            return

        # Erreur inconnue
        self.logger.error(f"❌ Erreur de commande : {error}")
        await ctx.send("❌ Une erreur est survenue.")

    # ═══════════════════════════════════════════════════════════
    # 🔌 FONCTION 04 – on_disconnect
    # ═══════════════════════════════════════════════════════════

    async def on_disconnect(self):
        """Événement déclenché lors de la déconnexion"""
        self.logger.warning("⚠️ Bot déconnecté de Discord")

    # ═══════════════════════════════════════════════════════════
    # 🔄 FONCTION 05 – on_resumed
    # ═══════════════════════════════════════════════════════════

    async def on_resumed(self):
        """Événement déclenché lors de la reconnexion"""
        self.logger.info("🔄 Bot reconnecté à Discord")

    # ═══════════════════════════════════════════════════════════
    # ➕ FONCTION 06 – on_guild_join
    # ═══════════════════════════════════════════════════════════

    async def on_guild_join(self, guild: discord.Guild):
        """Événement déclenché quand le bot rejoint un serveur"""
        self.logger.info(
            f"➕ Bot ajouté au serveur : {guild.name} (ID: {guild.id}) | "
            f"Membres : {guild.member_count}"
        )

    # ═══════════════════════════════════════════════════════════
    # ➖ FONCTION 07 – on_guild_remove
    # ═══════════════════════════════════════════════════════════

    async def on_guild_remove(self, guild: discord.Guild):
        """Événement déclenché quand le bot quitte un serveur"""
        self.logger.info(f"➖ Bot retiré du serveur : {guild.name} (ID: {guild.id})")

# ═══════════════════════════════════════════════════════════════
# ✅ FIN DU FICHIER
# ═══════════════════════════════════════════════════════════════
