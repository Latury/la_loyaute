# 📋 Changelog

Tous les changements notables de **La Loyauté** seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

---

## [Non publié]

### À venir
- Logs avancés (messages supprimés/modifiés, rôles, salons)
- Messages de bienvenue et d'au revoir personnalisables
- Commande `/help` interactive avec pagination
- Système d'auto-modération (spam, filtre de mots)
- Système de tickets pour support
- Système de niveaux et XP

---

## [0.2.0] - 26/12/2025

### 🎉 Système de logs Discord et modération avancée

#### Ajouté - Système de logs Discord
- Nouveau fichier `utilitaires/logs_discord.py` avec fonctions de logs automatiques
- Logs visuels dans Discord avec embeds colorés et détaillés
- Fonction `log_kick()` : Log d'expulsion de membre
- Fonction `log_ban()` : Log de bannissement avec raison
- Fonction `log_unban()` : Log de débannissement
- Fonction `log_timeout()` : Log de mise en timeout avec durée
- Fonction `log_warn()` : Log d'avertissement avec compteur
- Fonction `log_clear()` : Log de suppression de messages en masse
- Fonction `log_member_join()` : Log d'arrivée de membre (âge du compte, total membres)
- Fonction `log_member_leave()` : Log de départ de membre (temps passé sur serveur)
- Variable `LOGS_CHANNEL_ID` dans `configuration.py` pour salon de logs

#### Ajouté - Commandes de modération (prefix /)
- `/kick @membre [raison]` : Expulse un membre du serveur
- `/ban @membre [raison]` : Bannit un membre du serveur
- `/unban user_id [raison]` : Débannit un utilisateur par son ID
- `/timeout @membre [durée] [raison]` : Met un membre en timeout temporaire
- `/warn @membre [raison]` : Avertit un membre (stockage dans JSON)
- `/warnings @membre` : Consulte les warns d'un membre
- `/removewarn @membre [index]` : Supprime un warn spécifique
- `/clearwarns @membre` : Efface tous les warns d'un membre
- `/setlogs #salon` : Configure le salon de logs Discord
- `/setlogs` (sans paramètre) : Désactive les logs Discord

#### Ajouté - Événements de membres
- Nouveau fichier `evenements/events_membres.py` pour gérer les membres
- Événement `on_member_join` : Détecte l'arrivée d'un membre
- Événement `on_member_remove` : Détecte le départ d'un membre
- Logs automatiques dans Discord pour arrivées/départs
- Extension `evenements.events_membres` ajoutée au chargement dans `principal.py`

#### Ajouté - Système de warns
- Stockage des warns dans `donnees/warns.json`
- Compteur d'avertissements par utilisateur et par serveur
- Historique complet (modérateur, raison, date)
- Commandes de gestion complètes (ajout, consultation, suppression)
- Affichage formaté avec embeds Discord

#### Ajouté - Outils de développement
- Script `verifier_doublons.py` à la racine du projet
- Détection automatique de fichiers en double (même nom)
- Détection de fichiers avec contenu identique (hash MD5)
- Détection de fichiers temporaires et backups
- Détection de fonctions/classes dupliquées
- Rapport généré sur le Bureau en `.txt`
- Exclusion automatique de `.venv` et autres dossiers
- Script ajouté au `.gitignore`

#### Modifié - Configuration
- Ajout de `LOGS_CHANNEL_ID` dans `configuration.py`
- Documentation sur comment obtenir l'ID d'un salon Discord
- Valeur par défaut à 0 (logs désactivés)
- Variable modifiable via `/setlogs` ou fichier de config

#### Modifié - Architecture
- Extension de `commandes_admin.py` avec 9 nouvelles commandes
- Import des fonctions de logs dans les commandes de modération
- Appels automatiques des logs après chaque action de modération
- Amélioration de la gestion des erreurs avec messages explicites

#### Modifié - Documentation
- Mise à jour de la structure du projet dans README.md
- Ajout de `events_membres.py` dans l'arborescence
- Ajout de `logs_discord.py` dans l'arborescence
- Ajout du dossier `donnees/` pour stockage JSON
- Mise à jour du tableau des commandes administratives
- Documentation des nouvelles fonctionnalités de logs

#### Technique
- Utilisation de `discord.Embed` pour logs visuels
- Gestion asynchrone des appels de logs
- Vérification de l'existence du salon de logs
- Gestion des erreurs si salon inexistant ou supprimé
- Formatage des durées (secondes → jours/heures/minutes)
- Calcul de l'âge des comptes utilisateurs
- Stockage JSON avec lecture/écriture sécurisée
- Script d'analyse utilisant hashlib pour détection doublons

#### Sécurité
- Vérification des permissions avant actions de modération
- Impossibilité de kick/ban soi-même ou le bot
- Impossibilité de modérer un membre avec rôle supérieur
- Logs de toutes les actions de modération
- Stockage sécurisé des warns avec horodatage

#### Tests
- Toutes les commandes de modération testées et fonctionnelles
- Système de logs Discord vérifié et opérationnel
- Événements de membres validés (arrivée/départ)
- Système de warns testé (ajout, consultation, suppression)
- Script de vérification de doublons exécuté avec succès
- Aucun doublon critique détecté dans le projet
- Configuration du salon de logs validée

---

## [0.1.0] - 24/12/2025

### 🎉 Première version opérationnelle

#### Ajouté - Infrastructure
- Architecture complète du projet avec séparation modulaire
- Fichier `principal.py` comme point d'entrée avec boucle asynchrone
- Gestionnaire de bot dans `noyau/gestionnaire_bot.py` avec classe LoyauteBot
- Gestionnaire de permissions dans `noyau/gestionnaire_permissions.py`
- Système de logs automatique avec rotation dans `utilitaires/logger.py`
- Fonctions utilitaires réutilisables dans `utilitaires/helpers.py`
- Configuration centralisée dans `configuration.py` avec support .env

#### Ajouté - Commandes de base (prefix !)
- `!aide` : Affiche la liste complète des commandes avec descriptions
- `!info` : Informations détaillées sur le bot (version, stats, technologies)
- `!ping` : Test de latence avec indicateur de qualité (vert/jaune/rouge)
- `!stats` : Statistiques complètes (uptime, RAM, commandes, messages)
- `!serveur` : Informations sur le serveur Discord (membres, rôles, boosts)
- `!utilisateur` : Profil détaillé d'un utilisateur (rôles, dates, permissions)

#### Ajouté - Commandes administratives (prefix /)
- `/clear [nombre]` : Suppression en masse de messages (1-100)
- `/logs [nombre]` : Consultation des logs récents (1-50 lignes)
- `/config` : Affichage de la configuration actuelle du bot
- `/reload [extension]` : Rechargement d'une extension sans redémarrage
- `/shutdown` : Arrêt propre du bot avec confirmation

#### Ajouté - Événements Discord
- `on_ready` : Cadre de démarrage ASCII professionnel avec statistiques
- `on_message` : Traitement des messages avec compteur et logs debug
- `on_message_delete` : Tracking des suppressions de messages
- `on_message_edit` : Suivi des modifications de messages
- `on_raw_bulk_message_delete` : Gestion des suppressions en masse
- Gestion des messages privés avec réponse automatique

#### Ajouté - Système de permissions
- Vérification par rôle (Admin, Modérateur)
- Vérification par ID développeur
- Décorateurs personnalisés (@require_admin, @require_moderator)
- Fonction `obtenir_niveau_permission()` pour affichage du statut
- Support du propriétaire de serveur avec permissions spéciales

#### Ajouté - Système de logs
- Logs colorés dans la console (gris/bleu/jaune/rouge selon niveau)
- Fichiers de logs avec rotation (1 fichier par jour)
- Horodatage précis (jour/mois/année heure:minutes:secondes)
- Niveaux de logs configurables (DEBUG, INFO, WARNING, ERROR)
- Fonction de nettoyage automatique des anciens logs (30 jours)
- Statistiques des logs (nombre de fichiers, taille totale)

#### Ajouté - Fonctionnalités utilitaires
- Création d'embeds personnalisés avec footer et timestamp
- Embeds prédéfinis (succès, erreur, avertissement, info)
- Formatage des dates au format français (jour/mois/année)
- Formatage des durées lisibles (jours, heures, minutes)
- Formatage des nombres avec séparateurs (1 234 567)
- Barres de progression visuelles pour statistiques
- Validation d'URLs
- Troncature de textes avec ellipse
- Obtention du nom d'affichage (pseudo ou nom d'utilisateur)

#### Ajouté - Documentation
- README.md complet avec badges, structure, et exemples
- CHANGELOG.md pour suivi des versions
- patchnotes.md pour notes utilisateur
- FEUILLE_DE_ROUTE.md pour planification future
- Fichier .gitignore configuré pour Python et secrets
- Template secrets.env avec variables requises
- Commentaires détaillés dans tout le code

#### Modifié - Corrections
- Cadre de démarrage sans emojis pour alignement parfait (80 caractères)
- Suppression de `process_commands()` dans `on_message` pour éviter duplication
- Gestion correcte des valeurs vides dans secrets.env
- Textes sans accents dans le cadre ASCII pour éviter problèmes d'alignement

#### Technique
- Code 100% en français (noms, commentaires, documentation)
- Architecture modulaire avec cogs Discord
- Programmation asynchrone avec asyncio
- Utilisation de discord.py 2.3+ avec intents
- Support des slash commands
- Gestion des erreurs robuste avec traceback
- Cache et optimisations pour réduire appels API
- Fonctions numérotées avec cadres de commentaires professionnels

#### Sécurité
- Token Discord stocké dans variables d'environnement
- Système de vérification des permissions avant exécution
- Validation des rôles pour commandes admin
- Logs de sécurité pour actions sensibles
- Gestion des erreurs sans exposition d'informations sensibles

#### Tests
- Bot testé et opérationnel sur serveur Discord
- Toutes les commandes de base fonctionnelles
- Toutes les commandes admin vérifiées
- Connexion Discord stable avec reconnexion automatique
- Logs générés correctement avec rotation
- Embeds personnalisés fonctionnels
- Système de permissions validé

---

## Format des versions

### Types de changements
- **Ajouté** : Nouvelles fonctionnalités
- **Modifié** : Changements dans les fonctionnalités existantes
- **Déprécié** : Fonctionnalités bientôt supprimées
- **Supprimé** : Fonctionnalités retirées
- **Corrigé** : Corrections de bugs
- **Sécurité** : Corrections de vulnérabilités

---

*Dernière mise à jour : 26/12/2025 02:20:00*
