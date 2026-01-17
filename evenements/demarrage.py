# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                               ║
# ║  🚀 LA LOYAUTÉ - ÉVÉNEMENT DE DÉMARRAGE                                      ║
# ║  Discord Bot | Gestion de l'initialisation et de l'affichage de démarrage    ║
# ║  Développé par Latury                                                        ║
# ║  Version 0.2.2                                                               ║
# ║                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🚀 FICHIER : demarrage.py
# ║ 📦 MODULE : evenements
# ║ 📝 DESCRIPTION : Gestion de l'événement on_ready et affichage professionnel
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15 janvier 2026
# ║ 🔖 VERSION : 0.2.2
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

import discord
from discord.ext import commands
from datetime import datetime

# Importation de la configuration
import configuration as config
from utilitaires.helpers import formater_date, formater_nombre

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 📦 CLASSE 01 – Demarrage
# ║ 🎯 Cog gérant l'événement de démarrage du bot Discord
# ╚═══════════════════════════════════════════════════════════════════════════════
class Demarrage(commands.Cog):
    """Cog gérant l'événement de démarrage du bot"""

    def __init__(self, bot):
        """Initialise le cog de démarrage"""

        self.bot = bot
        self.demarrage_effectue = False

    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ 🎨 FONCTION 01 – creer_cadre_demarrage
    # ║ 📝 Crée un cadre ASCII professionnel avec les infos de démarrage
    # ╚═══════════════════════════════════════════════════════════════════════════════
    def creer_cadre_demarrage(self) -> list:
        """Crée le cadre de démarrage professionnel"""

        # ── 🔹 Récupération des statistiques
        stats = self.bot.obtenir_statistiques()
        date_heure = formater_date(datetime.now())

        # ── 🔹 Construction du cadre (sans emojis pour éviter problèmes d'alignement)
        lignes = []
        largeur = 78

        # Bordure supérieure
        lignes.append("╔" + "═" * largeur + "╗")
        lignes.append("║" + " " * largeur + "║")

        # Titre principal
        titre = "LA LOYAUTE - BOT DISCORD"
        lignes.append("║" + titre.center(largeur) + "║")
        lignes.append("║" + " " * largeur + "║")

        # Informations de version
        version = f"Version {config.VERSION_BOT}"
        lignes.append("║" + version.center(largeur) + "║")

        developpeur = f"Developpe par {config.DEVELOPPEUR}"
        lignes.append("║" + developpeur.center(largeur) + "║")
        lignes.append("║" + " " * largeur + "║")

        # Séparateur
        lignes.append("╠" + "═" * largeur + "╣")
        lignes.append("║" + " " * largeur + "║")

        # Informations du bot
        info_bot = f"Bot connecte : {stats['nom']}"
        lignes.append("║  " + info_bot.ljust(largeur - 2) + "║")

        info_id = f"ID : {stats['id']}"
        lignes.append("║  " + info_id.ljust(largeur - 2) + "║")
        lignes.append("║" + " " * largeur + "║")

        # Statistiques
        stat_serveurs = f"Serveurs connectes : {formater_nombre(stats['serveurs'])}"
        lignes.append("║  " + stat_serveurs.ljust(largeur - 2) + "║")

        stat_users = f"Utilisateurs accessibles : {formater_nombre(stats['utilisateurs'])}"
        lignes.append("║  " + stat_users.ljust(largeur - 2) + "║")

        stat_commandes = f"Commandes chargees : {stats['commandes']}"
        lignes.append("║  " + stat_commandes.ljust(largeur - 2) + "║")

        stat_latence = f"Latence : {stats['latence']} ms"
        lignes.append("║  " + stat_latence.ljust(largeur - 2) + "║")
        lignes.append("║" + " " * largeur + "║")

        # Informations de démarrage
        info_date = f"Demarre le : {date_heure}"
        lignes.append("║  " + info_date.ljust(largeur - 2) + "║")

        info_prefix = f"Prefix commandes : {config.PREFIX_BASE} (base) | {config.PREFIX_ADMIN} (admin)"
        lignes.append("║  " + info_prefix.ljust(largeur - 2) + "║")
        lignes.append("║" + " " * largeur + "║")

        # Séparateur
        lignes.append("╠" + "═" * largeur + "╣")
        lignes.append("║" + " " * largeur + "║")

        # Statut final
        statut = "BOT OPERATIONNEL ET PRET A L'EMPLOI"
        lignes.append("║" + statut.center(largeur) + "║")
        lignes.append("║" + " " * largeur + "║")

        # Bordure inférieure
        lignes.append("╚" + "═" * largeur + "╝")

        return lignes

    # ╔═══════════════════════════════════════════════════════════════════════════════
    # ║ 🎯 FONCTION 02 – on_ready
    # ║ 📝 Événement déclenché quand le bot est connecté et prêt
    # ╚═══════════════════════════════════════════════════════════════════════════════
    @commands.Cog.listener()
    async def on_ready(self):
        """Événement déclenché quand le bot est prêt"""

        # ── 🔹 Éviter les exécutions multiples
        if self.demarrage_effectue:
            self.bot.logger.info("🔄 Reconnexion détectée")
            return

        self.demarrage_effectue = True

        # ── 🔹 Affichage du cadre de démarrage
        self.bot.logger.info("")
        self.bot.logger.info("")

        cadre = self.creer_cadre_demarrage()
        for ligne in cadre:
            self.bot.logger.info(ligne)

        self.bot.logger.info("")
        self.bot.logger.info("")

        # ── 🔹 Informations supplémentaires (avec emojis ici, hors du cadre)
        self.bot.logger.info("=" * 80)
        self.bot.logger.info("  📋  INFORMATIONS COMPLEMENTAIRES")
        self.bot.logger.info("=" * 80)

        # Liste des serveurs
        if self.bot.guilds:
            self.bot.logger.info("  🏠  Serveurs :")
            for guild in self.bot.guilds:
                nom_serveur = guild.name[:60]
                info = f"       • {nom_serveur} (ID: {guild.id}) - {guild.member_count} membres"
                self.bot.logger.info(info)

        self.bot.logger.info("=" * 80)
        self.bot.logger.info("")

        # ── 🔹 Message de confirmation
        self.bot.logger.info("🎉 Le bot La Loyaute est maintenant en ligne et operationnel !")
        self.bot.logger.info(f"💡 Tapez {config.PREFIX_BASE}aide pour voir les commandes disponibles")
        self.bot.logger.info("")

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🔌 FONCTION SETUP – setup
# ║ 📝 Charge le cog de démarrage dans le bot Discord
# ╚═══════════════════════════════════════════════════════════════════════════════
async def setup(bot):
    """Charge le cog de démarrage"""
    await bot.add_cog(Demarrage(bot))


# ╔═══════════════════════════════════════════════════════════════════════════════
# ║  FIN DU FICHIER demarrage.py
# ╚═══════════════════════════════════════════════════════════════════════════════
