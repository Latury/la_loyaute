from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ ⚙️ LA LOYAUTÉ - commandes_configuration.py
# ║
# ║ 🤖 Bot Discord privé développé en Python
# ║ 👨‍💻 Développé par Latury
# ║ 📦 Version : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

"""
⚙️ LA LOYAUTÉ - Commandes de Configuration
══════════════════════════════════════════════════════════════════════════════
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import json
from pathlib import Path
from datetime import datetime

from configuration import COULEUR_PRINCIPALE, COULEUR_SUCCES, COULEUR_ERREUR

# Import direct des utilitaires
from utilitaires.embeds_interactifs import (
    creer_embed_menu_principal,
    VueMenuPrincipal
)

# ═══════════════════════════════════════════════════════════════════════════════
# ║ ⚙️ CLASSE : CommandesConfiguration
# ║ 📝 Gestion complète des commandes de configuration du bot
# ═══════════════════════════════════════════════════════════════════════════════

class CommandesConfiguration(commands.Cog):
    """
    ⚙️ Cog contenant toutes les commandes de configuration du bot
    """

    def __init__(self, bot):
        """Initialise le cog de configuration"""
        self.bot = bot
        self.logger = bot.logger
        self.config_manager = bot.config_manager
        self.logger.info("✅ Module CommandesConfiguration chargé")

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ ⚙️ FONCTION 01 – /config
    # ║ ⚙️ Affiche le menu de configuration interactif avec Select Menu
    # ╚═════════════════════════════════════════════════════════════════════════

    @app_commands.command(name="config", description="⚙️ Ouvrir le menu de configuration interactif")
    @app_commands.checks.has_permissions(administrator=True)
    async def config(self, interaction: discord.Interaction):
        """Affiche le menu de configuration interactif"""
        try:
            # Vérifier que guild_id existe
            if not interaction.guild_id or not interaction.guild:
                await interaction.response.send_message(
                    "❌ Cette commande ne peut être utilisée qu'en serveur.",
                    ephemeral=True
                )
                return

            guild_id = interaction.guild_id

            # Créer l'embed du menu principal
            embed = creer_embed_menu_principal(guild_id)

            # Créer la vue avec le Select Menu
            view = VueMenuPrincipal(self.config_manager, guild_id)

            # Envoyer le message
            await interaction.response.send_message(
                embed=embed,
                view=view,
                ephemeral=True
            )

            self.logger.info(
                f"📊 Menu de configuration ouvert par {interaction.user} "
                f"sur {interaction.guild.name}"
            )

        except Exception as e:
            self.logger.error(f"❌ Erreur dans /config : {e}")
            await interaction.response.send_message(
                f"❌ Une erreur est survenue : {e}",
                ephemeral=True
            )

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📤 FONCTION 02 – /config-export
    # ║ 📤 Exporte la configuration actuelle en fichier JSON téléchargeable
    # ╚═════════════════════════════════════════════════════════════════════════

    @app_commands.command(name="config-export", description="📤 Exporter la configuration du serveur en JSON")
    @app_commands.checks.has_permissions(administrator=True)
    async def config_export(self, interaction: discord.Interaction):
        """Exporte la configuration actuelle du serveur"""
        try:
            await interaction.response.defer(ephemeral=True)

            # Vérifier que guild_id et guild existent
            if not interaction.guild_id or not interaction.guild:
                await interaction.followup.send(
                    "❌ Cette commande ne peut être utilisée qu'en serveur.",
                    ephemeral=True
                )
                return

            guild_id = interaction.guild_id
            config = self.config_manager.obtenir_configuration(guild_id)

            # Créer le fichier JSON
            nom_fichier = f"config_{interaction.guild.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            chemin_fichier = Path("temp") / nom_fichier

            # Créer le dossier temp s'il n'existe pas
            chemin_fichier.parent.mkdir(exist_ok=True)

            # Sauvegarder la configuration
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            # Créer l'embed
            embed = discord.Embed(
                title="📤 Export de Configuration",
                description=(
                    f"Configuration du serveur **{interaction.guild.name}** exportée avec succès !\n\n"
                    f"📄 **Fichier** : `{nom_fichier}`\n"
                    f"📊 **Éléments** : {len(config)} paramètres"
                ),
                color=COULEUR_SUCCES,
                timestamp=datetime.now()
            )

            # Envoyer le fichier
            await interaction.followup.send(
                embed=embed,
                file=discord.File(chemin_fichier, filename=nom_fichier),
                ephemeral=True
            )

            # Supprimer le fichier temporaire
            chemin_fichier.unlink()

            self.logger.info(
                f"📤 Configuration exportée par {interaction.user} "
                f"sur {interaction.guild.name}"
            )

        except Exception as e:
            self.logger.error(f"❌ Erreur dans /config-export : {e}")
            await interaction.followup.send(
                f"❌ Une erreur est survenue lors de l'export : {e}",
                ephemeral=True
            )

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📥 FONCTION 03 – /config-import
    # ║ 📥 Importe une configuration depuis un fichier JSON sauvegardé
    # ╚═════════════════════════════════════════════════════════════════════════

    @app_commands.command(name="config-import", description="📥 Importer une configuration depuis un fichier JSON")
    @app_commands.describe(fichier="Fichier JSON de configuration à importer")
    @app_commands.checks.has_permissions(administrator=True)
    async def config_import(
        self,
        interaction: discord.Interaction,
        fichier: discord.Attachment
    ):
        """Importe une configuration depuis un fichier JSON"""
        try:
            await interaction.response.defer(ephemeral=True)

            # Vérifier que guild_id existe
            if not interaction.guild_id:
                await interaction.followup.send(
                    "❌ Cette commande ne peut être utilisée qu'en serveur.",
                    ephemeral=True
                )
                return

            # Vérifier le type de fichier
            if not fichier.filename.endswith('.json'):
                await interaction.followup.send(
                    "❌ Le fichier doit être au format JSON (.json)",
                    ephemeral=True
                )
                return

            # Télécharger et lire le fichier
            contenu = await fichier.read()
            config_importee = json.loads(contenu.decode('utf-8'))

            # Valider la configuration
            if not isinstance(config_importee, dict):
                await interaction.followup.send(
                    "❌ Le fichier JSON est invalide (doit être un objet)",
                    ephemeral=True
                )
                return

            guild_id = interaction.guild_id

            # Sauvegarder l'ancienne configuration (backup)
            config_actuelle = self.config_manager.obtenir_configuration(guild_id)

            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="⚠️ Confirmation d'Import",
                description=(
                    "Vous êtes sur le point d'importer une nouvelle configuration.\n\n"
                    "**Cette action va remplacer la configuration actuelle !**\n\n"
                    f"📊 **Paramètres à importer** : {len(config_importee)}\n"
                    f"📊 **Paramètres actuels** : {len(config_actuelle)}\n\n"
                    "Voulez-vous continuer ?"
                ),
                color=COULEUR_PRINCIPALE,
                timestamp=datetime.now()
            )

            # Créer les boutons de confirmation
            view = ConfirmationImportView(
                self.config_manager,
                guild_id,
                config_importee,
                self.logger
            )

            await interaction.followup.send(
                embed=embed,
                view=view,
                ephemeral=True
            )

        except json.JSONDecodeError:
            await interaction.followup.send(
                "❌ Erreur : Le fichier JSON est mal formaté",
                ephemeral=True
            )
        except Exception as e:
            self.logger.error(f"❌ Erreur dans /config-import : {e}")
            await interaction.followup.send(
                f"❌ Une erreur est survenue lors de l'import : {e}",
                ephemeral=True
            )

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📊 FONCTION 04 – /config-logs-set
    # ║ 📊 Configure le salon Discord où envoyer tous les logs du bot
    # ╚═════════════════════════════════════════════════════════════════════════

    @app_commands.command(name="config-logs-set", description="📊 Définir le salon de logs Discord")
    @app_commands.describe(salon="Salon où envoyer les logs")
    @app_commands.checks.has_permissions(administrator=True)
    async def config_logs_set(
        self,
        interaction: discord.Interaction,
        salon: discord.TextChannel
    ):
        """Configure le salon de logs"""
        try:
            # Vérifier que guild_id et guild existent
            if not interaction.guild_id or not interaction.guild:
                await interaction.response.send_message(
                    "❌ Cette commande ne peut être utilisée qu'en serveur.",
                    ephemeral=True
                )
                return

            guild_id = interaction.guild_id

            # Enregistrer le salon
            self.config_manager.definir_salon_logs(guild_id, salon.id)

            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="✅ Salon de logs configuré",
                description=(
                    f"Le salon {salon.mention} a été défini comme salon de logs.\n\n"
                    "Tous les événements seront maintenant enregistrés dans ce salon."
                ),
                color=COULEUR_SUCCES,
                timestamp=datetime.now()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

            self.logger.info(
                f"📊 Salon de logs défini par {interaction.user} "
                f"sur {interaction.guild.name} : {salon.name}"
            )

        except Exception as e:
            self.logger.error(f"❌ Erreur dans /config-logs-set : {e}")
            await interaction.response.send_message(
                f"❌ Une erreur est survenue : {e}",
                ephemeral=True
            )

    @app_commands.command(name="config-logs-create", description="➕ Créer automatiquement un salon de logs privé")
    @app_commands.checks.has_permissions(administrator=True)
    async def config_logs_create(self, interaction: discord.Interaction):
        """Crée automatiquement un salon de logs privé"""
        try:
            await interaction.response.defer(ephemeral=True)

            # Vérifier que guild et guild_id existent
            if not interaction.guild or not interaction.guild_id:
                await interaction.followup.send(
                    "❌ Cette commande ne peut être utilisée qu'en serveur.",
                    ephemeral=True
                )
                return

            guild = interaction.guild
            guild_id = interaction.guild_id

            # Permissions : seuls les admins peuvent voir
            perm_default = discord.PermissionOverwrite()
            perm_default.read_messages = False

            perm_bot = discord.PermissionOverwrite()
            perm_bot.read_messages = True
            perm_bot.send_messages = True
            perm_bot.embed_links = True

            overwrites = {
                guild.default_role: perm_default,
                guild.me: perm_bot
            }

            # Ajouter les administrateurs
            for role in guild.roles:
                if role.permissions.administrator:
                    perm_admin = discord.PermissionOverwrite()
                    perm_admin.read_messages = True
                    overwrites[role] = perm_admin

            # Créer le salon
            salon = await guild.create_text_channel(
                name="🔒-logs",
                topic="📊 Logs automatiques du bot La Loyauté - Réservé aux administrateurs",
                overwrites=overwrites
            )

            # Enregistrer dans la config
            self.config_manager.definir_salon_logs(guild_id, salon.id)

            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="✅ Salon de logs créé",
                description=(
                    f"Le salon {salon.mention} a été créé avec succès !\n\n"
                    "📊 Les logs sont maintenant activés.\n"
                    "🔒 Seuls les administrateurs peuvent voir ce salon."
                ),
                color=COULEUR_SUCCES,
                timestamp=datetime.now()
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

            self.logger.info(
                f"➕ Salon de logs créé par {interaction.user} "
                f"sur {guild.name}"
            )

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions pour créer un salon.",
                ephemeral=True
            )
        except Exception as e:
            self.logger.error(f"❌ Erreur dans /config-logs-create : {e}")
            await interaction.followup.send(
                f"❌ Une erreur est survenue : {e}",
                ephemeral=True
            )

    @app_commands.command(name="config-logs-reset", description="🔴 Désactiver les logs Discord")
    @app_commands.checks.has_permissions(administrator=True)
    async def config_logs_reset(self, interaction: discord.Interaction):
        """Désactive les logs"""
        try:
            # Vérifier que guild_id et guild existent
            if not interaction.guild_id or not interaction.guild:
                await interaction.response.send_message(
                    "❌ Cette commande ne peut être utilisée qu'en serveur.",
                    ephemeral=True
                )
                return

            guild_id = interaction.guild_id

            # Désactiver les logs
            self.config_manager.definir_salon_logs(guild_id, None)

            # Créer l'embed de confirmation
            embed = discord.Embed(
                title="✅ Logs désactivés",
                description="Les logs Discord ont été désactivés avec succès.",
                color=COULEUR_SUCCES,
                timestamp=datetime.now()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

            self.logger.info(
                f"🔴 Logs désactivés par {interaction.user} "
                f"sur {interaction.guild.name}"
            )

        except Exception as e:
            self.logger.error(f"❌ Erreur dans /config-logs-reset : {e}")
            await interaction.response.send_message(
                f"❌ Une erreur est survenue : {e}",
                ephemeral=True
            )


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔘 CLASSE : ConfirmationImportView
# ║ 🔘 Vue avec boutons de confirmation pour l'import de configuration
# ═══════════════════════════════════════════════════════════════════════════════

class ConfirmationImportView(discord.ui.View):
    """Vue avec boutons de confirmation pour l'import"""

    def __init__(self, config_manager, guild_id: int, config_importee: dict, logger):
        super().__init__(timeout=60)
        self.config_manager = config_manager
        self.guild_id = guild_id
        self.config_importee = config_importee
        self.logger = logger

    @discord.ui.button(label="✅ Confirmer", style=discord.ButtonStyle.success)
    async def confirmer(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        """✅ Confirme l'import de la configuration"""
        try:
            # Sauvegarder la nouvelle configuration
            for cle, valeur in self.config_importee.items():
                self.config_manager.definir(self.guild_id, cle, valeur)

            # Créer l'embed de succès
            embed = discord.Embed(
                title="✅ Configuration Importée",
                description=(
                    f"La configuration a été importée avec succès !\n\n"
                    f"📊 **{len(self.config_importee)} paramètres** ont été appliqués."
                ),
                color=COULEUR_SUCCES,
                timestamp=datetime.now()
            )

            await interaction.response.edit_message(embed=embed, view=None)

            if interaction.guild:
                self.logger.info(
                    f"📥 Configuration importée par {interaction.user} "
                    f"sur {interaction.guild.name}"
                )

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'import : {e}")
            await interaction.response.send_message(
                f"❌ Erreur lors de l'import : {e}",
                ephemeral=True
            )

    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.danger)
    async def annuler(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        """❌ Annule l'import"""
        embed = discord.Embed(
            title="❌ Import Annulé",
            description="L'import de la configuration a été annulé.",
            color=COULEUR_ERREUR,
            timestamp=datetime.now()
        )
        await interaction.response.edit_message(embed=embed, view=None)


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔌 FONCTION SETUP
# ║ 🔌 Charge le cog des commandes de configuration dans le bot
# ═══════════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """Charge le cog des commandes de configuration"""
    await bot.add_cog(CommandesConfiguration(bot))
