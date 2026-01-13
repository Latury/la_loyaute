# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║  📄 FICHIER : commandes_admin.py
# ║  📦 MODULE : commandes
# ║  📝 DESCRIPTION : Commandes administratives (slash commands)
# ║  👤 AUTEUR : Latury
# ║  📅 DATE : 25/12/2025
# ║  🔖 VERSION : 0.2.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import os
import json
from utilitaires.helpers import creer_embed, creer_embed_succes, creer_embed_erreur, creer_embed_avertissement
from utilitaires.logs_discord import log_kick, log_ban, log_unban, log_timeout, log_warn, log_clear
import configuration as config
from typing import Optional
from discord import Interaction, TextChannel
from discord.ext.commands import Cog
from discord.app_commands import command, describe


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 👑 CLASSE : CommandesAdmin
# ║ Description : Gestion des commandes administratives (slash commands)
# ═══════════════════════════════════════════════════════════════════════════════

class CommandesAdmin(commands.Cog):
    """Commandes administratives réservées aux modérateurs et administrateurs"""

    def __init__(self, bot):
        """Initialise le cog des commandes administratives"""
        self.bot = bot
        self.bot.logger.info("✅ Cog CommandesAdmin chargé")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🧹 Fonction 01 – Commande /clear
    # ║ Description : Supprime un nombre spécifique de messages
    # ╚═════════════════════════════════════════════════════════════════════════
    @app_commands.command(
        name="clear",
        description="Supprime un nombre spécifique de messages dans le salon"
    )
    @app_commands.describe(nombre="Nombre de messages à supprimer (max 100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, nombre: int):
        """Supprime des messages en masse"""

        # ── 🔹 Vérification que la commande est utilisée dans un serveur
        if not interaction.guild:
            embed = creer_embed_erreur(
                titre="Erreur",
                description="Cette commande ne peut être utilisée que dans un serveur."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # ── 🔹 Vérification du nombre de messages
        if nombre < 1 or nombre > 100:
            embed = creer_embed_erreur(
                titre="Erreur de paramètre",
                description="Le nombre de messages doit être entre 1 et 100."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # ── 🔹 Réponse différée (pour éviter le timeout)
        await interaction.response.defer(ephemeral=True)

        try:
            # ── 🔹 Suppression des messages
            if isinstance(interaction.channel, discord.TextChannel):
                messages_supprimes = await interaction.channel.purge(limit=nombre)
                nombre_supprimes = len(messages_supprimes)

                # ── 🔹 Message de confirmation
                embed = creer_embed_succes(
                    titre="Messages supprimés",
                    description=f"{config.EMOJI_SUCCES} **{nombre_supprimes}** message(s) supprimé(s) avec succès."
                )
                embed.add_field(
                    name="Modérateur",
                    value=interaction.user.mention,
                    inline=True
                )
                embed.add_field(
                    name="Salon",
                    value=interaction.channel.mention,
                    inline=True
                )

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log de l'action
                self.bot.logger.info(
                    f"🧹 {nombre_supprimes} messages supprimés par {interaction.user} "
                    f"dans {interaction.channel.name}"
                )

                # ── 🔹 Log Discord
                await log_clear(
                    bot=self.bot,
                    guild=interaction.guild,
                    salon=interaction.channel,
                    moderateur=interaction.user,
                    nombre=nombre_supprimes
                )


        except discord.Forbidden:
            embed = creer_embed_erreur(
                titre="Erreur de permissions",
                description="Je n'ai pas la permission de supprimer des messages dans ce salon."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            embed = creer_embed_erreur(
                titre="Erreur",
                description=f"Une erreur s'est produite lors de la suppression des messages."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            self.bot.logger.error(f"❌ Erreur dans /clear : {e}")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📝 Fonction 02 – Commande /logs
    # ║ Description : Affiche les dernières lignes du fichier de log
    # ╚═════════════════════════════════════════════════════════════════════════
    @app_commands.command(
        name="logs",
        description="Affiche les derniers logs du bot"
    )
    @app_commands.describe(nombre="Nombre de lignes à afficher (max 50)")
    @app_commands.checks.has_permissions(administrator=True)
    async def logs(self, interaction: discord.Interaction, nombre: int = 20):
        """Affiche les logs récents"""

        # ── 🔹 Vérification du nombre de lignes
        if nombre < 1 or nombre > 50:
            embed = creer_embed_erreur(
                titre="Erreur de paramètre",
                description="Le nombre de lignes doit être entre 1 et 50."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # ── 🔹 Réponse différée
        await interaction.response.defer(ephemeral=True)

        try:
            # ── 🔹 Récupération du fichier de log actuel
            aujourd_hui = datetime.now().strftime("%d-%m-%Y")
            fichier_log = f"logs/{config.NOM_BOT.lower().replace(' ', '_')}_{aujourd_hui}.log"

            if not os.path.exists(fichier_log):
                embed = creer_embed_avertissement(
                    titre="Aucun log disponible",
                    description="Aucun fichier de log n'a été trouvé pour aujourd'hui."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # ── 🔹 Lecture des dernières lignes
            with open(fichier_log, 'r', encoding='utf-8') as f:
                lignes = f.readlines()
                dernieres_lignes = lignes[-nombre:]

            # ── 🔹 Création de l'embed
            contenu = "".join(dernieres_lignes)

            # ── 🔹 Limitation à 1024 caractères (limite Discord)
            if len(contenu) > 1024:
                contenu = contenu[-1024:]
                contenu = "...\n" + contenu

            embed = creer_embed(
                titre=f"📝 Logs récents ({nombre} dernières lignes)",
                description="",
                couleur=config.COULEUR_PRINCIPALE
            )
            embed.add_field(
                name="Contenu",
                value=f"``````",
                inline=False
            )

            # ── 🔹 Statistiques des logs
            total_lignes = len(lignes)
            taille_fichier = os.path.getsize(fichier_log)
            taille_ko = round(taille_fichier / 1024, 2)

            embed.add_field(
                name="Statistiques",
                value=f"Total de lignes : {total_lignes}\nTaille du fichier : {taille_ko} Ko",
                inline=False
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

            # ── 🔹 Log de la consultation
            self.bot.logger.info(f"📝 Logs consultés par {interaction.user} ({nombre} lignes)")

        except Exception as e:
            embed = creer_embed_erreur(
                titre="Erreur",
                description="Impossible de lire le fichier de logs."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            self.bot.logger.error(f"❌ Erreur dans /logs : {e}")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🔄 Fonction 03 – Commande /reload
    # ║ Description : Recharge une extension du bot
    # ╚═════════════════════════════════════════════════════════════════════════
    @app_commands.command(
        name="reload",
        description="Recharge une extension du bot"
    )
    @app_commands.describe(extension="Nom de l'extension à recharger")
    @app_commands.checks.has_permissions(administrator=True)
    async def reload(self, interaction: discord.Interaction, extension: str):
        """Recharge une extension"""

        # ── 🔹 Réponse différée
        await interaction.response.defer(ephemeral=True)

        try:
            # ── 🔹 Rechargement de l'extension
            await self.bot.reload_extension(extension)

            # ── 🔹 Confirmation
            embed = creer_embed_succes(
                titre="Extension rechargée",
                description=f"{config.EMOJI_SUCCES} L'extension **{extension}** a été rechargée avec succès."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

            # ── 🔹 Log du rechargement
            self.bot.logger.info(f"🔄 Extension {extension} rechargée par {interaction.user}")

        except commands.ExtensionNotFound:
            embed = creer_embed_erreur(
                titre="Extension introuvable",
                description=f"L'extension **{extension}** n'existe pas."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except commands.ExtensionNotLoaded:
            embed = creer_embed_erreur(
                titre="Extension non chargée",
                description=f"L'extension **{extension}** n'est pas actuellement chargée."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            embed = creer_embed_erreur(
                titre="Erreur de rechargement",
                description=f"Impossible de recharger l'extension **{extension}**."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            self.bot.logger.error(f"❌ Erreur lors du rechargement de {extension} : {e}")

# ╔═════════════════════════════════════════════════════════════════════════
# ║ 🔄 Fonction 04 – Commande /sync
# ║ Description : Synchronise les commandes slash avec Discord
# ╚═════════════════════════════════════════════════════════════════════════

    @app_commands.command(
        name="sync",
        description="Synchronise les commandes slash du bot"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction: discord.Interaction):
        """Synchronise les commandes slash"""

        await interaction.response.defer(ephemeral=True)

        try:
            # ── 🔹 Synchronisation
            synced = await self.bot.tree.sync()

            # ── 🔹 Confirmation
            embed = creer_embed_succes(
                titre="Commandes synchronisées",
                description=f"{config.EMOJI_SUCCES} **{len(synced)}** commande(s) synchronisée(s) avec Discord."
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

            # ── 🔹 Log
            self.bot.logger.info(f"🔄 {len(synced)} commandes synchronisées par {interaction.user}")

        except Exception as e:
            embed = creer_embed_erreur(
                titre="Erreur",
                description=f"Impossible de synchroniser les commandes."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            self.bot.logger.error(f"❌ Erreur dans /sync : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ 🔴 Fonction 05 – Commande /shutdown
        # ║ Description : Arrête proprement le bot
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="shutdown",
            description="Arrête proprement le bot"
        )
        @app_commands.checks.has_permissions(administrator=True)
        async def shutdown(self, interaction: discord.Interaction):
            """Arrête le bot"""

            # ── 🔹 Demande de confirmation
            embed = creer_embed_avertissement(
                titre="⚠️ Confirmation requise",
                description="Êtes-vous sûr de vouloir arrêter le bot ?\n\n"
                           "Réagissez avec ✅ pour confirmer ou ❌ pour annuler."
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)
            message = await interaction.original_response()

            # ── 🔹 Ajout des réactions
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            # ── 🔹 Vérification de la réaction
            def check(reaction, user):
                return (
                    user == interaction.user
                    and str(reaction.emoji) in ["✅", "❌"]
                    and reaction.message.id == message.id
                )

            try:
                reaction, user = await self.bot.wait_for(
                    'reaction_add',
                    timeout=30.0,
                    check=check
                )

                if str(reaction.emoji) == "✅":
                    # ── 🔹 Arrêt confirmé
                    embed = creer_embed_erreur(
                        titre="🔴 Arrêt du bot",
                        description="Le bot va s'arrêter dans quelques instants..."
                    )
                    await interaction.edit_original_response(embed=embed)

                    # ── 🔹 Log de l'arrêt
                    self.bot.logger.warning(f"🔴 Arrêt du bot demandé par {interaction.user}")

                    # ── 🔹 Fermeture du bot
                    await self.bot.close()

                else:
                    # ── 🔹 Arrêt annulé
                    embed = creer_embed_succes(
                        titre="Arrêt annulé",
                        description=f"{config.EMOJI_SUCCES} L'arrêt du bot a été annulé."
                    )
                    await interaction.edit_original_response(embed=embed)

            except Exception:
                # ── 🔹 Timeout ou erreur
                embed = creer_embed_erreur(
                    titre="Timeout",
                    description="Aucune réponse reçue. L'arrêt a été annulé."
                )
                await interaction.edit_original_response(embed=embed)

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ 🚫 Fonction 06 – Commande /kick
        # ║ Description : Expulse un membre du serveur
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="kick",
            description="Expulse un membre du serveur"
        )
        @app_commands.describe(
            membre="Le membre à expulser",
            raison="Raison de l'expulsion"
        )
        @app_commands.checks.has_permissions(kick_members=True)
        async def kick(
            self,
            interaction: discord.Interaction,
            membre: discord.Member,
            raison: str = "Aucune raison fournie"
        ):
            """Expulse un membre du serveur"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Vérifications de sécurité
            if membre.id == interaction.user.id:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Vous ne pouvez pas vous expulser vous-même."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if membre.id == self.bot.user.id:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Je ne peux pas m'expulser moi-même."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Vérification des rôles (seulement si interaction.user est Member)
            if isinstance(interaction.user, discord.Member):
                if membre.top_role >= interaction.user.top_role:
                    embed = creer_embed_erreur(
                        titre="Erreur",
                        description="Vous ne pouvez pas expulser un membre avec un rôle égal ou supérieur au vôtre."
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            # ── 🔹 Réponse différée
            await interaction.response.defer(ephemeral=True)

            try:
                # ── 🔹 Envoi d'un MP au membre avant expulsion
                try:
                    embed_mp = creer_embed_avertissement(
                        titre="Expulsion du serveur",
                        description=f"Vous avez été expulsé de **{interaction.guild.name}**."
                    )
                    embed_mp.add_field(name="Raison", value=raison, inline=False)
                    embed_mp.add_field(
                        name="Modérateur",
                        value=f"{interaction.user.mention}",
                        inline=False
                    )
                    await membre.send(embed=embed_mp)
                except discord.Forbidden:
                    pass

                # ── 🔹 Expulsion
                await membre.kick(reason=f"{raison} | Par {interaction.user}")

                # ── 🔹 Confirmation
                embed = creer_embed_succes(
                    titre="Membre expulsé",
                    description=f"{config.EMOJI_SUCCES} **{membre}** a été expulsé du serveur."
                )
                embed.add_field(name="Raison", value=raison, inline=False)
                embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log de l'action
                self.bot.logger.info(
                    f"🚫 {membre} (ID: {membre.id}) expulsé par {interaction.user} | Raison : {raison}"
                )

                # ── 🔹 Log Discord
                await log_kick(
                    bot=self.bot,
                    guild=interaction.guild,
                    membre=membre,
                    moderateur=interaction.user,
                    raison=raison
                )


            except discord.Forbidden:
                embed = creer_embed_erreur(
                    titre="Erreur de permissions",
                    description="Je n'ai pas la permission d'expulser ce membre."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /kick : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ 🔨 Fonction 07 – Commande /ban
        # ║ Description : Bannit un membre du serveur
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="ban",
            description="Bannit un membre du serveur"
        )
        @app_commands.describe(
            membre="Le membre à bannir",
            raison="Raison du bannissement",
            supprimer_messages="Nombre de jours de messages à supprimer (0-7)"
        )
        @app_commands.checks.has_permissions(ban_members=True)
        async def ban(
            self,
            interaction: discord.Interaction,
            membre: discord.Member,
            raison: str = "Aucune raison fournie",
            supprimer_messages: int = 0
        ):
            """Bannit un membre du serveur"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Vérifications de sécurité
            if membre.id == interaction.user.id:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Vous ne pouvez pas vous bannir vous-même."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if membre.id == self.bot.user.id:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Je ne peux pas me bannir moi-même."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Vérification des rôles (seulement si interaction.user est Member)
            if isinstance(interaction.user, discord.Member):
                if membre.top_role >= interaction.user.top_role:
                    embed = creer_embed_erreur(
                        titre="Erreur",
                        description="Vous ne pouvez pas bannir un membre avec un rôle égal ou supérieur au vôtre."
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            # ── 🔹 Vérification du nombre de jours
            if supprimer_messages < 0 or supprimer_messages > 7:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Le nombre de jours doit être entre 0 et 7."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Réponse différée
            await interaction.response.defer(ephemeral=True)

            try:
                # ── 🔹 Envoi d'un MP au membre avant bannissement
                try:
                    embed_mp = creer_embed_erreur(
                        titre="Bannissement du serveur",
                        description=f"Vous avez été banni de **{interaction.guild.name}**."
                    )
                    embed_mp.add_field(name="Raison", value=raison, inline=False)
                    embed_mp.add_field(
                        name="Modérateur",
                        value=f"{interaction.user.mention}",
                        inline=False
                    )
                    await membre.send(embed=embed_mp)
                except discord.Forbidden:
                    pass

                # ── 🔹 Bannissement
                await membre.ban(
                    reason=f"{raison} | Par {interaction.user}",
                    delete_message_days=supprimer_messages
                )

                # ── 🔹 Confirmation
                embed = creer_embed_succes(
                    titre="Membre banni",
                    description=f"{config.EMOJI_SUCCES} **{membre}** a été banni du serveur."
                )
                embed.add_field(name="Raison", value=raison, inline=False)
                embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)
                if supprimer_messages > 0:
                    embed.add_field(
                        name="Messages supprimés",
                        value=f"{supprimer_messages} jour(s)",
                        inline=True
                    )

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log de l'action
                self.bot.logger.info(
                    f"🔨 {membre} (ID: {membre.id}) banni par {interaction.user} | "
                    f"Raison : {raison} | Messages supprimés : {supprimer_messages}j"
                )

                # ── 🔹 Log Discord
                await log_ban(
                    bot=self.bot,
                    guild=interaction.guild,
                    membre=membre,
                    moderateur=interaction.user,
                    raison=raison,
                    jours_messages=supprimer_messages
                )


            except discord.Forbidden:
                embed = creer_embed_erreur(
                    titre="Erreur de permissions",
                    description="Je n'ai pas la permission de bannir ce membre."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /ban : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ 🔓 Fonction 08 – Commande /unban
        # ║ Description : Débannit un utilisateur
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="unban",
            description="Débannit un utilisateur du serveur"
        )
        @app_commands.describe(
            user_id="L'ID de l'utilisateur à débannir",
            raison="Raison du débannissement"
        )
        @app_commands.checks.has_permissions(ban_members=True)
        async def unban(
            self,
            interaction: discord.Interaction,
            user_id: str,
            raison: str = "Aucune raison fournie"
        ):
            """Débannit un utilisateur"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Vérification de l'ID
            try:
                user_id_int = int(user_id)
            except ValueError:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="L'ID fourni n'est pas valide."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Réponse différée
            await interaction.response.defer(ephemeral=True)

            try:
                # ── 🔹 Recherche de l'utilisateur dans les bans
                ban_entry = None
                async for ban in interaction.guild.bans():
                    if ban.user.id == user_id_int:
                        ban_entry = ban
                        break

                if not ban_entry:
                    embed = creer_embed_erreur(
                        titre="Utilisateur non trouvé",
                        description=f"Aucun utilisateur avec l'ID `{user_id}` n'est actuellement banni."
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return

                # ── 🔹 Débannissement
                await interaction.guild.unban(
                    ban_entry.user,
                    reason=f"{raison} | Par {interaction.user}"
                )

                # ── 🔹 Confirmation
                embed = creer_embed_succes(
                    titre="Utilisateur débanni",
                    description=f"{config.EMOJI_SUCCES} **{ban_entry.user}** a été débanni du serveur."
                )
                embed.add_field(name="Raison", value=raison, inline=False)
                embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log de l'action
                self.bot.logger.info(
                    f"🔓 {ban_entry.user} (ID: {user_id_int}) débanni par {interaction.user} | "
                    f"Raison : {raison}"
                )

                # ── 🔹 Log Discord
                await log_unban(
                    bot=self.bot,
                    guild=interaction.guild,
                    utilisateur=ban_entry.user,
                    moderateur=interaction.user,
                    raison=raison
                )


            except discord.NotFound:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Utilisateur introuvable."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

            except discord.Forbidden:
                embed = creer_embed_erreur(
                    titre="Erreur de permissions",
                    description="Je n'ai pas la permission de débannir des utilisateurs."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /unban : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ 🔇 Fonction 09 - Commande /timeout
        # ║ Description : Met un membre en timeout (mute temporaire)
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="timeout",
            description="Met un membre en timeout (mute temporaire)"
        )
        @app_commands.describe(
            membre="Le membre à mettre en timeout",
            duree="Durée en minutes (max 40320 = 28 jours)",
            raison="Raison du timeout"
        )
        @app_commands.checks.has_permissions(moderate_members=True)
        async def timeout(
            self,
            interaction: discord.Interaction,
            membre: discord.Member,
            duree: int,
            raison: str = "Aucune raison fournie"
        ):
            """Met un membre en timeout"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Vérifications de sécurité
            if membre.id == interaction.user.id:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Vous ne pouvez pas vous mettre en timeout vous-même."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if membre.id == self.bot.user.id:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Je ne peux pas me mettre en timeout moi-même."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Vérification des rôles (seulement si interaction.user est Member)
            if isinstance(interaction.user, discord.Member):
                if membre.top_role >= interaction.user.top_role:
                    embed = creer_embed_erreur(
                        titre="Erreur",
                        description="Vous ne pouvez pas timeout un membre avec un rôle égal ou supérieur au vôtre."
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            # ── 🔹 Vérification de la durée (max 28 jours = 40320 minutes)
            if duree < 1 or duree > 40320:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="La durée doit être entre 1 minute et 40320 minutes (28 jours)."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Réponse différée
            await interaction.response.defer(ephemeral=True)

            try:
                # ── 🔹 Calcul de la durée
                duree_timedelta = timedelta(minutes=duree)

                # ── 🔹 Application du timeout
                await membre.timeout(
                    duree_timedelta,
                    reason=f"{raison} | Par {interaction.user}"
                )

                # ── 🔹 Formatage de la durée pour affichage
                jours, reste = divmod(duree, 1440)
                heures, minutes = divmod(reste, 60)

                duree_texte = []
                if jours > 0:
                    duree_texte.append(f"{jours}j")
                if heures > 0:
                    duree_texte.append(f"{heures}h")
                if minutes > 0:
                    duree_texte.append(f"{minutes}m")

                duree_affichage = " ".join(duree_texte)

                # ── 🔹 Confirmation
                embed = creer_embed_succes(
                    titre="Membre mis en timeout",
                    description=f"{config.EMOJI_SUCCES} **{membre.mention}** a été mis en timeout."
                )
                embed.add_field(name="Durée", value=duree_affichage, inline=True)
                embed.add_field(name="Raison", value=raison, inline=False)
                embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log de l'action
                self.bot.logger.info(
                    f"🔇 {membre} (ID: {membre.id}) mis en timeout par {interaction.user} | "
                    f"Durée : {duree_affichage} | Raison : {raison}"
                )

                # ── 🔹 Log Discord
                await log_timeout(
                    bot=self.bot,
                    guild=interaction.guild,
                    membre=membre,
                    moderateur=interaction.user,
                    duree=duree_affichage,
                    raison=raison
                )


            except discord.Forbidden:
                embed = creer_embed_erreur(
                    titre="Erreur de permissions",
                    description="Je n'ai pas la permission de mettre ce membre en timeout."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /timeout : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ ⚠️ Fonction 10 - Commande /warn
        # ║ Description : Donne un avertissement à un membre
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="warn",
            description="Donne un avertissement à un membre"
        )
        @app_commands.describe(
            membre="Le membre à avertir",
            raison="Raison de l'avertissement"
        )
        @app_commands.checks.has_permissions(moderate_members=True)
        async def warn(
            self,
            interaction: discord.Interaction,
            membre: discord.Member,
            raison: str
        ):
            """Donne un avertissement à un membre"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Vérifications de sécurité
            if membre.id == interaction.user.id:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Vous ne pouvez pas vous avertir vous-même."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if membre.id == self.bot.user.id:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Je ne peux pas m'avertir moi-même."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if isinstance(interaction.user, discord.Member):
                if membre.top_role >= interaction.user.top_role:
                    embed = creer_embed_erreur(
                        titre="Erreur",
                        description="Vous ne pouvez pas avertir un membre avec un rôle égal ou supérieur au vôtre."
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            # ── 🔹 Réponse différée
            await interaction.response.defer(ephemeral=True)

            try:
                import json
                from datetime import datetime

                # ── 🔹 Chargement des warns
                fichier_warns = "donnees/warns.json"

                try:
                    with open(fichier_warns, 'r', encoding='utf-8') as f:
                        warns = json.load(f)
                except FileNotFoundError:
                    warns = {}

                # ── 🔹 Création de l'ID du warn
                user_id_str = str(membre.id)
                if user_id_str not in warns:
                    warns[user_id_str] = []

                warn_id = len(warns[user_id_str]) + 1

                # ── 🔹 Ajout du warn
                nouveau_warn = {
                    "id": warn_id,
                    "raison": raison,
                    "moderateur": str(interaction.user),
                    "moderateur_id": interaction.user.id,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "serveur": interaction.guild.name
                }

                warns[user_id_str].append(nouveau_warn)

                # ── 🔹 Sauvegarde
                with open(fichier_warns, 'w', encoding='utf-8') as f:
                    json.dump(warns, f, indent=4, ensure_ascii=False)

                # ── 🔹 Envoi d'un MP au membre
                try:
                    embed_mp = creer_embed_avertissement(
                        titre="Avertissement reçu",
                        description=f"Vous avez reçu un avertissement sur **{interaction.guild.name}**."
                    )
                    embed_mp.add_field(name="Raison", value=raison, inline=False)
                    embed_mp.add_field(name="Modérateur", value=str(interaction.user), inline=True)
                    embed_mp.add_field(name="Total d'avertissements", value=str(len(warns[user_id_str])), inline=True)
                    await membre.send(embed=embed_mp)
                except discord.Forbidden:
                    pass

                # ── 🔹 Confirmation
                embed = creer_embed_succes(
                    titre="Avertissement donné",
                    description=f"{config.EMOJI_SUCCES} **{membre}** a reçu un avertissement."
                )
                embed.add_field(name="Raison", value=raison, inline=False)
                embed.add_field(name="Warn ID", value=f"#{warn_id}", inline=True)
                embed.add_field(name="Total", value=f"{len(warns[user_id_str])} warn(s)", inline=True)

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log
                self.bot.logger.info(
                    f"⚠️ Warn #{warn_id} donné à {membre} (ID: {membre.id}) par {interaction.user} | "
                    f"Raison : {raison} | Total : {len(warns[user_id_str])}"
                )

                # ── 🔹 Log Discord
                await log_warn(
                    bot=self.bot,
                    guild=interaction.guild,
                    membre=membre,
                    moderateur=interaction.user,
                    raison=raison,
                    warn_id=warn_id,
                    total=len(warns[user_id_str])
                )


            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /warn : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ 📋 Fonction 11 – Commande /warns
        # ║ Description : Affiche les warns d'un membre
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="warns",
            description="Affiche les avertissements d'un membre"
        )
        @app_commands.describe(membre="Le membre à consulter")
        @app_commands.checks.has_permissions(moderate_members=True)
        async def warns(
            self,
            interaction: discord.Interaction,
            membre: discord.Member
        ):
            """Affiche les warns d'un membre"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Réponse différée
            await interaction.response.defer(ephemeral=True)

            try:

                # ── 🔹 Chargement des warns
                fichier_warns = "donnees/warns.json"

                try:
                    with open(fichier_warns, 'r', encoding='utf-8') as f:
                        warns = json.load(f)
                except FileNotFoundError:
                    warns = {}

                user_id_str = str(membre.id)
                warns_membre = warns.get(user_id_str, [])

                # ── 🔹 Vérification
                if not warns_membre:
                    embed = creer_embed_succes(
                        titre="Aucun avertissement",
                        description=f"**{membre}** n'a aucun avertissement."
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return

                # ── 🔹 Création de l'embed
                embed = creer_embed(
                    titre=f"⚠️ Avertissements de {membre.name}",
                    description=f"**{len(warns_membre)}** avertissement(s) enregistré(s)",
                    couleur=config.COULEUR_AVERTISSEMENT
                )

                # ── 🔹 Affichage des warns (5 derniers max)
                warns_affiches = warns_membre[-5:] if len(warns_membre) > 5 else warns_membre

                for warn in warns_affiches:
                    embed.add_field(
                        name=f"Warn #{warn['id']} • {warn['date']}",
                        value=f"**Raison :** {warn['raison']}\n"
                              f"**Modérateur :** {warn['moderateur']}",
                        inline=False
                    )

                if len(warns_membre) > 5:
                    embed.set_footer(text=f"Affichage des 5 derniers warns sur {len(warns_membre)} total")

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log
                self.bot.logger.info(
                    f"📋 Warns consultés pour {membre} par {interaction.user} | Total : {len(warns_membre)}"
                )

            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /warns : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ ❌ Fonction 12 – Commande /unwarn
        # ║ Description : Retire un warn spécifique
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="unwarn",
            description="Retire un avertissement spécifique"
        )
        @app_commands.describe(
            membre="Le membre concerné",
            warn_id="L'ID du warn à retirer"
        )
        @app_commands.checks.has_permissions(moderate_members=True)
        async def unwarn(
            self,
            interaction: discord.Interaction,
            membre: discord.Member,
            warn_id: int
        ):
            """Retire un warn spécifique"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Réponse différée
            await interaction.response.defer(ephemeral=True)

            try:

                # ── 🔹 Chargement des warns
                fichier_warns = "donnees/warns.json"

                try:
                    with open(fichier_warns, 'r', encoding='utf-8') as f:
                        warns = json.load(f)
                except FileNotFoundError:
                    warns = {}

                user_id_str = str(membre.id)
                warns_membre = warns.get(user_id_str, [])

                # ── 🔹 Recherche du warn
                warn_trouve = None
                index_warn = None

                for index, warn in enumerate(warns_membre):
                    if warn['id'] == warn_id:
                        warn_trouve = warn
                        index_warn = index
                        break

                if not warn_trouve:
                    embed = creer_embed_erreur(
                        titre="Warn introuvable",
                        description=f"Le warn #{warn_id} n'existe pas pour **{membre}**."
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return

                # ── 🔹 Suppression du warn
                warns_membre.pop(index_warn)
                warns[user_id_str] = warns_membre

                # ── 🔹 Sauvegarde
                with open(fichier_warns, 'w', encoding='utf-8') as f:
                    json.dump(warns, f, indent=4, ensure_ascii=False)

                # ── 🔹 Confirmation
                embed = creer_embed_succes(
                    titre="Warn retiré",
                    description=f"{config.EMOJI_SUCCES} Le warn #{warn_id} de **{membre}** a été retiré."
                )
                embed.add_field(name="Raison du warn", value=warn_trouve['raison'], inline=False)
                embed.add_field(name="Warns restants", value=str(len(warns_membre)), inline=True)

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log
                self.bot.logger.info(
                    f"❌ Warn #{warn_id} retiré de {membre} par {interaction.user} | "
                    f"Restant : {len(warns_membre)}"
                )

            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /unwarn : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ 🗑️ Fonction 13 – Commande /clearwarns
        # ║ Description : Efface tous les warns d'un membre
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="clearwarns",
            description="Efface tous les avertissements d'un membre"
        )
        @app_commands.describe(
            membre="Le membre dont effacer les warns",
            raison="Raison de l'effacement (optionnel)"
        )
        @app_commands.checks.has_permissions(administrator=True)
        async def clearwarns(
            self,
            interaction: discord.Interaction,
            membre: discord.Member,
            raison: str = "Aucune raison fournie"
        ):
            """Efface tous les warns d'un membre"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 Réponse différée
            await interaction.response.defer(ephemeral=True)

            try:

                # ── 🔹 Chargement des warns
                fichier_warns = "donnees/warns.json"

                try:
                    with open(fichier_warns, 'r', encoding='utf-8') as f:
                        warns = json.load(f)
                except FileNotFoundError:
                    warns = {}

                user_id_str = str(membre.id)
                warns_membre = warns.get(user_id_str, [])

                # ── 🔹 Vérification
                if not warns_membre:
                    embed = creer_embed_erreur(
                        titre="Aucun warn",
                        description=f"**{membre}** n'a aucun avertissement à effacer."
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return

                nombre_warns = len(warns_membre)

                # ── 🔹 Effacement
                warns[user_id_str] = []

                # ── 🔹 Sauvegarde
                with open(fichier_warns, 'w', encoding='utf-8') as f:
                    json.dump(warns, f, indent=4, ensure_ascii=False)

                # ── 🔹 Confirmation
                embed = creer_embed_succes(
                    titre="Warns effacés",
                    description=f"{config.EMOJI_SUCCES} **{nombre_warns}** warn(s) de **{membre}** ont été effacés."
                )
                embed.add_field(name="Raison", value=raison, inline=False)
                embed.add_field(name="Modérateur", value=interaction.user.mention, inline=True)

                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 Log
                self.bot.logger.info(
                    f"🗑️ {nombre_warns} warns effacés pour {membre} par {interaction.user} | "
                    f"Raison : {raison}"
                )

            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /clearwarns : {e}")

        # ╔═════════════════════════════════════════════════════════════════════════
        # ║ 📊 Fonction 14 – Commande /setlogs
        # ║ Description : Configure le salon de logs
        # ║
        # ║ Pour obtenir l'ID d'un salon :
        # ║ 1. Active le Mode Développeur Discord (Paramètres > Avancés)
        # ║ 2. Clique droit sur le salon → Copier l'identifiant du salon
        # ║ 3. Utilise /setlogs #salon ou colle l'ID directement
        # ╚═════════════════════════════════════════════════════════════════════════
        @app_commands.command(
            name="setlogs",
            description="Configure le salon de logs du bot"
        )
        @app_commands.describe(salon="Le salon où envoyer les logs (laisser vide pour désactiver)")
        @app_commands.checks.has_permissions(administrator=True)
        async def setlogs(
            self,
            interaction: discord.Interaction,
            salon: discord.TextChannel | None = None
        ):
            """Configure le salon de logs"""

            # ── 🔹 Vérification que la commande est utilisée dans un serveur
            if not interaction.guild:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description="Cette commande ne peut être utilisée que dans un serveur."
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            try:
                if salon is None:
                    # ── 🔹 Désactivation
                    config.LOGS_CHANNEL_ID = 0

                    embed = creer_embed_succes(
                        titre="Logs désactivés",
                        description=f"{config.EMOJI_SUCCES} Le système de logs a été désactivé."
                    )
                else:
                    # ── 🔹 Configuration
                    config.LOGS_CHANNEL_ID = salon.id

                    embed = creer_embed_succes(
                        titre="Logs configurés",
                        description=f"{config.EMOJI_SUCCES} Les logs seront envoyés dans {salon.mention}."
                    )
                    embed.add_field(
                        name="📋 ID du salon",
                        value=f"`{salon.id}`",
                        inline=False
                    )

                    # ── 🔹 Message de test
                    from utilitaires.logs_discord import envoyer_log

                    await envoyer_log(
                        bot=self.bot,
                        guild=interaction.guild,
                        titre="✅ Logs activés",
                        description="Le système de logs est maintenant opérationnel !",
                        couleur=config.COULEUR_SUCCES,
                        champs=[
                            {"name": "Configuré par", "value": interaction.user.mention, "inline": True}
                        ]
                    )

                await interaction.response.send_message(embed=embed, ephemeral=True)

                # ── 🔹 Log
                self.bot.logger.info(
                    f"📊 Salon de logs configuré : {salon.name if salon else 'Désactivé'} par {interaction.user}"
                )

            except Exception as e:
                embed = creer_embed_erreur(
                    titre="Erreur",
                    description=f"Une erreur s'est produite : {str(e)}"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                self.bot.logger.error(f"❌ Erreur dans /setlogs : {e}")



    # ═══════════════════════════════════════════════════════════════════════════════
# ║ ⚙️ FONCTION SETUP
# ║ Description : Charge le cog dans le bot
# ═══════════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """Charge le cog des commandes administratives"""
    await bot.add_cog(CommandesAdmin(bot))





