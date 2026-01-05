# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ ⚙️ LA LOYAUTÉ - GESTIONNAIRE DE CONFIGURATION
# ║
# ║ Gestion de la configuration par serveur (salon de logs, etc.)
# ║ Développé par Latury
# ║ Version : 0.2.1
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import json
import os
from typing import Optional
import discord


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📁 CONSTANTES
# ║ Description : Chemins et valeurs par défaut
# ═══════════════════════════════════════════════════════════════════════════════

FICHIER_CONFIG = "donnees/config_serveurs.json"
DOSSIER_DONNEES = "donnees"


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📦 CLASSE PRINCIPALE
# ║ Description : Gestionnaire de configuration des serveurs
# ═══════════════════════════════════════════════════════════════════════════════

class GestionnaireConfiguration:
    """Gère la configuration des serveurs Discord"""

    def __init__(self, logger):
        """
        Initialise le gestionnaire de configuration

        Args:
            logger: Instance du logger pour les logs
        """
        self.logger = logger
        self.config = {}
        self._charger_configuration()


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 📂 FONCTION 01 – Chargement de la configuration
    # ║ Description : Charge la configuration depuis le fichier JSON
    # ═══════════════════════════════════════════════════════════════════════════

    def _charger_configuration(self):
        """Charge la configuration depuis le fichier JSON"""
        try:
            # ── 🔹 ÉTAPE 1 : Vérifier si le dossier existe
            if not os.path.exists(DOSSIER_DONNEES):
                os.makedirs(DOSSIER_DONNEES)
                self.logger.info(f"📁 Dossier '{DOSSIER_DONNEES}' créé")

            # ── 🔹 ÉTAPE 2 : Vérifier si le fichier existe
            if os.path.exists(FICHIER_CONFIG):
                with open(FICHIER_CONFIG, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.logger.info(f"✅ Configuration chargée : {len(self.config)} serveur(s)")
            else:
                # ── 🔹 ÉTAPE 3 : Créer un fichier vide si inexistant
                self.config = {}
                self._sauvegarder_configuration()
                self.logger.info(f"📝 Fichier de configuration créé : {FICHIER_CONFIG}")

        except Exception as e:
            self.logger.error(f"❌ Erreur lors du chargement de la configuration : {e}")
            self.config = {}


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 💾 FONCTION 02 – Sauvegarde de la configuration
    # ║ Description : Sauvegarde la configuration dans le fichier JSON
    # ═══════════════════════════════════════════════════════════════════════════

    def _sauvegarder_configuration(self):
        """Sauvegarde la configuration dans le fichier JSON"""
        try:
            with open(FICHIER_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.logger.debug(f"💾 Configuration sauvegardée")
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la sauvegarde de la configuration : {e}")


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🔍 FONCTION 03 – Obtenir l'ID du salon de logs
    # ║ Description : Récupère l'ID du salon de logs d'un serveur
    # ═══════════════════════════════════════════════════════════════════════════

    def obtenir_salon_logs(self, guild_id: int) -> Optional[int]:
        """
        Obtient l'ID du salon de logs configuré pour un serveur

        Args:
            guild_id: ID du serveur Discord

        Returns:
            ID du salon de logs ou None si non configuré
        """
        guild_id_str = str(guild_id)

        if guild_id_str in self.config:
            return self.config[guild_id_str].get("logs_channel_id")

        return None


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ ✏️ FONCTION 04 – Définir le salon de logs
    # ║ Description : Configure le salon de logs pour un serveur
    # ═══════════════════════════════════════════════════════════════════════════

    def definir_salon_logs(self, guild_id: int, channel_id: int) -> bool:
        """
        Définit le salon de logs pour un serveur

        Args:
            guild_id: ID du serveur Discord
            channel_id: ID du salon à utiliser pour les logs

        Returns:
            True si succès, False sinon
        """
        try:
            guild_id_str = str(guild_id)

            # ── 🔹 ÉTAPE 1 : Créer l'entrée du serveur si nécessaire
            if guild_id_str not in self.config:
                self.config[guild_id_str] = {}

            # ── 🔹 ÉTAPE 2 : Définir le salon de logs
            self.config[guild_id_str]["logs_channel_id"] = channel_id

            # ── 🔹 ÉTAPE 3 : Sauvegarder
            self._sauvegarder_configuration()

            self.logger.info(f"✅ Salon de logs défini : Serveur {guild_id} → Salon {channel_id}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la définition du salon de logs : {e}")
            return False


    # ═══════════════════════════════════════════════════════════════════════════
    # ║ 🗑️ FONCTION 05 – Réinitialiser le salon de logs
    # ║ Description : Supprime la configuration du salon de logs
    # ═══════════════════════════════════════════════════════════════════════════

    def reinitialiser_salon_logs(self, guild_id: int) -> bool:
        """
        Réinitialise (supprime) le salon de logs d'un serveur

        Args:
            guild_id: ID du serveur Discord

        Returns:
            True si succès, False sinon
        """
        try:
            guild_id_str = str(guild_id)

            # ── 🔹 ÉTAPE 1 : Vérifier si le serveur existe
            if guild_id_str in self.config:
                # ── 🔹 ÉTAPE 2 : Supprimer le salon de logs
                if "logs_channel_id" in self.config[guild_id_str]:
                    del self.config[guild_id_str]["logs_channel_id"]

                    # ── 🔹 ÉTAPE 3 : Supprimer le serveur si vide
                    if not self.config[guild_id_str]:
                        del self.config[guild_id_str]

                    # ── 🔹 ÉTAPE 4 : Sauvegarder
                    self._sauvegarder_configuration()

                    self.logger.info(f"✅ Salon de logs réinitialisé pour le serveur {guild_id}")
                    return True

            return False

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la réinitialisation du salon de logs : {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# FIN DU FICHIER gestionnaire_configuration.py
# ═══════════════════════════════════════════════════════════════════════════════
