# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║  📨 LA LOYAUTÉ - ÉVÉNEMENTS DE MESSAGES
# ║
# ║  Gestion des événements liés aux messages Discord
# ║  Développé par Latury
# ║  Version : 0.1.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from datetime import datetime

# Importation de la configuration
import configuration as config
from utilitaires.helpers import formater_date

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📦 Classe 01 – Cog de messages
# ║ Description : Gère tous les événements liés aux messages
# ╚══════════════════════════════════════════════════════════════════════════════
class Messages(commands.Cog):
    """Cog gérant les événements de messages"""

    def __init__(self, bot):
        """Initialise le cog de messages"""

        self.bot = bot
        self.messages_traites = 0
        self.messages_supprimes = 0
        self.messages_modifies = 0

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📝 Fonction 01 – Événement on_message
    # ║ Description : Appelé à chaque nouveau message
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Événement déclenché à chaque nouveau message"""

        # ── 🔹 Ignorer les messages du bot
        if message.author.bot:
            return

        # ── 🔹 Incrémentation du compteur
        self.messages_traites += 1

        # ── 🔹 Log si mode debug activé
        if config.DEBUG_MODE:
            info = (
                f"📨 Message reçu | "
                f"Auteur: {message.author} | "
                f"Serveur: {message.guild.name if message.guild else 'MP'} | "
                f"Contenu: {message.content[:50]}"
            )
            self.bot.logger.debug(info)

        # ── 🔹 Réponse automatique en MP (exemple)
        if isinstance(message.channel, discord.DMChannel):
            await self.gerer_message_prive(message)

        # ── 🔹 NOTE : Ne pas appeler process_commands ici
        # Le bot le fait déjà automatiquement via commands.Bot


    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 💬 Fonction 02 – Gestion des messages privés
    # ║ Description : Gère les messages privés envoyés au bot
    # ╚═════════════════════════════════════════════════════════════════════════
    async def gerer_message_prive(self, message: discord.Message):
        """Gère les messages privés"""

        # ── 🔹 Log du message privé
        self.bot.logger.info(f"💌 MP reçu de {message.author} : {message.content[:100]}")

        # ── 🔹 Réponse automatique (exemple)
        embed = discord.Embed(
            title=f"{config.EMOJI_INFO} Message reçu",
            description=(
                f"Bonjour **{message.author.name}** !\n\n"
                f"Votre message a bien été reçu. Si vous avez besoin d'aide, "
                f"utilisez la commande `{config.PREFIX_BASE}aide` sur un serveur.\n\n"
                f"Ce bot est actuellement en développement."
            ),
            color=config.COULEUR_INFO
        )
        embed.set_footer(text=f"{config.NOM_BOT} v{config.VERSION_BOT}")
        embed.timestamp = datetime.now()

        try:
            await message.author.send(embed=embed)
        except discord.Forbidden:
            self.bot.logger.warning(f"⚠️ Impossible de répondre à {message.author}")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🗑️ Fonction 03 – Événement on_message_delete
    # ║ Description : Appelé quand un message est supprimé
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Événement déclenché quand un message est supprimé"""

        # ── 🔹 Ignorer les messages du bot
        if message.author.bot:
            return

        # ── 🔹 Incrémentation du compteur
        self.messages_supprimes += 1

        # ── 🔹 Log de la suppression
        if config.DEBUG_MODE:
            info = (
                f"🗑️ Message supprimé | "
                f"Auteur: {message.author} | "
                f"Serveur: {message.guild.name if message.guild else 'MP'} | "
                f"Contenu: {message.content[:50]}"
            )
            self.bot.logger.debug(info)

        # ── 🔹 Ici, vous pouvez ajouter un système de logs dans un salon dédié
        # Exemple : envoyer la suppression dans un salon de logs

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ ✏️ Fonction 04 – Événement on_message_edit
    # ║ Description : Appelé quand un message est modifié
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_message_edit(self, avant: discord.Message, apres: discord.Message):
        """Événement déclenché quand un message est modifié"""

        # ── 🔹 Ignorer les messages du bot
        if avant.author.bot:
            return

        # ── 🔹 Ignorer si le contenu n'a pas changé (edit d'embed par exemple)
        if avant.content == apres.content:
            return

        # ── 🔹 Incrémentation du compteur
        self.messages_modifies += 1

        # ── 🔹 Log de la modification
        if config.DEBUG_MODE:
            info = (
                f"✏️ Message modifié | "
                f"Auteur: {avant.author} | "
                f"Serveur: {avant.guild.name if avant.guild else 'MP'} | "
                f"Avant: {avant.content[:30]} | "
                f"Après: {apres.content[:30]}"
            )
            self.bot.logger.debug(info)

        # ── 🔹 Traiter les commandes sur le message modifié
        await self.bot.process_commands(apres)

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📊 Fonction 05 – Obtenir les statistiques
    # ║ Description : Retourne les statistiques des messages
    # ╚═════════════════════════════════════════════════════════════════════════
    def obtenir_statistiques(self) -> dict:
        """Retourne les statistiques des messages"""

        return {
            'messages_traites': self.messages_traites,
            'messages_supprimes': self.messages_supprimes,
            'messages_modifies': self.messages_modifies
        }

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🔍 Fonction 06 – Événement on_raw_message_delete
    # ║ Description : Appelé pour messages non en cache
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        """Événement pour messages supprimés non en cache"""

        # ── 🔹 Log de la suppression
        if config.DEBUG_MODE:
            self.bot.logger.debug(
                f"🗑️ Message supprimé (non en cache) | "
                f"ID: {payload.message_id} | "
                f"Canal: {payload.channel_id}"
            )

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🔍 Fonction 07 – Événement on_raw_message_edit
    # ║ Description : Appelé pour messages modifiés non en cache
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        """Événement pour messages modifiés non en cache"""

        # ── 🔹 Log de la modification
        if config.DEBUG_MODE and 'content' in payload.data:
            self.bot.logger.debug(
                f"✏️ Message modifié (non en cache) | "
                f"ID: {payload.message_id} | "
                f"Canal: {payload.channel_id}"
            )

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🔇 Fonction 08 – Événement on_raw_bulk_message_delete
    # ║ Description : Appelé lors de suppressions en masse
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload: discord.RawBulkMessageDeleteEvent):
        """Événement déclenché lors de suppression en masse"""

        # ── 🔹 Log de la suppression en masse
        nombre_messages = len(payload.message_ids)
        self.messages_supprimes += nombre_messages

        self.bot.logger.info(
            f"🗑️ Suppression en masse de {nombre_messages} messages | "
            f"Canal: {payload.channel_id}"
        )

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📦 Fonction setup
# ║ Description : Fonction requise pour charger le cog
# ╚══════════════════════════════════════════════════════════════════════════════
async def setup(bot):
    """Charge le cog de messages"""
    await bot.add_cog(Messages(bot))
