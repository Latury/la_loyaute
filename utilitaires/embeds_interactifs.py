# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🦁 LA LOYAUTÉ - embeds_interactifs.py
# ║
# ║ 🎨 Bot Discord privé développé en Python
# ║ 👨‍💻 Développé par Latury
# ║ 📦 Version : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 📄 FICHIER : embeds_interactifs.py
# ║ ⚙️ MODULE : Système d'embeds interactifs
# ║ 📝 DESCRIPTION : Système complet d'embeds Discord avec menus déroulants, boutons et modals pour interface de configuration
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15/01/2026
# ║ 🔢 VERSION : 0.2.2
# ║
# ═══════════════════════════════════════════════════════════════════════════════

"""
🦁 LA LOYAUTÉ - Système d'embeds interactifs
══════════════════════════════════════════════════════════════════════════════
Menus déroulants, boutons et modals pour configuration visuelle
"""

import discord
from discord.ui import Select, View, Button, Modal, TextInput
from typing import Optional
from datetime import datetime

from configuration import COULEUR_PRINCIPALE, COULEUR_SUCCES, COULEUR_ERREUR, COULEUR_AVERTISSEMENT

# ══════════════════════════════════════════════════════════════════════
# ║ 📋 FONCTIONS DE CRÉATION D'EMBEDS
# ══════════════════════════════════════════════════════════════════════

def creer_embed_menu_principal(guild_id: int) -> discord.Embed:
    """
    🎨 Crée l'embed du menu principal de configuration

    Args:
        guild_id: ID du serveur Discord

    Returns:
        discord.Embed: Embed du menu principal
    """
    embed = discord.Embed(
        title="⚙️ Configuration du Bot",
        description=(
            "Bienvenue dans le panneau de configuration de **La Loyauté** !\n\n"
            "Utilisez le menu déroulant ci-dessous pour configurer les différents modules du bot.\n\n"
            "**Modules disponibles :**\n"
            "📊 **Logs** - Configuration des logs Discord\n"
            "🎭 **Rôles** - Gestion des rôles automatiques\n"
            "💬 **Messages** - Messages de bienvenue et départ\n"
            "🛡️ **Modération** - Outils de modération\n"
            "📢 **Annonces** - Configuration des annonces"
        ),
        color=COULEUR_PRINCIPALE,
        timestamp=datetime.now()
    )

    embed.set_footer(text="La Loyauté • Configuration Interactive")
    return embed


def creer_embed_logs(config: dict) -> discord.Embed:
    """
    📊 Crée l'embed de configuration des logs

    Args:
        config: Configuration actuelle du serveur

    Returns:
        discord.Embed: Embed de configuration des logs
    """
    salon_logs_id = config.get('salon_logs')
    statut = "✅ Activé" if salon_logs_id else "❌ Désactivé"
    salon_mention = f"<#{salon_logs_id}>" if salon_logs_id else "Aucun"

    embed = discord.Embed(
        title="📊 Configuration des Logs",
        description=(
            "Les logs permettent d'enregistrer tous les événements importants du serveur.\n\n"
            f"**Statut actuel :** {statut}\n"
            f"**Salon de logs :** {salon_mention}\n\n"
            "**Actions disponibles :**\n"
            "• Définir un salon de logs existant\n"
            "• Créer automatiquement un salon de logs\n"
            "• Désactiver les logs"
        ),
        color=COULEUR_PRINCIPALE,
        timestamp=datetime.now()
    )

    embed.set_footer(text="📊 Module Logs")
    return embed

# ══════════════════════════════════════════════════════════════════════
# ║ 🎯 CLASSE : VUE MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════════════

class VueMenuPrincipal(View):
    """🎯 Vue principale avec menu déroulant de sélection"""

    def __init__(self, config_manager, guild_id: int):
        super().__init__(timeout=180)
        self.config_manager = config_manager
        self.guild_id = guild_id
        self.add_item(SelectMenuConfiguration(config_manager, guild_id))


class SelectMenuConfiguration(Select):
    """📋 Menu déroulant de sélection des modules"""

    def __init__(self, config_manager, guild_id: int):
        self.config_manager = config_manager
        self.guild_id = guild_id

        options = [
            discord.SelectOption(
                label="📊 Logs Discord",
                description="Configurer l'enregistrement des événements",
                emoji="📊",
                value="logs"
            ),
            discord.SelectOption(
                label="🎭 Rôles Automatiques",
                description="Gérer l'attribution automatique des rôles",
                emoji="🎭",
                value="roles"
            ),
            discord.SelectOption(
                label="💬 Messages de Bienvenue",
                description="Personnaliser les messages d'accueil",
                emoji="💬",
                value="messages"
            ),
            discord.SelectOption(
                label="🛡️ Modération",
                description="Configurer les outils de modération",
                emoji="🛡️",
                value="moderation"
            ),
            discord.SelectOption(
                label="📢 Annonces",
                description="Paramétrer le système d'annonces",
                emoji="📢",
                value="annonces"
            ),
            discord.SelectOption(
                label="🔙 Retour au menu",
                description="Revenir au menu principal",
                emoji="🔙",
                value="menu"
            )
        ]

        super().__init__(
            placeholder="📋 Choisissez un module à configurer...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        """📞 Gère la sélection d'un module"""
        choix = self.values[0]

        if choix == "menu":
            embed = creer_embed_menu_principal(self.guild_id)
            view = VueMenuPrincipal(self.config_manager, self.guild_id)
            await interaction.response.edit_message(embed=embed, view=view)

        elif choix == "logs":
            config = self.config_manager.obtenir_configuration(self.guild_id)
            embed = creer_embed_logs(config)
            view = VueConfigurationLogs(self.config_manager, self.guild_id)
            await interaction.response.edit_message(embed=embed, view=view)

        else:
            embed = discord.Embed(
                title=f"🚧 Module {choix.upper()} en développement",
                description="Ce module sera disponible prochainement !",
                color=COULEUR_AVERTISSEMENT,
                timestamp=datetime.now()
            )
            await interaction.response.edit_message(embed=embed, view=self.view)

# ══════════════════════════════════════════════════════════════════════
# ║ 📊 CLASSE : VUE CONFIGURATION LOGS
# ══════════════════════════════════════════════════════════════════════

class VueConfigurationLogs(View):
    """📊 Vue de configuration des logs avec boutons d'action"""

    def __init__(self, config_manager, guild_id: int):
        super().__init__(timeout=180)
        self.config_manager = config_manager
        self.guild_id = guild_id
        self.add_item(SelectMenuConfiguration(config_manager, guild_id))

    @discord.ui.button(label="✅ Créer un salon de logs", style=discord.ButtonStyle.success, emoji="➕")
    async def creer_salon_logs(self, interaction: discord.Interaction, button: Button):
        """➕ Crée automatiquement un salon de logs"""
        try:
            await interaction.response.defer(ephemeral=True)

            guild = interaction.guild
            guild_id = interaction.guild_id

            # Vérifier que guild et guild_id existent
            if not guild or not guild_id:
                await interaction.followup.send(
                    "❌ Cette commande ne peut être utilisée qu'en serveur.",
                    ephemeral=True
                )
                return

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

            # Mettre à jour l'embed
            config = self.config_manager.obtenir_configuration(guild_id)
            embed = creer_embed_logs(config)

            if interaction.message:
                await interaction.message.edit(embed=embed)

            await interaction.followup.send(
                f"✅ Le salon {salon.mention} a été créé avec succès !",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions pour créer un salon.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Une erreur est survenue : {e}",
                ephemeral=True
            )

    @discord.ui.button(label="🔴 Désactiver les logs", style=discord.ButtonStyle.danger, emoji="❌")
    async def desactiver_logs(self, interaction: discord.Interaction, button: Button):
        """🔴 Désactive les logs"""
        try:
            # Récupérer guild_id
            guild_id = interaction.guild_id

            if not guild_id:
                await interaction.response.send_message(
                    "❌ Cette commande ne peut être utilisée qu'en serveur.",
                    ephemeral=True
                )
                return

            # Désactiver les logs
            self.config_manager.definir_salon_logs(guild_id, None)

            # Mettre à jour l'embed
            config = self.config_manager.obtenir_configuration(guild_id)
            embed = creer_embed_logs(config)

            await interaction.response.edit_message(embed=embed)
            await interaction.followup.send(
                "✅ Les logs ont été désactivés avec succès !",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Une erreur est survenue : {e}",
                ephemeral=True
            )

# ══════════════════════════════════════════════════════════════════════
# ║ 📝 CLASSE : MODAL DE CONFIGURATION
# ══════════════════════════════════════════════════════════════════════

class ModalConfigurationTexte(Modal):
    """📝 Modal pour saisir du texte de configuration"""

    def __init__(self, config_manager, guild_id: int, cle_config: str, titre: str, placeholder: str):
        super().__init__(title=titre, timeout=300)
        self.config_manager = config_manager
        self.guild_id = guild_id
        self.cle_config = cle_config

        self.champ_texte = TextInput(
            label="Valeur",
            placeholder=placeholder,
            required=True,
            max_length=2000,
            style=discord.TextStyle.paragraph
        )

        self.add_item(self.champ_texte)

    async def on_submit(self, interaction: discord.Interaction):
        """💾 Enregistre la valeur saisie"""
        try:
            valeur = self.champ_texte.value
            self.config_manager.definir(self.guild_id, self.cle_config, valeur)

            embed = discord.Embed(
                title="✅ Configuration enregistrée",
                description=f"La valeur a été enregistrée avec succès !\n\n**Clé :** `{self.cle_config}`",
                color=COULEUR_SUCCES,
                timestamp=datetime.now()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Une erreur est survenue : {e}",
                ephemeral=True
            )

# ══════════════════════════════════════════════════════════════════════
# ║ 🎨 CLASSE : VUE AVEC PAGINATION
# ══════════════════════════════════════════════════════════════════════

class VuePagination(View):
    """🎨 Vue avec système de pagination"""

    def __init__(self, embeds: list, timeout: int = 180):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.page_actuelle = 0
        self.max_pages = len(embeds)
        self.update_buttons()

    def update_buttons(self):
        """🔄 Met à jour l'état des boutons"""
        self.bouton_precedent.disabled = (self.page_actuelle == 0)
        self.bouton_suivant.disabled = (self.page_actuelle == self.max_pages - 1)

    @discord.ui.button(label="◀️ Précédent", style=discord.ButtonStyle.secondary)
    async def bouton_precedent(self, interaction: discord.Interaction, button: Button):
        """◀️ Page précédente"""
        self.page_actuelle = max(0, self.page_actuelle - 1)
        self.update_buttons()

        embed = self.embeds[self.page_actuelle]
        embed.set_footer(text=f"Page {self.page_actuelle + 1}/{self.max_pages}")

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="▶️ Suivant", style=discord.ButtonStyle.secondary)
    async def bouton_suivant(self, interaction: discord.Interaction, button: Button):
        """▶️ Page suivante"""
        self.page_actuelle = min(self.max_pages - 1, self.page_actuelle + 1)
        self.update_buttons()

        embed = self.embeds[self.page_actuelle]
        embed.set_footer(text=f"Page {self.page_actuelle + 1}/{self.max_pages}")

        await interaction.response.edit_message(embed=embed, view=self)
# ═══════════════════════════════════════════════════════════════════════════════
# ║ ✅ FIN DU FICHIER – Système d'embeds interactifs complet
# ║ 📦 Menus déroulants, boutons, modals et pagination disponibles
# ╚═══════════════════════════════════════════════════════════════════════════════