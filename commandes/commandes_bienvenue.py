# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🦁 LA LOYAUTÉ - commandes_bienvenue.py
# ║
# ║ ⚙️ Configuration du système de bienvenue/départ
# ║ 👨‍💻 Développé par Latury
# ║ 📦 Version : 0.3.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

"""
⚙️ Commandes de configuration du système de bienvenue/départ
══════════════════════════════════════════════════════════════════════════════
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from pathlib import Path
import json
import configuration as config
from utilitaires.logger import creer_logger

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📁 CONFIGURATION DES FICHIERS
# ╚══════════════════════════════════════════════════════════════════════════════

DONNEES_DIR = Path("donnees")
CONFIG_FILE = DONNEES_DIR / "bienvenue_config.json"

# ═══════════════════════════════════════════════════════════════════════════════
# ║ ⚙️ COG PRINCIPAL - CommandesBienvenue
# ╚══════════════════════════════════════════════════════════════════════════════

class CommandesBienvenue(commands.Cog):
    """Commandes de gestion du système de bienvenue et départ"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = creer_logger("commandes_bienvenue", config.NIVEAU_LOG)

    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 📂 GESTION DE LA CONFIGURATION
    # ╚══════════════════════════════════════════════════════════════════════════

    def charger_config(self):
        """Charge la configuration depuis le fichier JSON"""
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur chargement config: {e}")
            return None

    def sauvegarder_config(self, config_data):
        """Sauvegarde la configuration"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde config: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🎉 GROUPE DE COMMANDES : /bienvenue
    # ╚══════════════════════════════════════════════════════════════════════════

    bienvenue_group = app_commands.Group(
        name="bienvenue",
        description="⚙️ Configuration du système de bienvenue/départ"
    )

    # ─────────────────────────────────────────────────────────────────────────
    # 📊 COMMANDE : /bienvenue status
    # ─────────────────────────────────────────────────────────────────────────

    @bienvenue_group.command(
        name="status",
        description="📊 Affiche la configuration actuelle du système"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def bienvenue_status(self, interaction: discord.Interaction):
        """Affiche la configuration actuelle"""
        conf = self.charger_config()

        if not conf or "bienvenue" not in conf or "depart" not in conf:
            await interaction.response.send_message(
                "❌ Erreur lors du chargement de la configuration",
                ephemeral=True
            )
            return

        # Création de l'embed
        embed = discord.Embed(
            title="⚙️ Configuration Bienvenue/Départ",
            color=config.COULEUR_INFO,
            timestamp=discord.utils.utcnow()
        )

        # Section Bienvenue
        bienvenue = conf["bienvenue"]
        statut_bienvenue = "🟢 Activé" if bienvenue.get("active") else "🔴 Désactivé"
        salon_bienvenue = f"<#{bienvenue['salon_id']}>" if bienvenue.get('salon_id') else "Non configuré"
        role_auto = f"<@&{bienvenue['role_auto_id']}>" if bienvenue.get('role_auto_id') else "Aucun"
        message_bv = bienvenue.get('message', '')[:50] if bienvenue.get('message') else 'Non défini'

        embed.add_field(
            name="🎉 Système de bienvenue",
            value=(
                f"**Statut :** {statut_bienvenue}\n"
                f"**Salon :** {salon_bienvenue}\n"
                f"**Rôle auto :** {role_auto}\n"
                f"**Message :** `{message_bv}...`"
            ),
            inline=False
        )

        # Section Départ
        depart = conf["depart"]
        statut_depart = "🟢 Activé" if depart.get("active") else "🔴 Désactivé"
        salon_depart = f"<#{depart['salon_id']}>" if depart.get('salon_id') else "Non configuré"
        message_dep = depart.get('message', '')[:50] if depart.get('message') else 'Non défini'

        embed.add_field(
            name="👋 Système de départ",
            value=(
                f"**Statut :** {statut_depart}\n"
                f"**Salon :** {salon_depart}\n"
                f"**Message :** `{message_dep}...`"
            ),
            inline=False
        )

        embed.set_footer(text=f"Demandé par {interaction.user.name}")
        await interaction.response.send_message(embed=embed)
        self.logger.info(f"Status affiché par {interaction.user.name}")

    # ─────────────────────────────────────────────────────────────────────────
    # ⚙️ COMMANDE : /bienvenue activer
    # ─────────────────────────────────────────────────────────────────────────

    @bienvenue_group.command(
        name="activer",
        description="✅ Active le système de bienvenue"
    )
    @app_commands.describe(salon="Le salon où envoyer les messages de bienvenue")
    @app_commands.checks.has_permissions(administrator=True)
    async def bienvenue_activer(
        self,
        interaction: discord.Interaction,
        salon: discord.TextChannel
    ):
        """Active le système de bienvenue"""
        conf = self.charger_config()

        if not conf or "bienvenue" not in conf:
            await interaction.response.send_message(
                "❌ Erreur lors du chargement de la configuration",
                ephemeral=True
            )
            return

        # Mise à jour de la config
        conf["bienvenue"]["active"] = True
        conf["bienvenue"]["salon_id"] = salon.id

        if self.sauvegarder_config(conf):
            embed = discord.Embed(
                title="✅ Système de bienvenue activé",
                description=(
                    f"Les messages de bienvenue seront envoyés dans {salon.mention}\n\n"
                    f"**Configuration :**\n"
                    f"• Salon : {salon.mention}\n"
                    f"• Embed : Oui\n"
                    f"• Message : `{conf['bienvenue'].get('message', 'Message par défaut')}`"
                ),
                color=config.COULEUR_SUCCES
            )
            await interaction.response.send_message(embed=embed)
            self.logger.info(f"Bienvenue activé par {interaction.user.name} dans #{salon.name}")
        else:
            await interaction.response.send_message(
                "❌ Erreur lors de la sauvegarde",
                ephemeral=True
            )

    # ─────────────────────────────────────────────────────────────────────────
    # 🔴 COMMANDE : /bienvenue desactiver
    # ─────────────────────────────────────────────────────────────────────────

    @bienvenue_group.command(
        name="desactiver",
        description="❌ Désactive le système de bienvenue"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def bienvenue_desactiver(self, interaction: discord.Interaction):
        """Désactive le système de bienvenue"""
        conf = self.charger_config()

        if not conf or "bienvenue" not in conf:
            await interaction.response.send_message(
                "❌ Erreur lors du chargement de la configuration",
                ephemeral=True
            )
            return

        conf["bienvenue"]["active"] = False

        if self.sauvegarder_config(conf):
            embed = discord.Embed(
                title="🔴 Système de bienvenue désactivé",
                description="Les messages de bienvenue ne seront plus envoyés.",
                color=config.COULEUR_AVERTISSEMENT
            )
            await interaction.response.send_message(embed=embed)
            self.logger.info(f"Bienvenue désactivé par {interaction.user.name}")
        else:
            await interaction.response.send_message(
                "❌ Erreur lors de la sauvegarde",
                ephemeral=True
            )

    # ─────────────────────────────────────────────────────────────────────────
    # ✏️ COMMANDE : /bienvenue message
    # ─────────────────────────────────────────────────────────────────────────

    @bienvenue_group.command(
        name="message",
        description="✏️ Personnalise le message de bienvenue"
    )
    @app_commands.describe(message="Le nouveau message (Variables: {mention}, {username}, {serveur}, {compteur})")
    @app_commands.checks.has_permissions(administrator=True)
    async def bienvenue_message(
        self,
        interaction: discord.Interaction,
        message: str
    ):
        """Personnalise le message de bienvenue"""
        conf = self.charger_config()

        if not conf or "bienvenue" not in conf:
            await interaction.response.send_message(
                "❌ Erreur lors du chargement de la configuration",
                ephemeral=True
            )
            return

        conf["bienvenue"]["message"] = message

        if self.sauvegarder_config(conf):
            embed = discord.Embed(
                title="✅ Message de bienvenue modifié",
                description=f"**Nouveau message :**\n{message}",
                color=config.COULEUR_SUCCES
            )

            embed.add_field(
                name="📝 Variables disponibles",
                value=(
                    "`{mention}` - Mention du membre\n"
                    "`{username}` - Nom du membre\n"
                    "`{serveur}` - Nom du serveur\n"
                    "`{compteur}` - Nombre de membres"
                ),
                inline=False
            )

            await interaction.response.send_message(embed=embed)
            self.logger.info(f"Message de bienvenue modifié par {interaction.user.name}")
        else:
            await interaction.response.send_message(
                "❌ Erreur lors de la sauvegarde",
                ephemeral=True
            )

    # ─────────────────────────────────────────────────────────────────────────
    # 🎭 COMMANDE : /bienvenue role
    # ─────────────────────────────────────────────────────────────────────────

    @bienvenue_group.command(
        name="role",
        description="🎭 Définit un rôle automatique pour les nouveaux membres"
    )
    @app_commands.describe(role="Le rôle à attribuer automatiquement (laisser vide pour désactiver)")
    @app_commands.checks.has_permissions(administrator=True)
    async def bienvenue_role(
        self,
        interaction: discord.Interaction,
        role: Optional[discord.Role] = None
    ):
        """Configure le rôle automatique"""
        conf = self.charger_config()

        if not conf or "bienvenue" not in conf:
            await interaction.response.send_message(
                "❌ Erreur lors du chargement de la configuration",
                ephemeral=True
            )
            return

        if role:
            conf["bienvenue"]["role_auto_id"] = role.id
            description = f"Le rôle {role.mention} sera attribué automatiquement aux nouveaux membres."
            titre = "✅ Rôle automatique configuré"
            couleur = config.COULEUR_SUCCES
        else:
            conf["bienvenue"]["role_auto_id"] = None
            description = "Le rôle automatique a été désactivé."
            titre = "🔴 Rôle automatique désactivé"
            couleur = config.COULEUR_AVERTISSEMENT

        if self.sauvegarder_config(conf):
            embed = discord.Embed(
                title=titre,
                description=description,
                color=couleur
            )
            await interaction.response.send_message(embed=embed)
            self.logger.info(f"Rôle auto configuré par {interaction.user.name}: {role.name if role else 'Aucun'}")
        else:
            await interaction.response.send_message(
                "❌ Erreur lors de la sauvegarde",
                ephemeral=True
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 👋 GROUPE DE COMMANDES : /depart
    # ╚══════════════════════════════════════════════════════════════════════════

    depart_group = app_commands.Group(
        name="depart",
        description="⚙️ Configuration des messages de départ"
    )

    # ─────────────────────────────────────────────────────────────────────────
    # ⚙️ COMMANDE : /depart activer
    # ─────────────────────────────────────────────────────────────────────────

    @depart_group.command(
        name="activer",
        description="✅ Active le système de messages de départ"
    )
    @app_commands.describe(salon="Le salon où envoyer les messages de départ")
    @app_commands.checks.has_permissions(administrator=True)
    async def depart_activer(
        self,
        interaction: discord.Interaction,
        salon: discord.TextChannel
    ):
        """Active le système de départ"""
        conf = self.charger_config()

        if not conf or "depart" not in conf:
            await interaction.response.send_message(
                "❌ Erreur lors du chargement de la configuration",
                ephemeral=True
            )
            return

        conf["depart"]["active"] = True
        conf["depart"]["salon_id"] = salon.id

        if self.sauvegarder_config(conf):
            embed = discord.Embed(
                title="✅ Système de départ activé",
                description=f"Les messages de départ seront envoyés dans {salon.mention}",
                color=config.COULEUR_SUCCES
            )
            await interaction.response.send_message(embed=embed)
            self.logger.info(f"Départ activé par {interaction.user.name} dans #{salon.name}")
        else:
            await interaction.response.send_message(
                "❌ Erreur lors de la sauvegarde",
                ephemeral=True
            )

    # ─────────────────────────────────────────────────────────────────────────
    # 🔴 COMMANDE : /depart desactiver
    # ─────────────────────────────────────────────────────────────────────────

    @depart_group.command(
        name="desactiver",
        description="❌ Désactive le système de messages de départ"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def depart_desactiver(self, interaction: discord.Interaction):
        """Désactive le système de départ"""
        conf = self.charger_config()

        if not conf or "depart" not in conf:
            await interaction.response.send_message(
                "❌ Erreur lors du chargement de la configuration",
                ephemeral=True
            )
            return

        conf["depart"]["active"] = False

        if self.sauvegarder_config(conf):
            embed = discord.Embed(
                title="🔴 Système de départ désactivé",
                description="Les messages de départ ne seront plus envoyés.",
                color=config.COULEUR_AVERTISSEMENT
            )
            await interaction.response.send_message(embed=embed)
            self.logger.info(f"Départ désactivé par {interaction.user.name}")
        else:
            await interaction.response.send_message(
                "❌ Erreur lors de la sauvegarde",
                ephemeral=True
            )

    # ─────────────────────────────────────────────────────────────────────────
    # ✏️ COMMANDE : /depart message
    # ─────────────────────────────────────────────────────────────────────────

    @depart_group.command(
        name="message",
        description="✏️ Personnalise le message de départ"
    )
    @app_commands.describe(message="Le nouveau message (Variables: {username}, {serveur}, {jours}, {compteur})")
    @app_commands.checks.has_permissions(administrator=True)
    async def depart_message(
        self,
        interaction: discord.Interaction,
        message: str
    ):
        """Personnalise le message de départ"""
        conf = self.charger_config()

        if not conf or "depart" not in conf:
            await interaction.response.send_message(
                "❌ Erreur lors du chargement de la configuration",
                ephemeral=True
            )
            return

        conf["depart"]["message"] = message

        if self.sauvegarder_config(conf):
            embed = discord.Embed(
                title="✅ Message de départ modifié",
                description=f"**Nouveau message :**\n{message}",
                color=config.COULEUR_SUCCES
            )

            embed.add_field(
                name="📝 Variables disponibles",
                value=(
                    "`{username}` - Nom du membre\n"
                    "`{serveur}` - Nom du serveur\n"
                    "`{jours}` - Jours passés sur le serveur\n"
                    "`{compteur}` - Nombre de membres restants"
                ),
                inline=False
            )

            await interaction.response.send_message(embed=embed)
            self.logger.info(f"Message de départ modifié par {interaction.user.name}")
        else:
            await interaction.response.send_message(
                "❌ Erreur lors de la sauvegarde",
                ephemeral=True
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # ║ ⚠️ GESTION DES ERREURS
    # ╚══════════════════════════════════════════════════════════════════════════

    @bienvenue_status.error
    @bienvenue_activer.error
    @bienvenue_desactiver.error
    @bienvenue_message.error
    @bienvenue_role.error
    @depart_activer.error
    @depart_desactiver.error
    @depart_message.error
    async def commande_error(self, interaction: discord.Interaction, error):
        """Gestion des erreurs des commandes"""
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                "❌ Vous devez être administrateur pour utiliser cette commande",
                ephemeral=True
            )
        else:
            self.logger.error(f"Erreur commande: {error}")
            await interaction.response.send_message(
                "❌ Une erreur s'est produite",
                ephemeral=True
            )

# ══════════════════════════════════════════════════════════════════════════
# ║ ⚙️ SETUP DU COG
# ══════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """Charge le cog CommandesBienvenue"""
    await bot.add_cog(CommandesBienvenue(bot))
