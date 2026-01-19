# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🛡️ LA LOYAUTÉ - GESTIONNAIRE DE PERMISSIONS
# ║ Discord Bot | Système de vérification des permissions et des rôles
# ║ Développé par Latury
# ║ Version 0.2.2 (CORRIGÉ)
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from typing import Union

# Importation de la configuration
import configuration as config

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🔐 FONCTION 01 – est_developpeur
# ║ 📝 Vérifie si l'utilisateur est un développeur
# ╚═══════════════════════════════════════════════════════════════════════════════

def est_developpeur(user_id: int) -> bool:
    """Vérifie si l'utilisateur est un développeur"""
    return user_id in config.DEVELOPPEURS_IDS

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 👑 FONCTION 02 – est_administrateur
# ║ 📝 Vérifie si l'utilisateur est administrateur
# ╚═══════════════════════════════════════════════════════════════════════════════

def est_administrateur(member: discord.Member) -> bool:
    """Vérifie si le membre est administrateur"""

    # ── 🔹 Vérification du rôle admin configuré
    if config.ROLE_ADMIN_ID != 0:
        role_admin = discord.utils.get(member.roles, id=config.ROLE_ADMIN_ID)
        if role_admin:
            return True

    # ── 🔹 Vérification des permissions Discord
    return member.guild_permissions.administrator

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🛡️ FONCTION 03 – est_moderateur
# ║ 📝 Vérifie si l'utilisateur est modérateur
# ╚═══════════════════════════════════════════════════════════════════════════════

def est_moderateur(member: discord.Member) -> bool:
    """Vérifie si le membre est modérateur"""

    # ── 🔹 Les admins sont aussi modérateurs
    if est_administrateur(member):
        return True

    # ── 🔹 Vérification du rôle modérateur configuré
    if config.ROLE_MODERATEUR_ID != 0:
        role_moderateur = discord.utils.get(member.roles, id=config.ROLE_MODERATEUR_ID)
        if role_moderateur:
            return True

    # ── 🔹 Vérification des permissions Discord
    return (
        member.guild_permissions.kick_members or
        member.guild_permissions.ban_members or
        member.guild_permissions.manage_messages
    )

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 FONCTION 04 – est_proprietaire_serveur
# ║ 📝 Vérifie si l'utilisateur est le propriétaire du serveur
# ╚═══════════════════════════════════════════════════════════════════════════════

def est_proprietaire_serveur(member: discord.Member) -> bool:
    """Vérifie si le membre est le propriétaire du serveur"""

    if member.guild:
        return member.id == member.guild.owner_id
    return False

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ ✅ FONCTION 05 – verifier_permissions
# ║ 📝 Vérifie tous les niveaux de permissions
# ╚═══════════════════════════════════════════════════════════════════════════════

def verifier_permissions(member: discord.Member, niveau: str = "base") -> tuple[bool, str]:
    """
    Vérifie si le membre a les permissions requises

    Args:
        member: Le membre Discord à vérifier
        niveau: Le niveau requis ('base', 'moderateur', 'admin', 'developpeur')

    Returns:
        tuple: (bool: autorisé, str: raison)
    """

    # ── 🔹 Niveau développeur
    if niveau == "developpeur":
        if est_developpeur(member.id):
            return True, "Développeur autorisé"
        return False, "Cette commande est réservée aux développeurs"

    # ── 🔹 Niveau administrateur
    if niveau == "admin":
        if est_developpeur(member.id) or est_administrateur(member):
            return True, "Administrateur autorisé"
        return False, "Cette commande est réservée aux administrateurs"

    # ── 🔹 Niveau modérateur
    if niveau == "moderateur":
        if est_developpeur(member.id) or est_moderateur(member):
            return True, "Modérateur autorisé"
        return False, "Cette commande est réservée aux modérateurs"

    # ── 🔹 Niveau base (tout le monde)
    return True, "Utilisateur autorisé"

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🎭 CLASSE 01 – Décorateurs pour les checks
# ║ 📝 Décorateurs personnalisés pour les commandes
# ╚═══════════════════════════════════════════════════════════════════════════════

def require_admin():
    """Décorateur pour exiger les permissions admin"""
    async def predicate(ctx):
        if not isinstance(ctx.author, discord.Member):
            raise commands.CheckFailure("Cette commande ne peut pas être utilisée en messages privés")

        autorise, raison = verifier_permissions(ctx.author, "admin")
        if not autorise:
            raise commands.CheckFailure(raison)
        return True

    return commands.check(predicate)

def require_moderator():
    """Décorateur pour exiger les permissions modérateur"""
    async def predicate(ctx):
        if not isinstance(ctx.author, discord.Member):
            raise commands.CheckFailure("Cette commande ne peut pas être utilisée en messages privés")

        autorise, raison = verifier_permissions(ctx.author, "moderateur")
        if not autorise:
            raise commands.CheckFailure(raison)
        return True

    return commands.check(predicate)

def require_developer():
    """Décorateur pour exiger les permissions développeur"""
    async def predicate(ctx):
        autorise, raison = verifier_permissions(ctx.author, "developpeur")
        if not autorise:
            raise commands.CheckFailure(raison)
        return True

    return commands.check(predicate)

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 📊 FONCTION 06 – obtenir_niveau_permission
# ║ 📝 Retourne le niveau de permission d'un utilisateur
# ╚═══════════════════════════════════════════════════════════════════════════════

def obtenir_niveau_permission(member: discord.Member) -> str:
    """Retourne le niveau de permission d'un membre"""

    if est_developpeur(member.id):
        return "👨‍💻 Développeur"
    elif est_proprietaire_serveur(member):
        return "👑 Propriétaire"
    elif est_administrateur(member):
        return "🛡️ Administrateur"
    elif est_moderateur(member):
        return "⚔️ Modérateur"
    else:
        return "👤 Utilisateur"

# ╔══════════════════════════════════════════════════════════════════════════════
# ║  FIN DU FICHIER gestionnaire_permissions.py
# ╚══════════════════════════════════════════════════════════════════════════════
