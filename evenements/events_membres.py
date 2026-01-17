# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║  👥 LA LOYAUTÉ - ÉVÉNEMENTS MEMBRES
# ║  Discord Bot | Gestion des événements liés aux membres du serveur
# ║  Développé par Latury
# ║  Version 0.2.2
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 👥 FICHIER : events_membres.py
# ║ 📦 MODULE : evenements
# ║ 📝 DESCRIPTION : Gestion des événements liés aux membres du serveur
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15 janvier 2026
# ║ 🔖 VERSION : 0.2.2
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from utilitaires import logs_discord


# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 📦 CLASSE 01 – EventsMembres
# ║ 🎯 Cog pour gérer tous les événements liés aux membres du serveur
# ╚═══════════════════════════════════════════════════════════════════════════════
class EventsMembres(commands.Cog):
    """Gestion des événements liés aux membres"""

    def __init__(self, bot):
        """
        Initialisation du cog EventsMembres

        Args:
            bot: Instance du bot Discord
        """
        self.bot = bot
        self.bot.logger.info("👥 Module EventsMembres chargé")


    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ 👋 FONCTION 01 – on_member_join
    # ║ 📝 Événement déclenché quand un membre rejoint le serveur
    # ╚═══════════════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_member_join(self, membre: discord.Member):
        """
        Événement déclenché quand un membre rejoint le serveur

        Args:
            membre: Membre qui a rejoint le serveur
        """
        try:
            # ── 🔹 ÉTAPE 1 : Log console
            # Afficher l'information dans la console du bot
            self.bot.logger.info(
                f"👋 Nouveau membre | "
                f"Nom: {membre} | "
                f"ID: {membre.id} | "
                f"Serveur: {membre.guild.name}"
            )

            # ── 🔹 ÉTAPE 2 : Log Discord
            # Envoyer un embed dans le salon de logs Discord
            await logs_discord.log_member_join(self.bot, membre)

        except Exception as e:
            # ── ⚠️ Gestion des erreurs
            self.bot.logger.error(f"❌ Erreur dans on_member_join : {e}")


    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ 👋 FONCTION 02 – on_member_remove
    # ║ 📝 Événement déclenché quand un membre quitte le serveur
    # ╚═══════════════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_member_remove(self, membre: discord.Member):
        """
        Événement déclenché quand un membre quitte le serveur

        Args:
            membre: Membre qui a quitté le serveur
        """
        try:
            # ── 🔹 ÉTAPE 1 : Log console
            # Afficher l'information dans la console du bot
            self.bot.logger.info(
                f"👋 Membre parti | "
                f"Nom: {membre} | "
                f"ID: {membre.id} | "
                f"Serveur: {membre.guild.name}"
            )

            # ── 🔹 ÉTAPE 2 : Log Discord
            # Envoyer un embed dans le salon de logs Discord
            await logs_discord.log_member_leave(self.bot, membre)

        except Exception as e:
            # ── ⚠️ Gestion des erreurs
            self.bot.logger.error(f"❌ Erreur dans on_member_remove : {e}")

    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ 🎭 FONCTION 03 – on_member_update
    # ║ 📝 Événement déclenché lors de changements au profil d'un membre
    # ╚═══════════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """
        Événement déclenché lors de la mise à jour d'un membre

        Args:
            before: État du membre avant modification
            after: État du membre après modification
        """
        try:
            # ── 🔹 ÉTAPE 1 : Vérification des rôles
            # Détection des changements de rôles uniquement
            roles_added = [role for role in after.roles if role not in before.roles]
            roles_removed = [role for role in before.roles if role not in after.roles]

            # ── 🔹 ÉTAPE 2 : Si des rôles ont changé
            if roles_added or roles_removed:

                # ── 🔹 ÉTAPE 3 : Log console
                # Afficher l'information dans la console du bot
                if roles_added:
                    roles_text = ", ".join([role.name for role in roles_added])
                    self.bot.logger.info(
                        f"🎭 Rôle(s) ajouté(s) | "
                        f"Membre: {after} | "
                        f"Rôle(s): {roles_text}"
                    )

                if roles_removed:
                    roles_text = ", ".join([role.name for role in roles_removed])
                    self.bot.logger.info(
                        f"🎭 Rôle(s) retiré(s) | "
                        f"Membre: {after} | "
                        f"Rôle(s): {roles_text}"
                    )

                # ── 🔹 ÉTAPE 4 : Log Discord
                # Envoyer un embed dans le salon de logs Discord
                await logs_discord.log_member_roles_update(self.bot, before, after)

        except Exception as e:
            # ── ⚠️ Gestion des erreurs
            self.bot.logger.error(f"❌ Erreur dans on_member_update : {e}")

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🔌 FONCTION SETUP – setup
# ║ 📝 Charge le cog EventsMembres dans le bot Discord
# ╚══════════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """
    Charge le cog EventsMembres dans le bot

    Args:
        bot: Instance du bot Discord
    """
    await bot.add_cog(EventsMembres(bot))


# ╔══════════════════════════════════════════════════════════════════════════════
# ║  FIN DU FICHIER events_membres.py
# ╚══════════════════════════════════════════════════════════════════════════════