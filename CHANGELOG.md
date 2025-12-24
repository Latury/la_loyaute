# 📋 Changelog

Tous les changements notables de **La Loyauté** seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

---

## [Non publié]

### À venir
- Système de modération automatique avec filtres personnalisables
- Commandes de musique avec lecteur audio intégré
- Intégration d'API externes (météo, traduction, etc.)
- Base de données SQLite pour persistance des données
- Système de niveaux et expérience pour les utilisateurs
- Dashboard web pour configuration à distance

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

*Dernière mise à jour : 24/12/2025 07:40:00*
