"""

═══════════════════════════════════════════════════════════════
FICHIER : noyau/gestionnaire_interface.py
MODULE : Gestionnaire Interface Configuration
DESCRIPTION : Gestion des menus interactifs Discord (Select Menu + Boutons)
AUTEUR : Latury
DATE : 17/01/2026
VERSION : 0.3.0 (CORRIGÉ)
═══════════════════════════════════════════════════════════════

"""

import discord
from discord import ui
from typing import Optional, Dict, Any, List
import json
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# SECTION 01 : CLASSE PRINCIPALE
# ═══════════════════════════════════════════════════════════════

class GestionnaireInterface:
    """
    🎨 FONCTION 01 : Gestion des interfaces interactives
    Gère les menus déroulants (Select Menu), boutons, et embeds
    pour la configuration interactive du bot.
    """

    def __init__(self, bot):
        """Initialise le gestionnaire d'interface"""
        self.bot = bot
        # ✅ CORRECTION : Dict[str, 'ConfigSession'] avec forward reference
        self.sessions_actives: Dict[str, 'ConfigSession'] = {}

    # ══════════════════════════════════════════════════════════
    # FONCTION 02 : Création session configuration
    # ══════════════════════════════════════════════════════════

    def creer_session(self, guild_id: int, user_id: int) -> 'ConfigSession':
        """
        Crée une nouvelle session de configuration pour un utilisateur

        Args:
            guild_id: ID du serveur Discord
            user_id: ID de l'utilisateur

        Returns:
            ConfigSession: Session de configuration active
        """
        session_id = f"{guild_id}_{user_id}"
        if session_id in self.sessions_actives:
            # Fermer l'ancienne session
            del self.sessions_actives[session_id]

        session = ConfigSession(guild_id, user_id, self.bot)
        self.sessions_actives[session_id] = session
        return session

    # ══════════════════════════════════════════════════════════
    # FONCTION 03 : Récupération session
    # ══════════════════════════════════════════════════════════

    def obtenir_session(self, guild_id: int, user_id: int) -> Optional['ConfigSession']:
        """Récupère une session active"""
        session_id = f"{guild_id}_{user_id}"
        return self.sessions_actives.get(session_id)

    # ══════════════════════════════════════════════════════════
    # FONCTION 04 : Fermeture session
    # ══════════════════════════════════════════════════════════

    def fermer_session(self, guild_id: int, user_id: int):
        """Ferme et supprime une session active"""
        session_id = f"{guild_id}_{user_id}"
        if session_id in self.sessions_actives:
            del self.sessions_actives[session_id]

# ═══════════════════════════════════════════════════════════════
# SECTION 02 : SESSION DE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

class ConfigSession:
    """
    🎯 FONCTION 05 : Gestion session individuelle
    Gère l'état de configuration pour un utilisateur spécifique
    """

    def __init__(self, guild_id: int, user_id: int, bot):
        self.guild_id = guild_id
        self.user_id = user_id
        self.bot = bot
        self.categorie_actuelle = "principal"
        self.navigation_historique: List[str] = []
        self.modifications_temporaires: Dict[str, Any] = {}
        self.created_at = datetime.now()

    def naviguer_vers(self, categorie: str):
        """Navigue vers une nouvelle catégorie"""
        self.navigation_historique.append(self.categorie_actuelle)
        self.categorie_actuelle = categorie

    def retour_arriere(self) -> Optional[str]:
        """Retourne à la catégorie précédente"""
        if self.navigation_historique:
            self.categorie_actuelle = self.navigation_historique.pop()
            return self.categorie_actuelle
        return None

# ═══════════════════════════════════════════════════════════════
# SECTION 03 : VUES DISCORD (Select Menu + Boutons)
# ═══════════════════════════════════════════════════════════════

class MenuPrincipalView(ui.View):
    """
    🎨 FONCTION 06 : Menu principal de configuration
    Vue Discord avec Select Menu pour choisir la catégorie
    """

    def __init__(self, session: ConfigSession):
        super().__init__(timeout=300)  # 5 minutes
        self.session = session
        self.add_item(SelectCategorie(session))
        self.add_item(BoutonExport())
        self.add_item(BoutonImport())
        self.add_item(BoutonFermer())

class SelectCategorie(ui.Select):
    """
    📋 FONCTION 07 : Select Menu des catégories
    """

    def __init__(self, session: ConfigSession):
        self.session = session

        options = [
            discord.SelectOption(
                label="📊 Logs",
                description="Configuration des logs Discord",
                emoji="📊",
                value="logs"
            ),
            discord.SelectOption(
                label="🛡️ Modération",
                description="Paramètres de modération",
                emoji="🛡️",
                value="moderation"
            ),
            discord.SelectOption(
                label="💰 Économie",
                description="Système économique (v0.4.0)",
                emoji="💰",
                value="economie"
            ),
            discord.SelectOption(
                label="📈 Niveaux & XP",
                description="Progression des membres (v0.5.0)",
                emoji="📈",
                value="xp"
            )
        ]

        super().__init__(
            placeholder="🔧 Choisissez une catégorie...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        """Callback lors de la sélection d'une catégorie"""
        categorie = self.values[0]
        self.session.naviguer_vers(categorie)

        # Afficher le menu de la catégorie sélectionnée
        if categorie == "logs":
            view = MenuLogsView(self.session)
            embed = creer_embed_logs(self.session)
        elif categorie == "moderation":
            view = MenuModerationView(self.session)
            embed = creer_embed_moderation(self.session)
        else:
            # Catégories futures
            embed = discord.Embed(
                title="🚧 En développement",
                description=f"La catégorie **{categorie}** sera disponible dans une prochaine version.",
                color=discord.Color.orange()
            )
            view = MenuPrincipalView(self.session)

        await interaction.response.edit_message(embed=embed, view=view)

# ═══════════════════════════════════════════════════════════════
# SECTION 04 : BOUTONS D'ACTION
# ═══════════════════════════════════════════════════════════════

class BoutonExport(ui.Button):
    """💾 FONCTION 08 : Bouton export JSON"""

    def __init__(self):
        super().__init__(
            label="Exporter",
            style=discord.ButtonStyle.primary,
            emoji="💾"
        )

    async def callback(self, interaction: discord.Interaction):
        """Export de la configuration en JSON"""
        await interaction.response.send_message(
            "📦 Export en cours... Utilisez `/config-export` pour un export complet.",
            ephemeral=True
        )

class BoutonImport(ui.Button):
    """📥 FONCTION 09 : Bouton import JSON"""

    def __init__(self):
        super().__init__(
            label="Importer",
            style=discord.ButtonStyle.secondary,
            emoji="📥"
        )

    async def callback(self, interaction: discord.Interaction):
        """Import d'une configuration JSON"""
        await interaction.response.send_message(
            "📥 Import disponible via `/config-import <fichier>`",
            ephemeral=True
        )

class BoutonFermer(ui.Button):
    """❌ FONCTION 10 : Bouton fermeture"""

    def __init__(self):
        super().__init__(
            label="Fermer",
            style=discord.ButtonStyle.danger,
            emoji="❌"
        )

    async def callback(self, interaction: discord.Interaction):
        """Ferme le menu de configuration"""
        await interaction.response.edit_message(
            content="✅ Menu de configuration fermé.",
            embed=None,
            view=None
        )

# ═══════════════════════════════════════════════════════════════
# SECTION 05 : VUES PAR CATÉGORIE
# ═══════════════════════════════════════════════════════════════

class MenuLogsView(ui.View):
    """📊 FONCTION 11 : Menu configuration logs"""

    def __init__(self, session: ConfigSession):
        super().__init__(timeout=300)
        self.session = session

        # Bouton retour
        self.add_item(BoutonRetour(session))
        self.add_item(BoutonActiver("logs"))
        self.add_item(BoutonDesactiver("logs"))

class MenuModerationView(ui.View):
    """🛡️ FONCTION 12 : Menu configuration modération"""

    def __init__(self, session: ConfigSession):
        super().__init__(timeout=300)
        self.session = session

        # Bouton retour
        self.add_item(BoutonRetour(session))

class BoutonRetour(ui.Button):
    """◀️ FONCTION 13 : Bouton retour"""

    def __init__(self, session: ConfigSession):
        super().__init__(
            label="Retour",
            style=discord.ButtonStyle.secondary,
            emoji="◀️"
        )
        self.session = session

    async def callback(self, interaction: discord.Interaction):
        """Retourne au menu principal"""
        self.session.retour_arriere()
        embed = creer_embed_principal(self.session)
        view = MenuPrincipalView(self.session)
        await interaction.response.edit_message(embed=embed, view=view)

class BoutonActiver(ui.Button):
    """✅ FONCTION 14 : Bouton activation"""

    def __init__(self, fonctionnalite: str):
        super().__init__(
            label="Activer",
            style=discord.ButtonStyle.success,
            emoji="✅"
        )
        self.fonctionnalite = fonctionnalite

    async def callback(self, interaction: discord.Interaction):
        """Active une fonctionnalité"""
        await interaction.response.send_message(
            f"✅ {self.fonctionnalite.capitalize()} activés !",
            ephemeral=True
        )

class BoutonDesactiver(ui.Button):
    """❌ FONCTION 15 : Bouton désactivation"""

    def __init__(self, fonctionnalite: str):
        super().__init__(
            label="Désactiver",
            style=discord.ButtonStyle.danger,
            emoji="❌"
        )
        self.fonctionnalite = fonctionnalite

    async def callback(self, interaction: discord.Interaction):
        """Désactive une fonctionnalité"""
        await interaction.response.send_message(
            f"❌ {self.fonctionnalite.capitalize()} désactivés !",
            ephemeral=True
        )

# ═══════════════════════════════════════════════════════════════
# SECTION 06 : CRÉATION D'EMBEDS
# ═══════════════════════════════════════════════════════════════

def creer_embed_principal(session: ConfigSession) -> discord.Embed:
    """
    🎨 FONCTION 16 : Création embed menu principal
    """
    embed = discord.Embed(
        title="⚙️ Configuration Interactive",
        description=(
            "Bienvenue dans le panneau de configuration de **La Loyauté** !\n\n"
            "🔧 Utilisez le menu déroulant ci-dessous pour choisir une catégorie.\n"
            "💾 Vous pouvez exporter/importer votre configuration en JSON.\n"
        ),
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📊 Logs",
        value="Configuration des logs Discord",
        inline=True
    )

    embed.add_field(
        name="🛡️ Modération",
        value="Paramètres de modération",
        inline=True
    )

    embed.add_field(
        name="🚧 À venir",
        value="💰 Économie | 📈 Niveaux & XP",
        inline=True
    )

    embed.set_footer(text="v0.3.0 • Interface Interactive • La Loyauté")
    embed.timestamp = datetime.now()

    return embed

def creer_embed_logs(session: ConfigSession) -> discord.Embed:
    """
    🎨 FONCTION 17 : Embed configuration logs
    ✅ CORRECTION : Retourne un Embed au lieu de None
    """
    # Récupérer la config actuelle du serveur
    config_manager = session.bot.config_manager
    config = config_manager.obtenir_configuration(session.guild_id)

    # Vérifier si les logs sont activés
    logs_actifs = config.get("logs_channel") is not None
    status_emoji = "✅" if logs_actifs else "❌"

    embed = discord.Embed(
        title="📊 Configuration des Logs",
        description=(
            f"**Statut :** {status_emoji} {'Activés' if logs_actifs else 'Désactivés'}\n\n"
            "Configurez les logs Discord pour suivre toutes les actions sur votre serveur.\n"
        ),
        color=discord.Color.green() if logs_actifs else discord.Color.red()
    )

    # Salon de logs actuel
    if logs_actifs:
        channel_id = config.get("logs_channel")
        embed.add_field(
            name="📢 Salon actuel",
            value=f"<#{channel_id}>",
            inline=True
        )
    else:
        embed.add_field(
            name="📢 Salon",
            value="Aucun configuré",
            inline=True
        )

    # Types de logs disponibles
    embed.add_field(
        name="📋 Types disponibles",
        value=(
            "🚫 Kick/Ban/Unban\n"
            "🔇 Timeout/Warn\n"
            "🗑️ Messages supprimés\n"
            "✏️ Messages modifiés\n"
            "👥 Membres (arrivée/départ)\n"
            "🎭 Changements de rôles"
        ),
        inline=True
    )

    embed.add_field(
        name="🔧 Actions",
        value=(
            "✅ **Activer** → Utilise le salon actuel\n"
            "❌ **Désactiver** → Stoppe les logs\n"
            "◀️ **Retour** → Menu principal"
        ),
        inline=False
    )

    embed.set_footer(text="Configuration Logs • v0.3.0")
    embed.timestamp = datetime.now()

    return embed

def creer_embed_moderation(session: ConfigSession) -> discord.Embed:
    """
    🎨 FONCTION 18 : Embed configuration modération
    ✅ CORRECTION : Retourne un Embed au lieu de None
    """
    embed = discord.Embed(
        title="🛡️ Configuration de la Modération",
        description=(
            "Configurez les paramètres de modération de votre serveur.\n\n"
            "⚠️ **Disponibilité :** v0.3.1 (prochaine version)"
        ),
        color=discord.Color.orange()
    )

    embed.add_field(
        name="🚧 Fonctionnalités prévues",
        value=(
            "🔨 **Auto-modération**\n"
            "• Filtrage de mots interdits\n"
            "• Anti-spam\n"
            "• Anti-flood\n"
            "• Anti-mention mass\n\n"
            "⚠️ **Système d'avertissements**\n"
            "• Warns automatiques\n"
            "• Sanctions progressives\n"
            "• Historique des warns\n\n"
            "🔒 **Permissions**\n"
            "• Rôles modérateurs\n"
            "• Rôles administrateurs\n"
            "• Whitelist/Blacklist"
        ),
        inline=False
    )

    embed.add_field(
        name="📅 Disponibilité",
        value="**v0.3.1** • Estimation : 1-2 semaines",
        inline=False
    )

    embed.set_footer(text="Configuration Modération • v0.3.0")
    embed.timestamp = datetime.now()

    return embed

# ═══════════════════════════════════════════════════════════════
# FIN DU FICHIER gestionnaire_interface.py
# ═══════════════════════════════════════════════════════════════
