# ═══════════════════════════════════════════════════════════════════════════════
# ║                                                                             
# ║  🧠 LA LOYAUTÉ - GESTIONNAIRE DU BOT
# ║
# ║  Classe principale du bot avec gestion des événements et extensions
# ║  Développé par Latury
# ║  Version : 0.1.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from datetime import datetime
import traceback

# Importation de la configuration
import configuration as config

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🤖 Classe 01 – LoyauteBot
# ║ Description : Classe principale héritant de commands.Bot
# ╚══════════════════════════════════════════════════════════════════════════════
class LoyauteBot(commands.Bot):
    """Classe principale du bot La Loyauté"""

    def __init__(self, command_prefix, intents, help_command, logger):
        """Initialise le bot avec les paramètres fournis"""

        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            help_command=help_command
        )

        # ── 🔹 Stockage des paramètres
        self.logger = logger
        self.heure_demarrage = None
        self.version = config.VERSION_BOT
        self.developpeur = config.DEVELOPPEUR

        # ── 🔹 Statistiques
        self.commandes_executees = 0
        self.erreurs_commandes = 0

        self.logger.info("🔧 Classe LoyauteBot initialisée")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🎯 Fonction 01 – Configuration du bot
    # ║ Description : Configure le bot après l'instanciation
    # ╚═════════════════════════════════════════════════════════════════════════
    async def setup_hook(self):
        """Hook appelé lors de la configuration du bot"""

        self.logger.info("⚙️ Configuration du bot en cours...")

        # ── 🔹 Synchronisation des commandes slash (si nécessaire)
        try:
            if config.GUILD_ID and config.GUILD_ID != 0:
                guild = discord.Object(id=config.GUILD_ID)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                self.logger.info(f"🔄 Commandes slash synchronisées pour le serveur {config.GUILD_ID}")
            else:
                await self.tree.sync()
                self.logger.info("🔄 Commandes slash synchronisées globalement")
        except Exception as e:
            self.logger.warning(f"⚠️ Impossible de synchroniser les commandes slash : {e}")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🚀 Fonction 02 – Événement on_ready
    # ║ Description : Appelé quand le bot est connecté et prêt
    # ╚═════════════════════════════════════════════════════════════════════════
    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""

        # ── 🔹 Enregistrement de l'heure de démarrage
        self.heure_demarrage = datetime.now()

        # ── 🔹 Statistiques du bot
        nb_serveurs = len(self.guilds)
        nb_utilisateurs = sum(guild.member_count for guild in self.guilds if guild.member_count)
        nb_commandes = len(self.commands)

        # ── 🔹 Logs de démarrage (l'affichage du cadre est géré dans demarrage.py)
        self.logger.info(f"🤖 Bot connecté : {self.user.name if self.user else 'Inconnu'} (ID: {self.user.id if self.user else 0})")
        self.logger.info(f"📊 Serveurs : {nb_serveurs}")
        self.logger.info(f"👥 Utilisateurs : {nb_utilisateurs}")
        self.logger.info(f"⚡ Commandes chargées : {nb_commandes}")

        # ── 🔹 Définition du statut
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{config.PREFIX_BASE}aide | Version {config.VERSION_BOT}"
            ),
            status=discord.Status.online
        )

        self.logger.info("✅ Bot opérationnel")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ ⚠️ Fonction 03 – Gestion des erreurs de commandes
    # ║ Description : Gère toutes les erreurs lors de l'exécution
    # ╚═════════════════════════════════════════════════════════════════════════
    async def on_command_error(self, ctx, error):
        """Gère les erreurs des commandes"""

        # ── 🔹 Incrémentation du compteur d'erreurs
        self.erreurs_commandes += 1

        # ── 🔹 Commande non trouvée
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"{config.EMOJI_AVERTISSEMENT} Commande inconnue. Utilisez `{config.PREFIX_BASE}aide` pour voir les commandes disponibles.")
            return

        # ── 🔹 Arguments manquants
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{config.EMOJI_ERREUR} {config.MSG_ERREUR_ARGUMENTS}")
            return

        # ── 🔹 Permissions manquantes
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{config.EMOJI_ERREUR} {config.MSG_ERREUR_PERMISSION}")
            return

        # ── 🔹 Cooldown
        if isinstance(error, commands.CommandOnCooldown):
            temps_restant = round(error.retry_after, 1)
            await ctx.send(f"{config.EMOJI_AVERTISSEMENT} Cette commande est en cooldown. Réessayez dans {temps_restant}s.")
            return

        # ── 🔹 Erreur générique
        self.logger.error(f"❌ Erreur dans la commande {ctx.command} : {error}")
        self.logger.error(traceback.format_exc())

        embed = discord.Embed(
            title=f"{config.EMOJI_ERREUR} Erreur",
            description=config.MSG_ERREUR_COMMANDE,
            color=config.COULEUR_ERREUR
        )
        embed.add_field(name="Détails", value=f"``````", inline=False)

        await ctx.send(embed=embed)

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📊 Fonction 04 – Statistiques du bot
    # ║ Description : Retourne les statistiques du bot
    # ╚═════════════════════════════════════════════════════════════════════════
    def obtenir_statistiques(self):
        """Retourne un dictionnaire avec les statistiques du bot"""

        # ── 🔹 Calcul de l'uptime
        uptime = None
        if self.heure_demarrage:
            delta = datetime.now() - self.heure_demarrage
            heures, reste = divmod(int(delta.total_seconds()), 3600)
            minutes, secondes = divmod(reste, 60)
            uptime = f"{heures}h {minutes}m {secondes}s"

        # ── 🔹 Compilation des statistiques
        stats = {
            'nom': self.user.name if self.user else 'Inconnu',
            'id': self.user.id if self.user else 0,
            'version': self.version,
            'developpeur': self.developpeur,
            'serveurs': len(self.guilds),
            'utilisateurs': sum(guild.member_count for guild in self.guilds if guild.member_count),
            'commandes': len(self.commands),
            'commandes_executees': self.commandes_executees,
            'erreurs': self.erreurs_commandes,
            'uptime': uptime,
            'latence': round(self.latency * 1000, 2)  # en ms
        }

        return stats

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📝 Fonction 05 – Avant l'exécution d'une commande
    # ║ Description : Hook appelé avant chaque commande
    # ╚═════════════════════════════════════════════════════════════════════════
    async def on_command(self, ctx):
        """Appelé avant l'exécution de chaque commande"""

        # ── 🔹 Incrémentation du compteur
        self.commandes_executees += 1

        # ── 🔹 Log de la commande
        self.logger.info(
            f"⚡ Commande exécutée : {ctx.command} | "
            f"Auteur : {ctx.author} (ID: {ctx.author.id}) | "
            f"Serveur : {ctx.guild.name if ctx.guild else 'MP'}"
        )

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🔌 Fonction 06 – Déconnexion du bot
    # ║ Description : Appelé lors de la déconnexion
    # ╚═════════════════════════════════════════════════════════════════════════
    async def on_disconnect(self):
        """Événement déclenché lors de la déconnexion"""

        self.logger.warning("⚠️ Bot déconnecté de Discord")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🔄 Fonction 07 – Reconnexion du bot
    # ║ Description : Appelé lors de la reconnexion
    # ╚═════════════════════════════════════════════════════════════════════════
    async def on_resumed(self):
        """Événement déclenché lors de la reconnexion"""

        self.logger.info("🔄 Bot reconnecté à Discord")
