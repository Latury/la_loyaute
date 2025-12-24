# ═══════════════════════════════════════════════════════════════════════════════
# ║                                                                             
# ║  📝 LA LOYAUTÉ - SYSTÈME DE LOGS
# ║
# ║  Gestionnaire de logs professionnel avec fichiers datés
# ║  Développé par Latury
# ║  Version : 0.1.0
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Importation de la configuration
import configuration as config

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📁 Fonction 01 – Création du dossier de logs
# ║ Description : Crée le dossier logs s'il n'existe pas
# ╚══════════════════════════════════════════════════════════════════════════════
def creer_dossier_logs():
    """Crée le dossier de logs s'il n'existe pas"""

    if not os.path.exists(config.DOSSIER_LOGS):
        os.makedirs(config.DOSSIER_LOGS)
        print(f"📁 Dossier '{config.DOSSIER_LOGS}' créé")

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🎨 Fonction 02 – Formateur coloré pour console
# ║ Description : Ajoute des couleurs aux logs de la console
# ╚══════════════════════════════════════════════════════════════════════════════
class FormateurCouleur(logging.Formatter):
    """Formateur de logs avec couleurs pour la console"""

    # Codes de couleurs ANSI
    GRIS = '\033[90m'
    BLEU = '\033[94m'
    VERT = '\033[92m'
    JAUNE = '\033[93m'
    ROUGE = '\033[91m'
    ROUGE_GRAS = '\033[1;91m'
    RESET = '\033[0m'

    # Association couleurs/niveaux
    COULEURS = {
        logging.DEBUG: GRIS,
        logging.INFO: BLEU,
        logging.WARNING: JAUNE,
        logging.ERROR: ROUGE,
        logging.CRITICAL: ROUGE_GRAS
    }

    def format(self, record):
        """Formate le message de log avec la couleur appropriée"""

        # ── 🔹 Récupération de la couleur
        couleur = self.COULEURS.get(record.levelno, self.RESET)

        # ── 🔹 Formatage du message
        record.levelname = f"{couleur}{record.levelname}{self.RESET}"

        return super().format(record)

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📝 Fonction 03 – Création du logger
# ║ Description : Crée et configure un logger avec fichier et console
# ╚══════════════════════════════════════════════════════════════════════════════
def creer_logger(nom: str, niveau: str = 'INFO') -> logging.Logger:
    """
    Crée un logger personnalisé pour le bot

    Args:
        nom: Nom du logger
        niveau: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        logging.Logger: Le logger configuré
    """

    # ── 🔹 Création du dossier de logs
    creer_dossier_logs()

    # ── 🔹 Création du logger
    logger = logging.getLogger(nom)
    logger.setLevel(getattr(logging, niveau.upper(), logging.INFO))

    # ── 🔹 Vérification si le logger a déjà des handlers (évite les duplications)
    if logger.handlers:
        return logger

    # ── 🔹 Création du nom de fichier avec date
    date_actuelle = datetime.now().strftime('%d-%m-%Y')
    nom_fichier = os.path.join(config.DOSSIER_LOGS, f"la_loyaute_{date_actuelle}.log")

    # ── 🔹 Handler pour fichier (avec rotation)
    handler_fichier = RotatingFileHandler(
        nom_fichier,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    handler_fichier.setLevel(logging.DEBUG)

    # ── 🔹 Formateur pour fichier
    formateur_fichier = logging.Formatter(
        config.FORMAT_LOG,
        datefmt=config.FORMAT_DATE_LOG
    )
    handler_fichier.setFormatter(formateur_fichier)

    # ── 🔹 Handler pour console avec couleurs
    handler_console = logging.StreamHandler()
    handler_console.setLevel(getattr(logging, niveau.upper(), logging.INFO))

    # ── 🔹 Formateur coloré pour console
    formateur_console = FormateurCouleur(
        config.FORMAT_LOG,
        datefmt=config.FORMAT_DATE_LOG
    )
    handler_console.setFormatter(formateur_console)

    # ── 🔹 Ajout des handlers au logger
    logger.addHandler(handler_fichier)
    logger.addHandler(handler_console)

    return logger

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 🗑️ Fonction 04 – Nettoyage des anciens logs
# ║ Description : Supprime les fichiers de logs trop anciens
# ╚══════════════════════════════════════════════════════════════════════════════
def nettoyer_anciens_logs(jours: int = 30):
    """
    Supprime les fichiers de logs plus anciens que X jours

    Args:
        jours: Nombre de jours de rétention
    """

    if not os.path.exists(config.DOSSIER_LOGS):
        return

    maintenant = datetime.now()
    fichiers_supprimes = 0

    # ── 🔹 Parcours des fichiers de logs
    for fichier in os.listdir(config.DOSSIER_LOGS):
        chemin_fichier = os.path.join(config.DOSSIER_LOGS, fichier)

        # ── 🔹 Vérification si c'est un fichier .log
        if os.path.isfile(chemin_fichier) and fichier.endswith('.log'):
            # ── 🔹 Récupération de la date de modification
            temps_modification = datetime.fromtimestamp(os.path.getmtime(chemin_fichier))
            age = (maintenant - temps_modification).days

            # ── 🔹 Suppression si trop ancien
            if age > jours:
                try:
                    os.remove(chemin_fichier)
                    fichiers_supprimes += 1
                except Exception as e:
                    print(f"⚠️ Erreur lors de la suppression de {fichier} : {e}")

    if fichiers_supprimes > 0:
        print(f"🗑️ {fichiers_supprimes} ancien(s) fichier(s) de logs supprimé(s)")

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📊 Fonction 05 – Statistiques des logs
# ║ Description : Retourne des statistiques sur les fichiers de logs
# ╚══════════════════════════════════════════════════════════════════════════════
def obtenir_stats_logs() -> dict:
    """Retourne des statistiques sur les fichiers de logs"""

    if not os.path.exists(config.DOSSIER_LOGS):
        return {
            'nombre_fichiers': 0,
            'taille_totale': 0,
            'fichier_actuel': 'Aucun'
        }

    # ── 🔹 Comptage des fichiers et taille
    fichiers = [f for f in os.listdir(config.DOSSIER_LOGS) if f.endswith('.log')]
    nombre_fichiers = len(fichiers)

    taille_totale = 0
    for fichier in fichiers:
        chemin = os.path.join(config.DOSSIER_LOGS, fichier)
        taille_totale += os.path.getsize(chemin)

    # ── 🔹 Conversion en MB
    taille_mb = round(taille_totale / (1024 * 1024), 2)

    # ── 🔹 Fichier actuel
    date_actuelle = datetime.now().strftime('%d-%m-%Y')
    fichier_actuel = f"la_loyaute_{date_actuelle}.log"

    return {
        'nombre_fichiers': nombre_fichiers,
        'taille_totale': taille_mb,
        'fichier_actuel': fichier_actuel
    }

# ╔══════════════════════════════════════════════════════════════════════════════
# ║ 📋 Fonction 06 – Lire les dernières lignes d'un log
# ║ Description : Lit les N dernières lignes d'un fichier de log
# ╚══════════════════════════════════════════════════════════════════════════════
def lire_dernieres_lignes(nombre_lignes: int = 50) -> list:
    """
    Lit les dernières lignes du fichier de log actuel

    Args:
        nombre_lignes: Nombre de lignes à lire

    Returns:
        list: Liste des dernières lignes
    """

    # ── 🔹 Détermination du fichier actuel
    date_actuelle = datetime.now().strftime('%d-%m-%Y')
    fichier_log = os.path.join(config.DOSSIER_LOGS, f"la_loyaute_{date_actuelle}.log")

    if not os.path.exists(fichier_log):
        return []

    # ── 🔹 Lecture des dernières lignes
    try:
        with open(fichier_log, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
            return lignes[-nombre_lignes:] if len(lignes) > nombre_lignes else lignes
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du log : {e}")
        return []
