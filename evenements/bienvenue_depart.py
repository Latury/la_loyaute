# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🦁 LA LOYAUTÉ - bienvenue_depart.py
# ║
# ║ 🎉 Gestion des arrivées et départs des membres
# ║ 👨‍💻 Développé par Latury
# ║ 📦 Version : 0.3.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

"""
🎉 Système de bienvenue et départ automatique
══════════════════════════════════════════════════════════════════════════════
"""

import discord
from discord.ext import commands
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import configuration as config
from utilitaires.logger import creer_logger

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📁 CONFIGURATION DES FICHIERS
# ╚══════════════════════════════════════════════════════════════════════════════

DONNEES_DIR = Path("donnees")
CONFIG_FILE = DONNEES_DIR / "bienvenue_config.json"

# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎉 COG PRINCIPAL - BienvenueDepart
# ╚══════════════════════════════════════════════════════════════════════════════

class BienvenueDepart(commands.Cog):
    """Gestion des événements d'arrivée et de départ des membres"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = creer_logger("bienvenue_depart", config.NIVEAU_LOG)
        self.config = self.charger_config()

        # Créer le dossier donnees si nécessaire
        DONNEES_DIR.mkdir(exist_ok=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 📂 GESTION DE LA CONFIGURATION
    # ╚══════════════════════════════════════════════════════════════════════════

    def charger_config(self):
        """Charge la configuration depuis le fichier JSON"""
        config_par_defaut = {
            "bienvenue": {
                "active": False,
                "salon_id": None,
                "message": "Bienvenue {mention} sur **{serveur}** ! 🎉",
                "embed_actif": True,
                "couleur": 0x57F287,  # Vert
                "role_auto_id": None
            },
            "depart": {
                "active": False,
                "salon_id": None,
                "message": "**{username}** a quitté le serveur. 👋",
                "embed_actif": True,
                "couleur": 0xED4245  # Rouge
            }
        }

        if not CONFIG_FILE.exists():
            self.sauvegarder_config(config_par_defaut)
            return config_par_defaut

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la config: {e}")
            return config_par_defaut

    def sauvegarder_config(self, config_data=None):
        """Sauvegarde la configuration dans le fichier JSON"""
        if config_data is None:
            config_data = self.config

        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            self.logger.info("Configuration sauvegardée")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🎉 ÉVÉNEMENT : Arrivée d'un nouveau membre
    # ╚══════════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Déclenché quand un nouveau membre rejoint le serveur"""
        conf = self.config["bienvenue"]

        # Vérifier si le système est activé
        if not conf["active"] or not conf["salon_id"]:
            return

        try:
            # Récupérer le salon de bienvenue
            salon = self.bot.get_channel(conf["salon_id"])
            if not salon:
                self.logger.warning(f"Salon de bienvenue introuvable: {conf['salon_id']}")
                return

            # Variables de remplacement
            variables = {
                "{mention}": member.mention,
                "{username}": member.name,
                "{serveur}": member.guild.name,
                "{compteur}": str(member.guild.member_count)
            }

            # Message de bienvenue
            if conf["embed_actif"]:
                embed = discord.Embed(
                    title="🎉 Nouveau membre !",
                    description=self._remplacer_variables(conf["message"], variables),
                    color=conf["couleur"],
                    timestamp=datetime.now(timezone.utc)
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(
                    text=f"Membre #{member.guild.member_count}",
                    icon_url=member.guild.icon.url if member.guild.icon else None
                )
                await salon.send(embed=embed)
            else:
                await salon.send(self._remplacer_variables(conf["message"], variables))

            # Attribution automatique du rôle
            if conf["role_auto_id"]:
                role = member.guild.get_role(conf["role_auto_id"])
                if role:
                    await member.add_roles(role, reason="Attribution automatique")
                    self.logger.info(f"Rôle {role.name} attribué à {member.name}")

            self.logger.info(f"Bienvenue envoyée pour {member.name}")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'envoi du message de bienvenue: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 👋 ÉVÉNEMENT : Départ d'un membre
    # ╚══════════════════════════════════════════════════════════════════════════

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Déclenché quand un membre quitte le serveur"""
        conf = self.config["depart"]

        # Vérifier si le système est activé
        if not conf["active"] or not conf["salon_id"]:
            return

        try:
            # Récupérer le salon de départ
            salon = self.bot.get_channel(conf["salon_id"])
            if not salon:
                self.logger.warning(f"Salon de départ introuvable: {conf['salon_id']}")
                return

            # Calculer le temps passé sur le serveur
            temps_passe = datetime.now(timezone.utc) - (member.joined_at or datetime.now(timezone.utc))
            jours = temps_passe.days

            # Variables de remplacement
            variables = {
                "{username}": member.name,
                "{serveur}": member.guild.name,
                "{jours}": str(jours),
                "{compteur}": str(member.guild.member_count)
            }

            # Message de départ
            if conf["embed_actif"]:
                embed = discord.Embed(
                    title="👋 Membre parti",
                    description=self._remplacer_variables(conf["message"], variables),
                    color=conf["couleur"],
                    timestamp=datetime.now(timezone.utc)
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.add_field(
                    name="📅 Temps passé",
                    value=f"{jours} jour(s)",
                    inline=True
                )
                embed.add_field(
                    name="👥 Membres restants",
                    value=str(member.guild.member_count),
                    inline=True
                )
                embed.set_footer(text=f"ID: {member.id}")
                await salon.send(embed=embed)
            else:
                await salon.send(self._remplacer_variables(conf["message"], variables))

            self.logger.info(f"Message de départ envoyé pour {member.name}")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'envoi du message de départ: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🔧 UTILITAIRES
    # ╚══════════════════════════════════════════════════════════════════════════

    def _remplacer_variables(self, texte: str, variables: dict) -> str:
        """Remplace les variables dans un texte"""
        for cle, valeur in variables.items():
            texte = texte.replace(cle, valeur)
        return texte

# ══════════════════════════════════════════════════════════════════════════
# ║ ⚙️ SETUP DU COG
# ══════════════════════════════════════════════════════════════════════════

async def setup(bot):
    """Charge le cog BienvenueDepart"""
    await bot.add_cog(BienvenueDepart(bot))
