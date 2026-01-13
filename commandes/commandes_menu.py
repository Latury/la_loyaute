from __future__ import annotations

# ══════════════════════════════════════════════════════════════════════
# ║
# ║  🎨 LA LOYAUTÉ - SYSTÈME DE MENU INTERACTIF
# ║
# ║  Gestion du menu de configuration avec embeds et boutons
# ║
# ║  📄 Fichier : commandes/commandes_menu.py
# ║  👤 Auteur : Latury
# ║  📅 Date : 07/01/2026
# ║  🔖 Version : 0.3.0
# ║
# ══════════════════════════════════════════════════════════════════════

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import configuration as config
from utilitaires.helpers import creer_embed

# ══════════════════════════════════════════════════════════════════════
# ║ 🎨 CLASSE : VUE DU MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════════════

class MenuPrincipalView(discord.ui.View):
    """Vue du menu principal avec boutons de navigation"""

    def __init__(self, bot):
        super().__init__(timeout=300)  # 5 minutes de timeout
        self.bot = bot
        self.message: Optional[discord.Message] = None

    # ─────────────────────────────────────────────────────────────────
    # 📊 Bouton : Section Logs
    # ─────────────────────────────────────────────────────────────────

    @discord.ui.button(
        label="Logs",
        emoji="📊",
        style=discord.ButtonStyle.primary,
        custom_id="menu_logs"
    )
    async def bouton_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Affiche le menu de configuration des logs"""
        if not interaction.guild:
            await interaction.response.send_message("❌ Cette commande ne fonctionne que dans un serveur.", ephemeral=True)
            return

        await interaction.response.defer()

        embed = creer_embed(
            titre="📊 Configuration des Logs",
            description="Configurez les logs de votre serveur",
            couleur=config.COULEUR_INFO
        )

        embed.add_field(
            name="📝 Logs actuels",
            value="• Arrivées/Départs de membres\n• Modifications de messages\n• Suppressions de messages\n• Changements de rôles\n• Actions de modération",
            inline=False
        )

        # Récupérer le salon de logs configuré
        gestionnaire_config = self.bot.gestionnaire_config
        salon_logs_id = gestionnaire_config.obtenir_salon_logs(interaction.guild.id)

        if salon_logs_id:
            salon_logs = interaction.guild.get_channel(salon_logs_id)
            if salon_logs:
                embed.add_field(
                    name="🎯 Salon configuré",
                    value=f"{salon_logs.mention}",
                    inline=False
                )
            else:
                embed.add_field(
                    name="⚠️ Salon configuré",
                    value=f"ID: {salon_logs_id} (salon introuvable)",
                    inline=False
                )
        else:
            embed.add_field(
                name="❌ Aucun salon configuré",
                value="Utilisez `/config logs #salon` pour configurer",
                inline=False
            )

        embed.set_footer(text="💡 Utilisez les commandes /config pour modifier la configuration")

        # Créer une vue avec bouton retour
        view = MenuRetourView(self.bot)

        await interaction.edit_original_response(embed=embed, view=view)

    # ─────────────────────────────────────────────────────────────────
    # 👋 Bouton : Section Bienvenue
    # ─────────────────────────────────────────────────────────────────

    @discord.ui.button(
        label="Bienvenue",
        emoji="👋",
        style=discord.ButtonStyle.success,
        custom_id="menu_bienvenue"
    )
    async def bouton_bienvenue(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Affiche le menu de configuration des messages de bienvenue"""
        await interaction.response.defer()

        embed = creer_embed(
            titre="👋 Configuration Bienvenue/Départ",
            description="Configurez les messages d'arrivée et de départ",
            couleur=config.COULEUR_SUCCES
        )

        embed.add_field(
            name="📥 Messages de bienvenue",
            value="Configurez un message personnalisé pour accueillir les nouveaux membres",
            inline=False
        )

        embed.add_field(
            name="📤 Messages de départ",
            value="Configurez un message pour dire au revoir aux membres qui partent",
            inline=False
        )

        embed.add_field(
            name="🎨 Variables disponibles",
            value="• `{membre}` - Mention du membre\n• `{nom}` - Nom du membre\n• `{serveur}` - Nom du serveur\n• `{nombre}` - Nombre de membres",
            inline=False
        )

        embed.add_field(
            name="⚙️ Configuration actuelle",
            value="*Fonctionnalité à venir dans v0.3.1*",
            inline=False
        )

        embed.set_footer(text="💡 Cette section sera complétée prochainement")

        # Créer une vue avec bouton retour
        view = MenuRetourView(self.bot)

        await interaction.edit_original_response(embed=embed, view=view)

    # ─────────────────────────────────────────────────────────────────
    # 🛡️ Bouton : Section Modération
    # ─────────────────────────────────────────────────────────────────

    @discord.ui.button(
        label="Modération",
        emoji="🛡️",
        style=discord.ButtonStyle.danger,
        custom_id="menu_moderation"
    )
    async def bouton_moderation(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Affiche le menu de configuration de la modération"""
        await interaction.response.defer()

        embed = creer_embed(
            titre="🛡️ Configuration Modération",
            description="Gérez les paramètres de modération du serveur",
            couleur=config.COULEUR_ERREUR
        )

        embed.add_field(
            name="⚔️ Commandes disponibles",
            value="• `/kick` - Expulser un membre\n• `/ban` - Bannir un membre\n• `/unban` - Débannir un membre\n• `/timeout` - Mettre en timeout\n• `/warn` - Avertir un membre\n• `/clear` - Supprimer des messages",
            inline=False
        )

        embed.add_field(
            name="📋 Système de warns",
            value="• `/warns` - Voir les warns d'un membre\n• `/clearwarns` - Effacer les warns",
            inline=False
        )

        embed.add_field(
            name="🔒 Permissions requises",
            value="Les modérateurs doivent avoir les permissions appropriées pour utiliser ces commandes",
            inline=False
        )

        embed.set_footer(text="💡 Toutes les actions de modération sont enregistrées dans les logs")

        # Créer une vue avec bouton retour
        view = MenuRetourView(self.bot)

        await interaction.edit_original_response(embed=embed, view=view)

    # ─────────────────────────────────────────────────────────────────
    # 🎭 Bouton : Section Auto-rôles
    # ─────────────────────────────────────────────────────────────────

    @discord.ui.button(
        label="Auto-rôles",
        emoji="🎭",
        style=discord.ButtonStyle.secondary,
        custom_id="menu_autoroles"
    )
    async def bouton_autoroles(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Affiche le menu de configuration des auto-rôles"""
        await interaction.response.defer()

        embed = creer_embed(
            titre="🎭 Configuration Auto-rôles",
            description="Gérez l'attribution automatique de rôles",
            couleur=config.COULEUR_AVERTISSEMENT
        )

        embed.add_field(
            name="🤖 Auto-rôles à l'arrivée",
            value="Attribuez automatiquement des rôles aux nouveaux membres",
            inline=False
        )

        embed.add_field(
            name="🎨 Rôles par réaction",
            value="Permettez aux membres de choisir leurs rôles en réagissant à un message",
            inline=False
        )

        embed.add_field(
            name="⚙️ Configuration actuelle",
            value="*Fonctionnalité à venir dans v0.3.2*",
            inline=False
        )

        embed.set_footer(text="💡 Cette section sera complétée prochainement")

        # Créer une vue avec bouton retour
        view = MenuRetourView(self.bot)

        await interaction.edit_original_response(embed=embed, view=view)

    # ─────────────────────────────────────────────────────────────────
    # ℹ️ Bouton : Informations
    # ─────────────────────────────────────────────────────────────────

    @discord.ui.button(
        label="Informations",
        emoji="ℹ️",
        style=discord.ButtonStyle.secondary,
        custom_id="menu_infos",
        row=1
    )
    async def bouton_infos(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Affiche les informations du bot"""
        await interaction.response.defer()

        # Calculer les statistiques
        total_membres = sum(guild.member_count or 0 for guild in self.bot.guilds)
        bot_name = self.bot.user.name if self.bot.user else "Bot"

        embed = creer_embed(
            titre="ℹ️ Informations du Bot",
            description=f"**{bot_name}** - Bot de gestion Discord",
            couleur=config.COULEUR_PRINCIPALE
        )

        embed.add_field(
            name="📊 Statistiques",
            value=f"• Serveurs : {len(self.bot.guilds)}\n• Membres : {total_membres}\n• Latence : {round(self.bot.latency * 1000)}ms",
            inline=False
        )

        embed.add_field(
            name="🔖 Version",
            value="`v0.3.0`",
            inline=True
        )

        embed.add_field(
            name="👤 Développeur",
            value="Latury",
            inline=True
        )

        embed.add_field(
            name="🔗 Liens utiles",
            value="• [GitHub](https://github.com/Latury/la_loyaute)\n• [Support](https://discord.gg/votre-serveur)",
            inline=False
        )

        embed.set_footer(text="Bot développé avec discord.py • v0.3.0")

        # Créer une vue avec bouton retour
        view = MenuRetourView(self.bot)

        await interaction.edit_original_response(embed=embed, view=view)

# ══════════════════════════════════════════════════════════════════════
# ║ 🔙 CLASSE : VUE RETOUR AU MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════════════

class MenuRetourView(discord.ui.View):
    """Vue avec bouton de retour au menu principal"""

    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

    @discord.ui.button(
        label="Retour au menu",
        emoji="🔙",
        style=discord.ButtonStyle.secondary,
        custom_id="retour_menu"
    )
    async def bouton_retour(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Retourne au menu principal"""
        if not interaction.guild:
            await interaction.response.send_message("❌ Cette commande ne fonctionne que dans un serveur.", ephemeral=True)
            return

        await interaction.response.defer()

        # Créer l'embed du menu principal
        embed = creer_embed(
            titre="🎨 Menu de Configuration",
            description=f"Bienvenue dans le panneau de configuration de **{interaction.guild.name}**",
            couleur=config.COULEUR_PRINCIPALE
        )

        embed.add_field(
            name="📊 Logs",
            value="Configurez les logs du serveur",
            inline=True
        )

        embed.add_field(
            name="👋 Bienvenue",
            value="Messages d'arrivée/départ",
            inline=True
        )

        embed.add_field(
            name="🛡️ Modération",
            value="Paramètres de modération",
            inline=True
        )

        embed.add_field(
            name="🎭 Auto-rôles",
            value="Attribution automatique de rôles",
            inline=True
        )

        embed.add_field(
            name="ℹ️ Informations",
            value="Informations sur le bot",
            inline=True
        )

        embed.set_footer(text="💡 Cliquez sur un bouton pour accéder à une section")

        # Créer la vue du menu principal
        view = MenuPrincipalView(self.bot)

        await interaction.edit_original_response(embed=embed, view=view)

# ══════════════════════════════════════════════════════════════════════
# ║ 📋 CLASSE : COMMANDES DE MENU
# ══════════════════════════════════════════════════════════════════════

class CommandesMenu(commands.Cog):
    """Gestion du menu de configuration interactif"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

    # ═══════════════════════════════════════════════════════════════════
    # ║ 🎨 Commande /menu
    # ║ Description : Affiche le menu de configuration interactif
    # ═══════════════════════════════════════════════════════════════════

    @app_commands.command(
        name="menu",
        description="🎨 Affiche le menu de configuration du serveur"
    )
    @app_commands.default_permissions(administrator=True)
    async def menu(self, interaction: discord.Interaction):
        """Affiche le menu principal de configuration"""

        if not interaction.guild:
            await interaction.response.send_message("❌ Cette commande ne fonctionne que dans un serveur.", ephemeral=True)
            return

        try:
            # Créer l'embed du menu principal
            bot_name = self.bot.user.name if self.bot.user else "Bot"

            embed = creer_embed(
                titre="🎨 Menu de Configuration",
                description=f"Bienvenue dans le panneau de configuration de **{interaction.guild.name}**",
                couleur=config.COULEUR_PRINCIPALE
            )

            embed.add_field(
                name="📊 Logs",
                value="Configurez les logs du serveur",
                inline=True
            )

            embed.add_field(
                name="👋 Bienvenue",
                value="Messages d'arrivée/départ",
                inline=True
            )

            embed.add_field(
                name="🛡️ Modération",
                value="Paramètres de modération",
                inline=True
            )

            embed.add_field(
                name="🎭 Auto-rôles",
                value="Attribution automatique de rôles",
                inline=True
            )

            embed.add_field(
                name="ℹ️ Informations",
                value="Informations sur le bot",
                inline=True
            )

            embed.set_footer(text="💡 Cliquez sur un bouton pour accéder à une section")

            # Créer la vue avec les boutons
            view = MenuPrincipalView(self.bot)

            # Envoyer le message
            await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

            # Logger l'action
            self.logger.info(f"📋 Menu affiché par {interaction.user} dans {interaction.guild.name}")

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'affichage du menu : {e}")
            await interaction.response.send_message(
                "❌ Une erreur est survenue lors de l'affichage du menu.",
                ephemeral=True
            )

# ══════════════════════════════════════════════════════════════════════
# ║ 🔌 FONCTION DE CHARGEMENT
# ══════════════════════════════════════════════════════════════════════

async def setup(bot):
    """Charge le cog des commandes de menu"""
    await bot.add_cog(CommandesMenu(bot))


