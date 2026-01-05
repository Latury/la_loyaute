# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ ⚙️ LA LOYAUTÉ - COMMANDES DE CONFIGURATION
# ║
# ║ Commandes pour configurer le bot (salon de logs, etc.)
# ║ Développé par Latury
# ║ Version : 0.2.1
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from discord import app_commands
from discord.ext import commands
from utilitaires.helpers import creer_embed
import configuration as config


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📦 CLASSE PRINCIPALE
# ║ Description : Commandes de configuration du bot
# ═══════════════════════════════════════════════════════════════════════════════

class CommandesConfiguration(commands.Cog):
    """Commandes pour configurer le bot"""

    def __init__(self, bot):
        """
        Initialisation du cog CommandesConfiguration

        Args:
            bot: Instance du bot Discord
        """
        self.bot = bot
        self.bot.logger.info("⚙️ Module CommandesConfiguration chargé")


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🎯 GROUPE DE COMMANDES : /config
    # ║ Description : Groupe principal pour toutes les configurations
    # ═══════════════════════════════════════════════════════════════════════════

    config_group = app_commands.Group(
        name="config",
        description="Configuration du bot"
    )


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 📝 FONCTION 01 – Commande : /config logs-set
    # ║ Description : Définir le salon de logs
    # ═══════════════════════════════════════════════════════════════════════════

    @config_group.command(
        name="logs-set",
        description="Définir le salon où afficher les logs du bot"
    )
    @app_commands.describe(
        salon="Le salon textuel à utiliser pour les logs"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def config_logs_set(
        self,
        interaction: discord.Interaction,
        salon: discord.TextChannel
    ):
        """Définit le salon de logs"""
        try:
            # ── 🔹 ÉTAPE 0 : Vérifications de sécurité
            if not interaction.guild:
                return

            if not isinstance(interaction.user, discord.Member):
                return

            # ── 🔹 ÉTAPE 1 : Vérification des permissions
            if not interaction.user.guild_permissions.administrator:
                if not interaction.user.guild_permissions.manage_guild:
                    embed = creer_embed(
                        titre="❌ Permission refusée",
                        description="Vous devez être **administrateur** ou avoir la permission **Gérer le serveur**.",
                        couleur=config.COULEUR_ERREUR
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            # ── 🔹 ÉTAPE 2 : Vérifier que le salon est dans le même serveur
            if salon.guild.id != interaction.guild.id:
                embed = creer_embed(
                    titre="❌ Erreur",
                    description="Le salon doit être sur ce serveur !",
                    couleur=config.COULEUR_ERREUR
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 ÉTAPE 3 : Vérifier que le bot peut écrire dans ce salon
            permissions = salon.permissions_for(interaction.guild.me)
            if not permissions.send_messages or not permissions.embed_links:
                embed = creer_embed(
                    titre="❌ Permissions insuffisantes",
                    description=f"Je n'ai pas les permissions nécessaires dans {salon.mention}.\n\n"
                                f"**Permissions requises :**\n"
                                f"• Envoyer des messages\n"
                                f"• Intégrer des liens",
                    couleur=config.COULEUR_ERREUR
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 ÉTAPE 4 : Définir le salon de logs
            succes = self.bot.config_manager.definir_salon_logs(
                interaction.guild.id,
                salon.id
            )

            if succes:
                # ── 🔹 ÉTAPE 5 : Confirmation
                embed = creer_embed(
                    titre="✅ Salon de logs configuré",
                    description=f"Les logs seront maintenant envoyés dans {salon.mention}",
                    couleur=config.COULEUR_SUCCES
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

                # ── 🔹 ÉTAPE 6 : Message de test dans le salon de logs
                embed_test = creer_embed(
                    titre="🛡️ Salon de logs configuré",
                    description=f"Ce salon a été défini comme salon de logs par {interaction.user.mention}.\n\n"
                                f"Tous les événements importants du serveur seront enregistrés ici.",
                    couleur=config.COULEUR_INFO
                )
                await salon.send(embed=embed_test)

                # ── 🔹 ÉTAPE 7 : Log dans la console
                self.bot.logger.info(
                    f"⚙️ Config | "
                    f"Salon de logs défini : {salon.name} ({salon.id}) | "
                    f"Serveur : {interaction.guild.name} | "
                    f"Par : {interaction.user}"
                )

            else:
                embed = creer_embed(
                    titre="❌ Erreur",
                    description="Une erreur est survenue lors de la configuration.",
                    couleur=config.COULEUR_ERREUR
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            self.bot.logger.error(f"❌ Erreur dans config_logs_set : {e}")
            embed = creer_embed(
                titre="❌ Erreur",
                description="Une erreur inattendue s'est produite.",
                couleur=config.COULEUR_ERREUR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🏗️ FONCTION 02 – Commande : /config logs-create
    # ║ Description : Créer automatiquement un salon de logs
    # ═══════════════════════════════════════════════════════════════════════════

    @config_group.command(
        name="logs-create",
        description="Créer automatiquement un salon dédié aux logs"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def config_logs_create(self, interaction: discord.Interaction):
        """Crée automatiquement un salon de logs"""
        try:
            # ── 🔹 ÉTAPE 0 : Vérifications de sécurité
            if not interaction.guild:
                return

            if not isinstance(interaction.user, discord.Member):
                return

            # ── 🔹 ÉTAPE 1 : Vérification des permissions
            if not interaction.user.guild_permissions.administrator:
                if not interaction.user.guild_permissions.manage_guild:
                    embed = creer_embed(
                        titre="❌ Permission refusée",
                        description="Vous devez être **administrateur** ou avoir la permission **Gérer le serveur**.",
                        couleur=config.COULEUR_ERREUR
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            # ── 🔹 ÉTAPE 2 : Vérifier que le bot peut créer des salons
            if not interaction.guild.me.guild_permissions.manage_channels:
                embed = creer_embed(
                    titre="❌ Permissions insuffisantes",
                    description="Je n'ai pas la permission **Gérer les salons** sur ce serveur.",
                    couleur=config.COULEUR_ERREUR
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # ── 🔹 ÉTAPE 3 : Différer la réponse (création peut prendre du temps)
            await interaction.response.defer(ephemeral=True)

            # ── 🔹 ÉTAPE 4 : Créer le salon
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                ),
                interaction.guild.me: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                    embed_links=True
                )
            }

            salon = await interaction.guild.create_text_channel(
                name="📋-logs-bot",
                topic="Salon de logs automatique - Tous les événements du serveur sont enregistrés ici",
                overwrites=overwrites,
                reason=f"Création automatique par {interaction.user}"
            )

            # ── 🔹 ÉTAPE 5 : Définir comme salon de logs
            succes = self.bot.config_manager.definir_salon_logs(
                interaction.guild.id,
                salon.id
            )

            if succes:
                # ── 🔹 ÉTAPE 6 : Confirmation
                embed = creer_embed(
                    titre="✅ Salon de logs créé",
                    description=f"Le salon {salon.mention} a été créé et configuré !\n\n"
                                f"**Caractéristiques :**\n"
                                f"• Visible uniquement par les administrateurs\n"
                                f"• Tous les événements y seront enregistrés\n"
                                f"• Peut être personnalisé selon vos besoins",
                    couleur=config.COULEUR_SUCCES
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

                # ── 🔹 ÉTAPE 7 : Message de bienvenue dans le salon
                embed_bienvenue = creer_embed(
                    titre="🛡️ Salon de logs activé",
                    description=f"Ce salon a été créé automatiquement par {interaction.user.mention}.\n\n"
                                f"**📊 Ce qui sera enregistré ici :**\n"
                                f"• Messages supprimés ou modifiés\n"
                                f"• Membres rejoignant ou quittant\n"
                                f"• Changements de rôles\n"
                                f"• Salons créés ou supprimés\n"
                                f"• Actions de modération (kick, ban, warn, etc.)\n\n"
                                f"Vous pouvez personnaliser les permissions de ce salon selon vos besoins.",
                    couleur=config.COULEUR_INFO
                )
                await salon.send(embed=embed_bienvenue)

                # ── 🔹 ÉTAPE 8 : Log dans la console
                self.bot.logger.info(
                    f"⚙️ Config | "
                    f"Salon de logs créé : {salon.name} ({salon.id}) | "
                    f"Serveur : {interaction.guild.name} | "
                    f"Par : {interaction.user}"
                )

            else:
                # Si échec de la config, supprimer le salon créé
                await salon.delete(reason="Échec de la configuration")
                embed = creer_embed(
                    titre="❌ Erreur",
                    description="Une erreur est survenue lors de la configuration.",
                    couleur=config.COULEUR_ERREUR
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            self.bot.logger.error(f"❌ Erreur dans config_logs_create : {e}")
            embed = creer_embed(
                titre="❌ Erreur",
                description="Une erreur inattendue s'est produite.",
                couleur=config.COULEUR_ERREUR
            )

            # Vérifier si on doit utiliser followup ou response
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🔍 FONCTION 03 – Commande : /config logs-show
    # ║ Description : Afficher la configuration actuelle
    # ═══════════════════════════════════════════════════════════════════════════

    @config_group.command(
        name="logs-show",
        description="Afficher la configuration actuelle des logs"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def config_logs_show(self, interaction: discord.Interaction):
        """Affiche la configuration actuelle des logs"""
        try:
            # ── 🔹 ÉTAPE 0 : Vérifications de sécurité
            if not interaction.guild:
                return

            # ── 🔹 ÉTAPE 1 : Récupérer la config
            salon_id = self.bot.config_manager.obtenir_salon_logs(interaction.guild.id)

            # ── 🔹 ÉTAPE 2 : Vérifier si configuré
            if salon_id:
                salon = interaction.guild.get_channel(salon_id)

                if salon:
                    embed = creer_embed(
                        titre="📋 Configuration des logs",
                        description=f"**Salon de logs actuel :**\n{salon.mention}\n\n"
                                    f"**ID du salon :** `{salon_id}`\n"
                                    f"**Statut :** ✅ Actif",
                        couleur=config.COULEUR_SUCCES
                    )
                else:
                    # Salon supprimé mais toujours en config
                    embed = creer_embed(
                        titre="⚠️ Configuration des logs",
                        description=f"**Salon de logs configuré :** `{salon_id}`\n\n"
                                    f"**⚠️ Attention :** Le salon n'existe plus !\n"
                                    f"Utilisez `/config logs-reset` puis reconfigurez un nouveau salon.",
                        couleur=config.COULEUR_AVERTISSEMENT
                    )
            else:
                embed = creer_embed(
                    titre="📋 Configuration des logs",
                    description="**Statut :** ❌ Aucun salon de logs configuré\n\n"
                                f"**Pour configurer :**\n"
                                f"• `/config logs-set #salon` - Définir un salon existant\n"
                                f"• `/config logs-create` - Créer un nouveau salon automatiquement",
                    couleur=config.COULEUR_INFO
                )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            self.bot.logger.error(f"❌ Erreur dans config_logs_show : {e}")
            embed = creer_embed(
                titre="❌ Erreur",
                description="Une erreur inattendue s'est produite.",
                couleur=config.COULEUR_ERREUR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🗑️ FONCTION 04 – Commande : /config logs-reset
    # ║ Description : Réinitialiser la configuration des logs
    # ═══════════════════════════════════════════════════════════════════════════

    @config_group.command(
        name="logs-reset",
        description="Désactiver les logs (réinitialiser la configuration)"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def config_logs_reset(self, interaction: discord.Interaction):
        """Réinitialise la configuration des logs"""
        try:
            # ── 🔹 ÉTAPE 0 : Vérifications de sécurité
            if not interaction.guild:
                return

            if not isinstance(interaction.user, discord.Member):
                return

            # ── 🔹 ÉTAPE 1 : Vérification des permissions
            if not interaction.user.guild_permissions.administrator:
                if not interaction.user.guild_permissions.manage_guild:
                    embed = creer_embed(
                        titre="❌ Permission refusée",
                        description="Vous devez être **administrateur** ou avoir la permission **Gérer le serveur**.",
                        couleur=config.COULEUR_ERREUR
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

            # ── 🔹 ÉTAPE 2 : Réinitialiser
            succes = self.bot.config_manager.reinitialiser_salon_logs(interaction.guild.id)

            if succes:
                embed = creer_embed(
                    titre="✅ Configuration réinitialisée",
                    description="Les logs ont été désactivés.\n\n"
                                f"Pour réactiver :\n"
                                f"• `/config logs-set #salon`\n"
                                f"• `/config logs-create`",
                    couleur=config.COULEUR_SUCCES
                )

                # ── 🔹 ÉTAPE 3 : Log dans la console
                self.bot.logger.info(
                    f"⚙️ Config | "
                    f"Salon de logs réinitialisé | "
                    f"Serveur : {interaction.guild.name} | "
                    f"Par : {interaction.user}"
                )
            else:
                embed = creer_embed(
                    titre="⚠️ Information",
                    description="Aucune configuration à réinitialiser.",
                    couleur=config.COULEUR_AVERTISSEMENT
                )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            self.bot.logger.error(f"❌ Erreur dans config_logs_reset : {e}")
            embed = creer_embed(
                titre="❌ Erreur",
                description="Une erreur inattendue s'est produite.",
                couleur=config.COULEUR_ERREUR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔧 FONCTION SETUP
# ║ Description : Fonction requise pour charger le cog dans le bot
# ═══════════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """
    Charge le cog CommandesConfiguration dans le bot

    Args:
        bot: Instance du bot Discord
    """
    await bot.add_cog(CommandesConfiguration(bot))


# ═══════════════════════════════════════════════════════════════════════════════
# FIN DU FICHIER commandes_configuration.py
# ═══════════════════════════════════════════════════════════════════════════════
