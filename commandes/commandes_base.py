from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║  💬 LA LOYAUTÉ - COMMANDES DE BASE
# ║
# ║  Commandes publiques accessibles à tous (prefix !)
# ║  Développé par Latury
# ║  Version : 0.1.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from datetime import datetime
import platform
import psutil
from typing import Optional  # ← AJOUTE CETTE LIGNE

# Importation de la configuration
import configuration as config
from utilitaires.helpers import (
    creer_embed,
    creer_embed_info,
    creer_embed_succes,
    formater_date,
    formater_duree,
    formater_nombre
)
from noyau.gestionnaire_permissions import obtenir_niveau_permission

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📦 Classe 01 – Cog des commandes de base
# ║ Description : Contient toutes les commandes publiques du bot
# ╚══════════════════════════════════════════════════════════════════════════════
class CommandesBase(commands.Cog):
    """Cog contenant les commandes de base accessibles à tous"""

    def __init__(self, bot):
        """Initialise le cog des commandes de base"""

        self.bot = bot

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📖 Fonction 01 – Commande !aide
    # ║ Description : Affiche la liste des commandes disponibles
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.command(
        name='aide',
        aliases=['help', 'h'],
        help='Affiche la liste des commandes disponibles'
    )
    async def aide(self, ctx):
        """Affiche l'aide du bot"""

        # ── 🔹 Création de l'embed principal
        embed = creer_embed(
            titre=f"📖 Aide - {config.NOM_BOT}",
            description=f"Voici la liste des commandes disponibles pour **{config.NOM_BOT}**.",
            couleur=config.COULEUR_PRINCIPALE
        )

        # ── 🔹 Commandes de base
        commandes_base = (
            f"`{config.PREFIX_BASE}aide` - Affiche cette aide\n"
            f"`{config.PREFIX_BASE}info` - Informations sur le bot\n"
            f"`{config.PREFIX_BASE}ping` - Teste la latence du bot\n"
            f"`{config.PREFIX_BASE}stats` - Statistiques du bot\n"
            f"`{config.PREFIX_BASE}serveur` - Informations sur le serveur\n"
            f"`{config.PREFIX_BASE}utilisateur [@mention]` - Informations sur un utilisateur"
        )

        embed.add_field(
            name="💬 Commandes de base",
            value=commandes_base,
            inline=False
        )

        # ── 🔹 Commandes admin (si autorisé)
        if ctx.author.guild_permissions.administrator:
            commandes_admin = (
                f"`/clear [nombre]` - Supprime des messages\n"
                f"`/config` - Configure le bot\n"
                f"`/logs` - Consulte les logs"
            )

            embed.add_field(
                name="👑 Commandes administratives",
                value=commandes_admin,
                inline=False
            )

        # ── 🔹 Informations supplémentaires
        embed.add_field(
            name="ℹ️ Informations",
            value=f"Prefix : `{config.PREFIX_BASE}` (commandes publiques) | `/` (commandes admin)",
            inline=False
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)

        await ctx.send(embed=embed)

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🤖 Fonction 02 – Commande !info
    # ║ Description : Affiche les informations sur le bot
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.command(
        name='info',
        aliases=['information', 'about'],
        help='Affiche les informations sur le bot'
    )
    async def info(self, ctx):
        """Affiche les informations du bot"""

        # ── 🔹 Récupération des statistiques
        stats = self.bot.obtenir_statistiques()

        # ── 🔹 Création de l'embed
        embed = creer_embed(
            titre=f"🤖 Informations - {config.NOM_BOT}",
            description=f"Bot Discord privé développé en Python avec discord.py",
            couleur=config.COULEUR_PRINCIPALE
        )

        # ── 🔹 Informations générales
        embed.add_field(
            name="📋 Général",
            value=(
                f"**Nom :** {stats['nom']}\n"
                f"**Version :** {stats['version']}\n"
                f"**Développeur :** {stats['developpeur']}\n"
                f"**ID :** {stats['id']}"
            ),
            inline=True
        )

        # ── 🔹 Statistiques
        embed.add_field(
            name="📊 Statistiques",
            value=(
                f"**Serveurs :** {formater_nombre(stats['serveurs'])}\n"
                f"**Utilisateurs :** {formater_nombre(stats['utilisateurs'])}\n"
                f"**Commandes :** {stats['commandes']}\n"
                f"**Latence :** {stats['latence']} ms"
            ),
            inline=True
        )

        # ── 🔹 Uptime
        if stats['uptime']:
            embed.add_field(
                name="⏱️ Temps de fonctionnement",
                value=f"**Uptime :** {stats['uptime']}",
                inline=False
            )

        # ── 🔹 Technologies
        embed.add_field(
            name="🛠️ Technologies",
            value=(
                f"**Python :** {platform.python_version()}\n"
                f"**Discord.py :** {discord.__version__}\n"
                f"**Système :** {platform.system()} {platform.release()}"
            ),
            inline=False
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)

        await ctx.send(embed=embed)

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🏓 Fonction 03 – Commande !ping
    # ║ Description : Teste la latence du bot
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.command(
        name='ping',
        help='Teste la latence du bot'
    )
    async def ping(self, ctx):
        """Teste la latence du bot"""

        # ── 🔹 Calcul de la latence
        latence_ws = round(self.bot.latency * 1000, 2)

        # ── 🔹 Détermination de la qualité
        if latence_ws < 100:
            emoji = "🟢"
            qualite = "Excellente"
            couleur = config.COULEUR_SUCCES
        elif latence_ws < 200:
            emoji = "🟡"
            qualite = "Bonne"
            couleur = config.COULEUR_AVERTISSEMENT
        else:
            emoji = "🔴"
            qualite = "Mauvaise"
            couleur = config.COULEUR_ERREUR

        # ── 🔹 Création de l'embed
        embed = creer_embed(
            titre=f"{emoji} Pong !",
            description=f"Latence : **{latence_ws} ms**\nQualité : **{qualite}**",
            couleur=couleur
        )

        await ctx.send(embed=embed)

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 📊 Fonction 04 – Commande !stats
    # ║ Description : Affiche les statistiques détaillées du bot
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.command(
        name='stats',
        aliases=['statistiques', 'statistics'],
        help='Affiche les statistiques du bot'
    )
    async def stats(self, ctx):
        """Affiche les statistiques du bot"""

        # ── 🔹 Récupération des statistiques
        stats = self.bot.obtenir_statistiques()

        # ── 🔹 Statistiques des messages (si disponible)
        messages_stats = {'messages_traites': 0, 'messages_supprimes': 0, 'messages_modifies': 0}
        messages_cog = self.bot.get_cog('Messages')
        if messages_cog:
            messages_stats = messages_cog.obtenir_statistiques()

        # ── 🔹 Utilisation de la RAM
        process = psutil.Process()
        ram_usage = round(process.memory_info().rss / 1024 / 1024, 2)

        # ── 🔹 Création de l'embed
        embed = creer_embed(
            titre="📊 Statistiques du bot",
            description=f"Statistiques détaillées de **{config.NOM_BOT}**",
            couleur=config.COULEUR_PRINCIPALE
        )

        # ── 🔹 Statistiques générales
        embed.add_field(
            name="🤖 Bot",
            value=(
                f"**Serveurs :** {formater_nombre(stats['serveurs'])}\n"
                f"**Utilisateurs :** {formater_nombre(stats['utilisateurs'])}\n"
                f"**Commandes :** {stats['commandes']}\n"
                f"**Latence :** {stats['latence']} ms"
            ),
            inline=True
        )

        # ── 🔹 Statistiques de commandes
        embed.add_field(
            name="⚡ Commandes",
            value=(
                f"**Exécutées :** {formater_nombre(stats['commandes_executees'])}\n"
                f"**Erreurs :** {formater_nombre(stats['erreurs'])}\n"
                f"**Taux de succès :** {self._calculer_taux_succes(stats)}%"
            ),
            inline=True
        )

        # ── 🔹 Statistiques de messages
        embed.add_field(
            name="📨 Messages",
            value=(
                f"**Traités :** {formater_nombre(messages_stats['messages_traites'])}\n"
                f"**Supprimés :** {formater_nombre(messages_stats['messages_supprimes'])}\n"
                f"**Modifiés :** {formater_nombre(messages_stats['messages_modifies'])}"
            ),
            inline=True
        )

        # ── 🔹 Ressources système
        embed.add_field(
            name="💻 Système",
            value=(
                f"**RAM utilisée :** {ram_usage} MB\n"
                f"**Python :** {platform.python_version()}\n"
                f"**Uptime :** {stats['uptime'] if stats['uptime'] else 'Indisponible'}"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🏠 Fonction 05 – Commande !serveur
    # ║ Description : Affiche les informations sur le serveur
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.command(
        name='serveur',
        aliases=['server', 'guild'],
        help='Affiche les informations sur le serveur'
    )
    @commands.guild_only()
    async def serveur(self, ctx):
        """Affiche les informations du serveur"""

        guild = ctx.guild

        # ── 🔹 Création de l'embed
        embed = creer_embed(
            titre=f"🏠 Informations - {guild.name}",
            description=f"Serveur créé le {formater_date(guild.created_at, inclure_heure=False)}",
            couleur=config.COULEUR_PRINCIPALE
        )

        # ── 🔹 Informations générales
        embed.add_field(
            name="📋 Général",
            value=(
                f"**Propriétaire :** {guild.owner.mention}\n"
                f"**ID :** {guild.id}\n"
                f"**Région :** {guild.preferred_locale}\n"
                f"**Niveau de vérification :** {guild.verification_level}"
            ),
            inline=True
        )

        # ── 🔹 Statistiques
        embed.add_field(
            name="📊 Statistiques",
            value=(
                f"**Membres :** {formater_nombre(guild.member_count)}\n"
                f"**Rôles :** {len(guild.roles)}\n"
                f"**Salons :** {len(guild.channels)}\n"
                f"**Emojis :** {len(guild.emojis)}"
            ),
            inline=True
        )

        # ── 🔹 Boosts
        if guild.premium_tier > 0:
            embed.add_field(
                name="💎 Boosts",
                value=(
                    f"**Niveau :** {guild.premium_tier}\n"
                    f"**Boosts :** {guild.premium_subscription_count}"
                ),
                inline=False
            )

        # ── 🔹 Icône du serveur
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await ctx.send(embed=embed)

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 👤 Fonction 06 – Commande !utilisateur
    # ║ Description : Affiche les informations sur un utilisateur
    # ╚═════════════════════════════════════════════════════════════════════════
    @commands.command(
        name='utilisateur',
        aliases=['user', 'userinfo', 'whois'],
        help='Affiche les informations sur un utilisateur'
    )
    @commands.guild_only()
    async def utilisateur(self, ctx, membre: Optional[discord.Member] = None):
        """Affiche les informations d'un utilisateur"""

        # ── 🔹 Par défaut, affiche l'auteur
        membre = membre if membre is not None else ctx.author

        # ── 🔹 Création de l'embed
        embed = creer_embed(
            titre=f"👤 Profil - {membre.name}",
            description=membre.mention,
            couleur=membre.color.value if membre.color != discord.Color.default() else config.COULEUR_PRINCIPALE
        )

        # ── 🔹 Informations générales
        embed.add_field(
            name="📋 Général",
            value=(
                f"**Nom complet :** {membre}\n"
                f"**ID :** {membre.id}\n"
                f"**Surnom :** {membre.nick or 'Aucun'}\n"
                f"**Bot :** {'Oui' if membre.bot else 'Non'}"
            ),
            inline=True
        )

        # ── 🔹 Dates
        embed.add_field(
            name="📅 Dates",
            value=(
                f"**Compte créé :** {formater_date(membre.created_at, inclure_heure=False)}\n"
                f"**Rejoint le serveur :** {formater_date(membre.joined_at, inclure_heure=False) if membre.joined_at else 'Inconnue'}"
            ),
            inline=True
        )

        # ── 🔹 Rôles
        roles = [role.mention for role in membre.roles[1:]]  # Exclut @everyone
        roles_texte = ", ".join(roles[:10]) if roles else "Aucun rôle"
        if len(roles) > 10:
            roles_texte += f" et {len(roles) - 10} autre(s)"

        embed.add_field(
            name=f"🎭 Rôles ({len(roles)})",
            value=roles_texte,
            inline=False
        )

        # ── 🔹 Permissions
        niveau = obtenir_niveau_permission(membre)
        embed.add_field(
            name="🔐 Niveau de permission",
            value=niveau,
            inline=False
        )

        # ── 🔹 Avatar
        if membre.avatar:
            embed.set_thumbnail(url=membre.avatar.url)

        await ctx.send(embed=embed)

    # ╔═════════════════════════════════════════════════════════════════════════
    # ║ 🔧 Fonction utilitaire – Calcul du taux de succès
    # ║ Description : Calcule le pourcentage de commandes réussies
    # ╚═════════════════════════════════════════════════════════════════════════
    def _calculer_taux_succes(self, stats: dict) -> float:
        """Calcule le taux de succès des commandes"""

        total = stats['commandes_executees']
        if total == 0:
            return 100.0

        succes = total - stats['erreurs']
        return round((succes / total) * 100, 2)

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📦 Fonction setup
# ║ Description : Fonction requise pour charger le cog
# ╚══════════════════════════════════════════════════════════════════════════════
async def setup(bot):
    """Charge le cog des commandes de base"""
    await bot.add_cog(CommandesBase(bot))





