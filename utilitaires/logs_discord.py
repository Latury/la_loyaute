# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║  📊 LA LOYAUTÉ - SYSTÈME DE LOGS DISCORD
# ║
# ║  Gestion des logs dans un salon Discord dédié
# ║  Développé par Latury
# ║  Version : 0.2.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from datetime import datetime
from typing import Optional, List, Dict, Any
import configuration as config
from utilitaires.helpers import creer_embed


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📝 Fonction 01 – Envoi d'un log dans le salon
# ║ Description : Envoie un embed de log dans le salon configuré
# ╚══════════════════════════════════════════════════════════════════════════════

async def envoyer_log(
    bot,
    guild: discord.Guild,
    titre: str,
    description: str = "",
    couleur: int = config.COULEUR_PRINCIPALE,
    champs: Optional[List[Dict[str, Any]]] = None,
    thumbnail: Optional[str] = None
):
    """
    Envoie un log dans le salon de logs configuré

    Args:
        bot: Instance du bot
        guild: Serveur Discord
        titre: Titre du log
        description: Description du log
        couleur: Couleur de l'embed
        champs: Liste de dictionnaires {name, value, inline}
        thumbnail: URL de la miniature
    """

    # ── 🔹 Vérification du salon de logs
    if config.LOGS_CHANNEL_ID == 0:
        return  # Pas de salon configuré

    try:
        salon_logs = guild.get_channel(config.LOGS_CHANNEL_ID)

        if not salon_logs:
            bot.logger.warning(f"⚠️ Salon de logs (ID: {config.LOGS_CHANNEL_ID}) introuvable")
            return

        # ── 🔹 Vérification du type de salon
        if not isinstance(salon_logs, (discord.TextChannel, discord.Thread)):
            bot.logger.error(f"❌ Le salon de logs doit être un salon textuel")
            return

        # ── 🔹 Création de l'embed
        embed = creer_embed(
            titre=titre,
            description=description,
            couleur=couleur,
            footer=False
        )

        # ── 🔹 Ajout des champs
        if champs:
            for champ in champs:
                embed.add_field(
                    name=champ.get('name', 'Info'),
                    value=champ.get('value', 'N/A'),
                    inline=champ.get('inline', True)
                )

        # ── 🔹 Ajout de la miniature
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        # ── 🔹 Footer personnalisé
        embed.set_footer(text=f"{guild.name} • Logs")
        embed.timestamp = datetime.now()

        # ── 🔹 Envoi
        await salon_logs.send(embed=embed)

    except discord.Forbidden:
        bot.logger.error(f"❌ Permissions manquantes pour envoyer dans le salon de logs")
    except Exception as e:
        bot.logger.error(f"❌ Erreur lors de l'envoi du log : {e}")


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🚫 Fonction 02 – Log d'expulsion
# ║ Description : Log une expulsion
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_kick(bot, guild: discord.Guild, membre: discord.Member, moderateur: discord.User | discord.Member, raison: str):
    """Log une expulsion"""
    thumbnail_url = membre.display_avatar.url if membre.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=guild,
        titre="🚫 Membre expulsé",
        description=f"**{membre}** a été expulsé du serveur",
        couleur=config.COULEUR_AVERTISSEMENT,
        champs=[
            {"name": "Membre", "value": f"{membre.mention}\n`{membre.id}`", "inline": True},
            {"name": "Modérateur", "value": moderateur.mention, "inline": True},
            {"name": "Raison", "value": raison, "inline": False}
        ],
        thumbnail=thumbnail_url
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🔨 Fonction 03 – Log de bannissement
# ║ Description : Log un bannissement
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_ban(bot, guild: discord.Guild, membre: discord.Member, moderateur: discord.User | discord.Member, raison: str, jours_messages: int = 0):
    """Log un bannissement"""

    champs = [
        {"name": "Membre", "value": f"{membre.mention}\n`{membre.id}`", "inline": True},
        {"name": "Modérateur", "value": moderateur.mention, "inline": True},
        {"name": "Raison", "value": raison, "inline": False}
    ]

    if jours_messages > 0:
        champs.append({"name": "Messages supprimés", "value": f"{jours_messages} jour(s)", "inline": True})

    thumbnail_url = membre.display_avatar.url if membre.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=guild,
        titre="🔨 Membre banni",
        description=f"**{membre}** a été banni du serveur",
        couleur=config.COULEUR_ERREUR,
        champs=champs,
        thumbnail=thumbnail_url
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🔓 Fonction 04 – Log de débannissement
# ║ Description : Log un débannissement
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_unban(bot, guild: discord.Guild, utilisateur: discord.User, moderateur: discord.User | discord.Member, raison: str):
    """Log un débannissement"""

    thumbnail_url = utilisateur.display_avatar.url if utilisateur.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=guild,
        titre="🔓 Membre débanni",
        description=f"**{utilisateur}** a été débanni du serveur",
        couleur=config.COULEUR_SUCCES,
        champs=[
            {"name": "Utilisateur", "value": f"{utilisateur.mention}\n`{utilisateur.id}`", "inline": True},
            {"name": "Modérateur", "value": moderateur.mention, "inline": True},
            {"name": "Raison", "value": raison, "inline": False}
        ],
        thumbnail=thumbnail_url
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🔇 Fonction 05 – Log de timeout
# ║ Description : Log un timeout
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_timeout(bot, guild: discord.Guild, membre: discord.Member, moderateur: discord.User | discord.Member, duree: str, raison: str):
    """Log un timeout"""

    thumbnail_url = membre.display_avatar.url if membre.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=guild,
        titre="🔇 Membre mis en timeout",
        description=f"**{membre}** a été mis en timeout",
        couleur=config.COULEUR_AVERTISSEMENT,
        champs=[
            {"name": "Membre", "value": f"{membre.mention}\n`{membre.id}`", "inline": True},
            {"name": "Durée", "value": duree, "inline": True},
            {"name": "Modérateur", "value": moderateur.mention, "inline": True},
            {"name": "Raison", "value": raison, "inline": False}
        ],
        thumbnail=thumbnail_url
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ ⚠️ Fonction 06 – Log d'avertissement
# ║ Description : Log un avertissement
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_warn(bot, guild: discord.Guild, membre: discord.Member, moderateur: discord.User | discord.Member, raison: str, warn_id: int, total: int):
    """Log un avertissement"""

    thumbnail_url = membre.display_avatar.url if membre.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=guild,
        titre="⚠️ Avertissement donné",
        description=f"**{membre}** a reçu un avertissement",
        couleur=config.COULEUR_AVERTISSEMENT,
        champs=[
            {"name": "Membre", "value": f"{membre.mention}\n`{membre.id}`", "inline": True},
            {"name": "Warn ID", "value": f"#{warn_id}", "inline": True},
            {"name": "Total", "value": f"{total} warn(s)", "inline": True},
            {"name": "Modérateur", "value": moderateur.mention, "inline": True},
            {"name": "Raison", "value": raison, "inline": False}
        ],
        thumbnail=thumbnail_url
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🧹 Fonction 07 – Log de nettoyage de messages
# ║ Description : Log une suppression de messages en masse
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_clear(bot, guild: discord.Guild, salon: discord.TextChannel, moderateur: discord.User | discord.Member, nombre: int):
    """Log un clear de messages"""

    await envoyer_log(
        bot=bot,
        guild=guild,
        titre="🧹 Messages supprimés",
        description=f"**{nombre}** message(s) supprimé(s)",
        couleur=config.COULEUR_INFO,
        champs=[
            {"name": "Salon", "value": salon.mention, "inline": True},
            {"name": "Nombre", "value": str(nombre), "inline": True},
            {"name": "Modérateur", "value": moderateur.mention, "inline": True}
        ]
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 👋 Fonction 08 – Log d'arrivée
# ║ Description : Log l'arrivée d'un membre
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_member_join(bot, membre: discord.Member):
    """Log l'arrivée d'un membre"""

    # ── 🔹 Calcul de l'âge du compte
    age_compte = datetime.now(membre.created_at.tzinfo) - membre.created_at
    jours = age_compte.days

    thumbnail_url = membre.display_avatar.url if membre.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=membre.guild,
        titre="👋 Nouveau membre",
        description=f"**{membre}** a rejoint le serveur",
        couleur=config.COULEUR_SUCCES,
        champs=[
            {"name": "Membre", "value": f"{membre.mention}\n`{membre.id}`", "inline": True},
            {"name": "Compte créé", "value": f"Il y a {jours} jour(s)", "inline": True},
            {"name": "Membres totaux", "value": str(membre.guild.member_count), "inline": True}
        ],
        thumbnail=thumbnail_url
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 👋 Fonction 09 – Log de départ
# ║ Description : Log le départ d'un membre
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_member_leave(bot, membre: discord.Member):
    """Log le départ d'un membre"""
    thumbnail_url = membre.display_avatar.url if membre.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=membre.guild,
        titre="👋 Membre parti",
        description=f"**{membre}** a quitté le serveur",
        couleur=config.COULEUR_ERREUR,
        champs=[
            {"name": "Membre", "value": f"{membre.mention}\n`{membre.id}`", "inline": True},
            {"name": "Membres restants", "value": str(membre.guild.member_count), "inline": True}
        ],
        thumbnail=thumbnail_url
    )
