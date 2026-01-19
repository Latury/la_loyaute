"""
═══════════════════════════════════════════════════════════════
FICHIER : commandes/commandes_interface.py
MODULE : Commandes Interface Interactive
DESCRIPTION : Cog pour le panneau de configuration interactif
AUTEUR : Latury
DATE : 19/01/2026
VERSION : 0.3.0
═══════════════════════════════════════════════════════════════
"""

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Select
from typing import Dict, Optional
import json
from io import BytesIO
import configuration as config
from utilitaires.helpers import creer_embed

# ═══════════════════════════════════════════════════════════════
# 📦 SESSION DE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

class SessionConfiguration:
    """Représente une session de configuration interactive"""

    def __init__(self, guild_id: int, user_id: int):
        self.guild_id = guild_id
        self.user_id = user_id
        self.current_category: Optional[str] = None
        self.modifications: Dict = {}

    def set_category(self, category: str):
        """Définit la catégorie active"""
        self.current_category = category

    def add_modification(self, key: str, value):
        """Enregistre une modification"""
        self.modifications[key] = value

# ═══════════════════════════════════════════════════════════════
# 🎨 GESTIONNAIRE D'INTERFACE
# ═══════════════════════════════════════════════════════════════

class GestionnaireInterface:
    """Gère les sessions d'interface interactive"""

    def __init__(self, bot):
        self.bot = bot
        self.sessions: Dict[int, SessionConfiguration] = {}

    def creer_session(self, guild_id: int, user_id: int) -> SessionConfiguration:
        """Crée une nouvelle session de configuration"""
        session = SessionConfiguration(guild_id, user_id)
        self.sessions[guild_id] = session
        return session

    def obtenir_session(self, guild_id: int) -> Optional[SessionConfiguration]:
        """Récupère une session existante"""
        return self.sessions.get(guild_id)

    def fermer_session(self, guild_id: int):
        """Ferme une session de configuration"""
        if guild_id in self.sessions:
            del self.sessions[guild_id]

# ═══════════════════════════════════════════════════════════════
# 📋 VUE MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════

class MenuPrincipalView(View):
    """Vue du menu principal avec Select Menu"""

    def __init__(self, session: SessionConfiguration):
        super().__init__(timeout=300)
        self.session = session

        # Créer le Select Menu
        self.select_menu = Select(
            placeholder="🎨 Choisissez une catégorie",
            options=[
                discord.SelectOption(
                    label="Logs",
                    description="Configuration des logs du serveur",
                    emoji="📊",
                    value="logs"
                ),
                discord.SelectOption(
                    label="Bienvenue",
                    description="Messages d'arrivée et de départ",
                    emoji="👋",
                    value="bienvenue"
                ),
                discord.SelectOption(
                    label="Modération",
                    description="Paramètres de modération",
                    emoji="🛡️",
                    value="moderation"
                ),
                discord.SelectOption(
                    label="Auto-rôles",
                    description="Attribution automatique de rôles",
                    emoji="🎭",
                    value="autoroles"
                ),
                discord.SelectOption(
                    label="Informations",
                    description="Informations sur le bot",
                    emoji="ℹ️",
                    value="infos"
                )
            ]
        )

        self.select_menu.callback = self.select_callback
        self.add_item(self.select_menu)

    async def select_callback(self, interaction: discord.Interaction):
        """Callback lors de la sélection d'une catégorie"""
        # Accès direct aux valeurs du Select Menu
        if not self.select_menu.values:
            return

        selected_value = self.select_menu.values[0]
        self.session.set_category(selected_value)

        # Créer l'embed correspondant à la catégorie
        embed = creer_embed_categorie(selected_value, self.session)
        await interaction.response.edit_message(embed=embed, view=self)

# ═══════════════════════════════════════════════════════════════
# 🎨 FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════

def creer_embed_principal(session: SessionConfiguration) -> discord.Embed:
    """Crée l'embed du menu principal"""
    embed = creer_embed(
        titre="🎨 Panneau de Configuration Interactif",
        description="Bienvenue dans le panneau de configuration moderne !\n"
                   "Utilisez le menu déroulant ci-dessous pour naviguer.",
        couleur=config.COULEUR_PRINCIPALE
    )

    embed.add_field(
        name="📊 Catégories disponibles",
        value=(
            "• **Logs** - Configuration des journaux\n"
            "• **Bienvenue** - Messages d'arrivée/départ\n"
            "• **Modération** - Outils de modération\n"
            "• **Auto-rôles** - Attribution automatique\n"
            "• **Informations** - À propos du bot"
        ),
        inline=False
    )

    embed.set_footer(text="💡 Sélectionnez une catégorie pour commencer")
    return embed

def creer_embed_categorie(categorie: str, session: SessionConfiguration) -> discord.Embed:
    """Crée l'embed pour une catégorie spécifique"""
    embeds = {
        "logs": {
            "titre": "📊 Configuration des Logs",
            "description": "Configurez les journaux de votre serveur",
            "champs": [
                {
                    "name": "📝 Événements enregistrés",
                    "value": "• Arrivées/Départs\n• Messages modifiés\n• Actions de modération",
                    "inline": False
                }
            ]
        },
        "bienvenue": {
            "titre": "👋 Configuration Bienvenue",
            "description": "Messages d'arrivée et de départ",
            "champs": [
                {
                    "name": "📥 Messages de bienvenue",
                    "value": "Personnalisez l'accueil des nouveaux membres",
                    "inline": False
                }
            ]
        },
        "moderation": {
            "titre": "🛡️ Configuration Modération",
            "description": "Outils de modération du serveur",
            "champs": [
                {
                    "name": "⚔️ Commandes disponibles",
                    "value": "kick, ban, timeout, warn, clear",
                    "inline": False
                }
            ]
        },
        "autoroles": {
            "titre": "🎭 Configuration Auto-rôles",
            "description": "Attribution automatique de rôles",
            "champs": [
                {
                    "name": "🤖 Fonctionnalités",
                    "value": "Rôles automatiques à l'arrivée",
                    "inline": False
                }
            ]
        },
        "infos": {
            "titre": "ℹ️ Informations du Bot",
            "description": "Détails et statistiques",
            "champs": [
                {
                    "name": "📦 Version",
                    "value": "v0.3.0",
                    "inline": True
                }
            ]
        }
    }

    data = embeds.get(categorie, embeds["logs"])

    embed = creer_embed(
        titre=data["titre"],
        description=data["description"],
        couleur=config.COULEUR_INFO
    )

    for champ in data["champs"]:
        embed.add_field(
            name=champ["name"],
            value=champ["value"],
            inline=champ.get("inline", False)
        )

    embed.set_footer(text="💡 Utilisez le menu pour changer de catégorie")
    return embed

# ═══════════════════════════════════════════════════════════════
# ⚙️ COG COMMANDES INTERFACE
# ═══════════════════════════════════════════════════════════════

class CommandesInterface(commands.Cog):
    """
    🎨 Cog pour les commandes d'interface interactive
    Gère le menu de configuration visuel avec Select Menu et boutons
    """

    def __init__(self, bot):
        """Initialise le cog avec le gestionnaire d'interface"""
        self.bot = bot
        self.gestionnaire = GestionnaireInterface(bot)

    @app_commands.command(name="panel", description="🎨 Ouvre le panneau de configuration interactif")
    @app_commands.checks.has_permissions(administrator=True)
    async def panel_interactif(self, interaction: discord.Interaction):
        """
        Ouvre le panneau de configuration interactif

        Affiche un menu avec Select Menu Discord permettant de naviguer
        entre les différentes catégories de configuration.

        Permissions requises: Administrateur
        """
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Cette commande doit être utilisée dans un serveur.",
                ephemeral=True
            )
            return

        session = self.gestionnaire.creer_session(
            interaction.guild.id,
            interaction.user.id
        )

        embed = creer_embed_principal(session)
        view = MenuPrincipalView(session)

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )

    @app_commands.command(name="panel-export", description="💾 Exporte la configuration du serveur en JSON")
    @app_commands.checks.has_permissions(administrator=True)
    async def panel_export(self, interaction: discord.Interaction):
        """
        Exporte la configuration actuelle en fichier JSON

        Permissions requises: Administrateur
        """
        # ✅ Vérification que la commande est utilisée dans un serveur
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Cette commande doit être utilisée dans un serveur.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            config_manager = self.bot.config_manager
            config_data = config_manager.obtenir_configuration(interaction.guild.id)

            json_data = json.dumps(config_data, indent=4, ensure_ascii=False)

            file = discord.File(
                BytesIO(json_data.encode()),
                filename=f"config_{interaction.guild.id}.json"
            )

            await interaction.followup.send(
                "📦 **Configuration exportée avec succès !**\n\n"
                "💾 Conservez ce fichier en lieu sûr.\n"
                "📥 Utilisez `/panel-import` pour restaurer cette configuration.",
                file=file,
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(
                f"❌ **Erreur lors de l'export**\n\n"
                f"Détails : `{str(e)}`",
                ephemeral=True
            )

# ═══════════════════════════════════════════════════════════════
# 🚀 FONCTION SETUP - Chargement du cog
# ═══════════════════════════════════════════════════════════════

async def setup(bot):
    """
    Charge le cog CommandesInterface dans le bot

    Cette fonction est appelée automatiquement par Discord.py
    lors du chargement de l'extension.
    """
    await bot.add_cog(CommandesInterface(bot))
    bot.logger.info("✅ Cog CommandesInterface chargé")
