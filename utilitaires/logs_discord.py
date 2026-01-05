# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 📊 LA LOYAUTÉ - SYSTÈME DE LOGS DISCORD
# ║
# ║ Gestion des logs dans un salon Discord dédié
# ║ Développé par Latury
# ║ Version : 0.2.1
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from datetime import datetime
from typing import Optional, List, Dict, Any
import configuration as config
from utilitaires.helpers import creer_embed


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📝 FONCTION 01 – Envoi d'un log dans le salon
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
    try:
        # ── 🔹 ÉTAPE 1 : Récupération du salon de logs via le gestionnaire
        salon_id = bot.config_manager.obtenir_salon_logs(guild.id)

        # ── 🔹 ÉTAPE 2 : Vérification si un salon est configuré
        if not salon_id:
            # Aucun salon configuré pour ce serveur
            bot.logger.debug(f"Aucun salon de logs configuré pour {guild.name}")
            return

        # ── 🔹 ÉTAPE 3 : Récupération du salon Discord
        salon_logs = guild.get_channel(salon_id)

        if not salon_logs:
            bot.logger.warning(
                f"⚠️ Salon de logs (ID: {salon_id}) introuvable pour {guild.name}"
            )
            return

        # ── 🔹 ÉTAPE 4 : Vérification du type de salon
        if not isinstance(salon_logs, (discord.TextChannel, discord.Thread)):
            bot.logger.error(f"❌ Le salon de logs doit être un salon textuel")
            return

        # ── 🔹 ÉTAPE 5 : Création de l'embed
        embed = creer_embed(
            titre=titre,
            description=description,
            couleur=couleur,
            footer=False
        )

        # ── 🔹 ÉTAPE 6 : Ajout des champs
        if champs:
            for champ in champs:
                embed.add_field(
                    name=champ.get('name', 'Info'),
                    value=champ.get('value', 'N/A'),
                    inline=champ.get('inline', True)
                )

        # ── 🔹 ÉTAPE 7 : Ajout de la miniature
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        # ── 🔹 ÉTAPE 8 : Footer personnalisé
        embed.set_footer(text=f"{guild.name} • Logs")
        embed.timestamp = datetime.now()

        # ── 🔹 ÉTAPE 9 : Envoi
        await salon_logs.send(embed=embed)

    except discord.Forbidden:
        bot.logger.error(f"❌ Permissions manquantes pour envoyer dans le salon de logs")
    except Exception as e:
        bot.logger.error(f"❌ Erreur lors de l'envoi du log : {e}")


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🚫 FONCTION 02 – Log d'expulsion
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
# ║ 🔨 FONCTION 03 – Log de bannissement
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
# ║ 🔓 FONCTION 04 – Log de débannissement
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
# ║ 🔇 FONCTION 05 – Log de timeout
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
# ║ ⚠️ FONCTION 06 – Log d'avertissement
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
# ║ 🧹 FONCTION 07 – Log de nettoyage de messages
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
# ║ 👋 FONCTION 08 – Log d'arrivée
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
# ║ 👋 FONCTION 09 – Log de départ
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


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🗑️ FONCTION 10 – Log de message supprimé
# ║ Description : Log la suppression d'un message
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_message_delete(bot, message: discord.Message):
    """Log la suppression d'un message"""
    # ── 🔹 Ignorer les messages des bots
    if message.author.bot:
        return

    # ── 🔹 Vérifier que c'est un message de serveur
    if not message.guild:
        return

    # ── 🔹 Construction des champs
    champs = [
        {"name": "👤 Auteur", "value": f"{message.author.mention}\n`{message.author.id}`", "inline": True},
    ]

    # ── 🔹 Salon (avec vérification du type)
    if isinstance(message.channel, (discord.TextChannel, discord.Thread)):
        champs.append({"name": "📍 Salon", "value": message.channel.mention, "inline": True})
    else:
        champs.append({"name": "📍 Salon", "value": f"#{getattr(message.channel, 'name', 'Inconnu')}", "inline": True})

    # ── 🔹 Contenu du message (si présent)
    if message.content:
        contenu = message.content
        if len(contenu) > 1024:
            contenu = contenu[:1021] + "..."
        champs.append({"name": "💬 Contenu", "value": contenu, "inline": False})

    # ── 🔹 Pièces jointes (si présentes)
    if message.attachments:
        attachments_info = "\n".join([f"📎 [{att.filename}]({att.url})" for att in message.attachments])
        if len(attachments_info) > 1024:
            attachments_info = attachments_info[:1021] + "..."
        champs.append({"name": "📎 Pièces jointes", "value": attachments_info, "inline": False})

    thumbnail_url = message.author.display_avatar.url if message.author.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=message.guild,
        titre="🗑️ Message supprimé",
        description=f"Un message de **{message.author}** a été supprimé",
        couleur=config.COULEUR_ERREUR,
        champs=champs,
        thumbnail=thumbnail_url
    )



# ╔══════════════════════════════════════════════════════════════════════════════
# ║ ✏️ FONCTION 11 – Log de message modifié
# ║ Description : Log la modification d'un message
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_message_edit(bot, before: discord.Message, after: discord.Message):
    """Log la modification d'un message"""
    # ── 🔹 Ignorer les messages des bots
    if after.author.bot:
        return

    # ── 🔹 Vérifier que c'est un message de serveur
    if not after.guild:
        return

    # ── 🔹 Ignorer si le contenu n'a pas changé
    if before.content == after.content:
        return

    # ── 🔹 Construction des champs
    champs = [
        {"name": "👤 Auteur", "value": f"{after.author.mention}\n`{after.author.id}`", "inline": True},
    ]

    # ── 🔹 Salon (avec vérification du type)
    if isinstance(after.channel, (discord.TextChannel, discord.Thread)):
        champs.append({"name": "📍 Salon", "value": after.channel.mention, "inline": True})
    else:
        champs.append({"name": "📍 Salon", "value": f"#{getattr(after.channel, 'name', 'Inconnu')}", "inline": True})

    champs.append({"name": "🔗 Lien", "value": f"[Aller au message]({after.jump_url})", "inline": True})

    # ── 🔹 Contenu avant
    before_content = before.content if before.content else "*Aucun contenu*"
    if len(before_content) > 1024:
        before_content = before_content[:1021] + "..."
    champs.append({"name": "📝 Avant", "value": before_content, "inline": False})

    # ── 🔹 Contenu après
    after_content = after.content if after.content else "*Aucun contenu*"
    if len(after_content) > 1024:
        after_content = after_content[:1021] + "..."
    champs.append({"name": "✅ Après", "value": after_content, "inline": False})

    thumbnail_url = after.author.display_avatar.url if after.author.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=after.guild,
        titre="✏️ Message modifié",
        description=f"**{after.author}** a modifié un message",
        couleur=config.COULEUR_AVERTISSEMENT,
        champs=champs,
        thumbnail=thumbnail_url
    )



# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🎭 FONCTION 12 – Log de mise à jour des rôles
# ║ Description : Log les changements de rôles d'un membre
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_member_roles_update(bot, before: discord.Member, after: discord.Member):
    """Log les changements de rôles d'un membre"""
    # ── 🔹 Détection des rôles ajoutés/retirés
    roles_added = [role for role in after.roles if role not in before.roles]
    roles_removed = [role for role in before.roles if role not in after.roles]

    # ── 🔹 Si aucun changement de rôle, on ignore
    if not roles_added and not roles_removed:
        return

    # ── 🔹 Construction des champs
    champs = [
        {"name": "👤 Membre", "value": f"{after.mention}\n`{after.id}`", "inline": True}
    ]

    # ── 🔹 Rôles ajoutés
    if roles_added:
        roles_text = ", ".join([role.mention for role in roles_added])
        champs.append({"name": "➕ Rôle(s) ajouté(s)", "value": roles_text, "inline": False})

    # ── 🔹 Rôles retirés
    if roles_removed:
        roles_text = ", ".join([role.mention for role in roles_removed])
        champs.append({"name": "➖ Rôle(s) retiré(s)", "value": roles_text, "inline": False})

    # ── 🔹 Choix du titre et de la couleur
    if roles_added:
        titre = "🎭 Rôle ajouté"
        couleur = config.COULEUR_SUCCES
    else:
        titre = "🎭 Rôle retiré"
        couleur = config.COULEUR_ERREUR

    thumbnail_url = after.display_avatar.url if after.display_avatar else None

    await envoyer_log(
        bot=bot,
        guild=after.guild,
        titre=titre,
        description=f"Les rôles de **{after}** ont changé",
        couleur=couleur,
        champs=champs,
        thumbnail=thumbnail_url
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🏗️ FONCTION 13 – Log de création de salon
# ║ Description : Log la création d'un salon
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_channel_create(bot, channel):
    """Log la création d'un salon"""
    # ── 🔹 Détermination du type de salon
    channel_type = {
        discord.ChannelType.text: "📝 Textuel",
        discord.ChannelType.voice: "🔊 Vocal",
        discord.ChannelType.category: "📁 Catégorie",
        discord.ChannelType.news: "📰 Annonces",
        discord.ChannelType.forum: "💬 Forum",
    }.get(channel.type, "❓ Autre")

    # ── 🔹 Construction des champs
    champs = [
        {"name": "📍 Salon", "value": f"{channel.mention if hasattr(channel, 'mention') else channel.name}\n`{channel.id}`", "inline": True},
        {"name": "🏷️ Type", "value": channel_type, "inline": True}
    ]

    # ── 🔹 Catégorie parente (si applicable)
    if hasattr(channel, 'category') and channel.category:
        champs.append({"name": "📁 Catégorie", "value": channel.category.name, "inline": True})

    await envoyer_log(
        bot=bot,
        guild=channel.guild,
        titre="🏗️ Salon créé",
        description=f"Un nouveau salon a été créé",
        couleur=config.COULEUR_SUCCES,
        champs=champs
    )


# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🗑️ FONCTION 14 – Log de suppression de salon
# ║ Description : Log la suppression d'un salon
# ╚══════════════════════════════════════════════════════════════════════════════

async def log_channel_delete(bot, channel):
    """Log la suppression d'un salon"""
    # ── 🔹 Détermination du type de salon
    channel_type = {
        discord.ChannelType.text: "📝 Textuel",
        discord.ChannelType.voice: "🔊 Vocal",
        discord.ChannelType.category: "📁 Catégorie",
        discord.ChannelType.news: "📰 Annonces",
        discord.ChannelType.forum: "💬 Forum",
    }.get(channel.type, "❓ Autre")

    # ── 🔹 Construction des champs
    champs = [
        {"name": "📍 Nom", "value": f"#{channel.name}\n`{channel.id}`", "inline": True},
        {"name": "🏷️ Type", "value": channel_type, "inline": True}
    ]

    # ── 🔹 Catégorie parente (si applicable)
    if hasattr(channel, 'category') and channel.category:
        champs.append({"name": "📁 Catégorie", "value": channel.category.name, "inline": True})

    await envoyer_log(
        bot=bot,
        guild=channel.guild,
        titre="🗑️ Salon supprimé",
        description=f"Un salon a été supprimé",
        couleur=config.COULEUR_ERREUR,
        champs=champs
    )


# ═══════════════════════════════════════════════════════════════════════════════
# FIN DU FICHIER logs_discord.py
# ═══════════════════════════════════════════════════════════════════════════════
