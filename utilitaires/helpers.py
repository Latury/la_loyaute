# ═══════════════════════════════════════════════════════════════════════════════
# ║                                                                             
# ║  🔧 LA LOYAUTÉ - FONCTIONS UTILITAIRES
# ║
# ║  Fonctions helpers réutilisables dans tout le projet
# ║  Développé par Latury
# ║  Version : 0.1.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import discord
from datetime import datetime, timedelta
from typing import Union, Optional
import re

# Importation de la configuration
import configuration as config

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📅 Fonction 01 – Formatage de la date
# ║ Description : Formate une date au format français
# ╚══════════════════════════════════════════════════════════════════════════════
def formater_date(date: datetime, inclure_heure: bool = True) -> str:
    """
    Formate une date au format français

    Args:
        date: La date à formater
        inclure_heure: Inclure l'heure dans le formatage

    Returns:
        str: Date formatée (ex: "24/12/2025 05:03:00")
    """

    if inclure_heure:
        return date.strftime('%d/%m/%Y %H:%M:%S')
    else:
        return date.strftime('%d/%m/%Y')

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ ⏱️ Fonction 02 – Formatage de la durée
# ║ Description : Convertit un timedelta en texte lisible
# ╚══════════════════════════════════════════════════════════════════════════════
def formater_duree(duree: timedelta) -> str:
    """
    Formate une durée en texte lisible

    Args:
        duree: La durée à formater

    Returns:
        str: Durée formatée (ex: "2j 5h 30m")
    """

    secondes_totales = int(duree.total_seconds())

    jours, reste = divmod(secondes_totales, 86400)
    heures, reste = divmod(reste, 3600)
    minutes, secondes = divmod(reste, 60)

    parties = []

    if jours > 0:
        parties.append(f"{jours}j")
    if heures > 0:
        parties.append(f"{heures}h")
    if minutes > 0:
        parties.append(f"{minutes}m")
    if secondes > 0 and not parties:  # Affiche secondes seulement si < 1 minute
        parties.append(f"{secondes}s")

    return " ".join(parties) if parties else "0s"

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🎨 Fonction 03 – Création d'embed de base
# ║ Description : Crée un embed Discord avec style uniforme
# ╚══════════════════════════════════════════════════════════════════════════════
def creer_embed(
    titre: str,
    description: str = "",
    couleur: int = config.COULEUR_PRINCIPALE,
    footer: bool = True,
    timestamp: bool = True
) -> discord.Embed:
    """
    Crée un embed Discord avec le style du bot

    Args:
        titre: Titre de l'embed
        description: Description de l'embed
        couleur: Couleur de l'embed (hex)
        footer: Ajouter le footer avec nom du bot
        timestamp: Ajouter le timestamp

    Returns:
        discord.Embed: L'embed créé
    """

    embed = discord.Embed(
        title=titre,
        description=description,
        color=couleur
    )

    # ── 🔹 Ajout du footer
    if footer:
        embed.set_footer(
            text=f"{config.NOM_BOT} v{config.VERSION_BOT} • Par {config.DEVELOPPEUR}",
            icon_url=None  # Peut être défini plus tard avec le logo du bot
        )

    # ── 🔹 Ajout du timestamp
    if timestamp:
        embed.timestamp = datetime.now()

    return embed

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ ✅ Fonction 04 – Embed de succès
# ║ Description : Crée un embed de succès avec style prédéfini
# ╚══════════════════════════════════════════════════════════════════════════════
def creer_embed_succes(titre: str, description: str = "") -> discord.Embed:
    """Crée un embed de succès"""

    return creer_embed(
        titre=f"{config.EMOJI_SUCCES} {titre}",
        description=description,
        couleur=config.COULEUR_SUCCES
    )

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ ❌ Fonction 05 – Embed d'erreur
# ║ Description : Crée un embed d'erreur avec style prédéfini
# ╚══════════════════════════════════════════════════════════════════════════════
def creer_embed_erreur(titre: str, description: str = "") -> discord.Embed:
    """Crée un embed d'erreur"""

    return creer_embed(
        titre=f"{config.EMOJI_ERREUR} {titre}",
        description=description,
        couleur=config.COULEUR_ERREUR
    )

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ ⚠️ Fonction 06 – Embed d'avertissement
# ║ Description : Crée un embed d'avertissement avec style prédéfini
# ╚══════════════════════════════════════════════════════════════════════════════
def creer_embed_avertissement(titre: str, description: str = "") -> discord.Embed:
    """Crée un embed d'avertissement"""

    return creer_embed(
        titre=f"{config.EMOJI_AVERTISSEMENT} {titre}",
        description=description,
        couleur=config.COULEUR_AVERTISSEMENT
    )

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ ℹ️ Fonction 07 – Embed d'information
# ║ Description : Crée un embed d'information avec style prédéfini
# ╚══════════════════════════════════════════════════════════════════════════════
def creer_embed_info(titre: str, description: str = "") -> discord.Embed:
    """Crée un embed d'information"""

    return creer_embed(
        titre=f"{config.EMOJI_INFO} {titre}",
        description=description,
        couleur=config.COULEUR_INFO
    )

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🔢 Fonction 08 – Formatage des nombres
# ║ Description : Formate un nombre avec séparateurs de milliers
# ╚══════════════════════════════════════════════════════════════════════════════
def formater_nombre(nombre: int) -> str:
    """
    Formate un nombre avec des espaces comme séparateurs

    Args:
        nombre: Le nombre à formater

    Returns:
        str: Nombre formaté (ex: "1 234 567")
    """

    return f"{nombre:,}".replace(',', ' ')

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📊 Fonction 09 – Barre de progression
# ║ Description : Crée une barre de progression visuelle
# ╚══════════════════════════════════════════════════════════════════════════════
def creer_barre_progression(
    valeur_actuelle: int,
    valeur_max: int,
    longueur: int = 10,
    caractere_rempli: str = "█",
    caractere_vide: str = "░"
) -> str:
    """
    Crée une barre de progression

    Args:
        valeur_actuelle: Valeur actuelle
        valeur_max: Valeur maximale
        longueur: Longueur de la barre
        caractere_rempli: Caractère pour la partie remplie
        caractere_vide: Caractère pour la partie vide

    Returns:
        str: Barre de progression (ex: "████░░░░░░ 40%")
    """

    if valeur_max == 0:
        pourcentage = 0
    else:
        pourcentage = min(100, max(0, int((valeur_actuelle / valeur_max) * 100)))

    rempli = int((pourcentage / 100) * longueur)
    vide = longueur - rempli

    barre = caractere_rempli * rempli + caractere_vide * vide

    return f"{barre} {pourcentage}%"

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🔗 Fonction 10 – Validation d'URL
# ║ Description : Vérifie si une chaîne est une URL valide
# ╚══════════════════════════════════════════════════════════════════════════════
def est_url_valide(url: str) -> bool:
    """
    Vérifie si une chaîne est une URL valide

    Args:
        url: L'URL à vérifier

    Returns:
        bool: True si l'URL est valide
    """

    regex_url = re.compile(
        r'^https?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domaine
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ou IP
        r'(?::\d+)?'  # port optionnel
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return url is not None and regex_url.search(url) is not None

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📝 Fonction 11 – Tronquer un texte
# ║ Description : Tronque un texte avec ellipse si trop long
# ╚══════════════════════════════════════════════════════════════════════════════
def tronquer_texte(texte: str, longueur_max: int = 100, ellipse: str = "...") -> str:
    """
    Tronque un texte s'il dépasse la longueur maximale

    Args:
        texte: Le texte à tronquer
        longueur_max: Longueur maximale
        ellipse: Caractères à ajouter à la fin

    Returns:
        str: Texte tronqué
    """

    if len(texte) <= longueur_max:
        return texte

    return texte[:longueur_max - len(ellipse)] + ellipse

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 👤 Fonction 12 – Obtenir le nom d'affichage
# ║ Description : Obtient le meilleur nom à afficher pour un utilisateur
# ╚══════════════════════════════════════════════════════════════════════════════
def obtenir_nom_affichage(user: Union[discord.User, discord.Member]) -> str:
    """
    Obtient le meilleur nom à afficher pour un utilisateur

    Args:
        user: L'utilisateur Discord

    Returns:
        str: Le nom à afficher
    """

    if isinstance(user, discord.Member) and user.nick:
        return user.nick
    return user.display_name
