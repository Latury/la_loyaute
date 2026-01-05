# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🤖 LA LOYAUTÉ - GESTIONNAIRE DU BOT
# ║
# ║ Classe principale du bot Discord
# ║ Développé par Latury
# ║ Version : 0.2.1
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from typing import Optional
from noyau.gestionnaire_configuration import GestionnaireConfiguration


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🤖 CLASSE PRINCIPALE
# ║ Description : Classe personnalisée du bot Discord
# ═══════════════════════════════════════════════════════════════════════════════

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

        # ── 🔹 ÉTAPE 1 : Stockage du logger
        self.logger = logger

        # ── 🔹 ÉTAPE 2 : Initialisation du gestionnaire de configuration
        self.config_manager = GestionnaireConfiguration(self.logger)
        self.logger.info("⚙️ Gestionnaire de configuration initialisé")

        # ── 🔹 ÉTAPE 3 : Variables d'état
        self.ready_called = False  # Pour éviter les appels multiples de on_ready


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🔧 FONCTION 01 – Configuration initiale
    # ║ Description : Configuration effectuée au démarrage du bot
    # ═══════════════════════════════════════════════════════════════════════════

    async def setup_hook(self):
        """
        Hook appelé avant la connexion du bot
        Utilisé pour la configuration initiale
        """
        try:
            self.logger.info("🔧 Exécution du setup_hook...")

            # ── 🔹 Synchronisation des commandes slash (si nécessaire)
            # await self.tree.sync()
            # self.logger.info("✅ Commandes slash synchronisées")

        except Exception as e:
            self.logger.error(f"❌ Erreur dans setup_hook : {e}")


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ ✅ FONCTION 02 – Bot prêt
    # ║ Description : Événement déclenché quand le bot est connecté
    # ═══════════════════════════════════════════════════════════════════════════

    async def on_ready(self):
        """
        Événement déclenché quand le bot est prêt
        """
        # ── 🔹 ÉTAPE 1 : Éviter les appels multiples
        if self.ready_called:
            return

        self.ready_called = True

        # ── 🔹 ÉTAPE 2 : Vérification de sécurité
        if not self.user:
            self.logger.error("❌ Erreur : self.user est None")
            return

        # ── 🔹 ÉTAPE 3 : Calcul du nombre total de membres
        total_membres = sum(guild.member_count or 0 for guild in self.guilds)

        # ── 🔹 ÉTAPE 4 : Log de connexion
        self.logger.info("═" * 80)
        self.logger.info(f"✅ Bot connecté : {self.user.name} (ID: {self.user.id})")
        self.logger.info(f"📊 Serveurs : {len(self.guilds)}")
        self.logger.info(f"👥 Membres : {total_membres}")
        self.logger.info("═" * 80)



    # ═══════════════════════════════════════════════════════════════════════════
    # ║ ❌ FONCTION 03 – Gestion des erreurs de commandes
    # ║ Description : Gère les erreurs qui surviennent lors de l'exécution
    # ═══════════════════════════════════════════════════════════════════════════

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """
        Gère les erreurs des commandes

        Args:
            ctx: Contexte de la commande
            error: Erreur survenue
        """
        # ── 🔹 Commande non trouvée (on ignore)
        if isinstance(error, commands.CommandNotFound):
            return

        # ── 🔹 Arguments manquants
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Argument manquant : `{error.param.name}`")
            return

        # ── 🔹 Permissions manquantes
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Vous n'avez pas les permissions nécessaires.")
            return

        # ── 🔹 Le bot n'a pas les permissions
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ Je n'ai pas les permissions nécessaires.")
            return

        # ── 🔹 Erreur de cooldown
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ Veuillez attendre {error.retry_after:.1f} secondes.")
            return

        # ── 🔹 Erreur inconnue
        self.logger.error(f"❌ Erreur de commande : {error}")
        await ctx.send("❌ Une erreur est survenue lors de l'exécution de la commande.")


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🔌 FONCTION 04 – Déconnexion du bot
    # ║ Description : Événement déclenché à la déconnexion
    # ═══════════════════════════════════════════════════════════════════════════

    async def on_disconnect(self):
        """
        Événement déclenché quand le bot se déconnecte
        """
        self.logger.warning("⚠️ Bot déconnecté de Discord")


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🔄 FONCTION 05 – Reconnexion du bot
    # ║ Description : Événement déclenché lors d'une reconnexion
    # ═══════════════════════════════════════════════════════════════════════════

    async def on_resumed(self):
        """
        Événement déclenché quand le bot se reconnecte
        """
        self.logger.info("🔄 Bot reconnecté à Discord")


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🛡️ FONCTION 06 – Rejoindre un serveur
    # ║ Description : Événement déclenché quand le bot rejoint un serveur
    # ═══════════════════════════════════════════════════════════════════════════

    async def on_guild_join(self, guild: discord.Guild):
        """
        Événement déclenché quand le bot rejoint un serveur

        Args:
            guild: Serveur rejoint
        """
        self.logger.info(
            f"➕ Bot ajouté au serveur : {guild.name} (ID: {guild.id}) | "
            f"Membres : {guild.member_count}"
        )


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 👋 FONCTION 07 – Quitter un serveur
    # ║ Description : Événement déclenché quand le bot quitte un serveur
    # ═══════════════════════════════════════════════════════════════════════════

    async def on_guild_remove(self, guild: discord.Guild):
        """
        Événement déclenché quand le bot quitte un serveur

        Args:
            guild: Serveur quitté
        """
        self.logger.info(
            f"➖ Bot retiré du serveur : {guild.name} (ID: {guild.id})"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# FIN DU FICHIER gestionnaire_bot.py
# ═══════════════════════════════════════════════════════════════════════════════
