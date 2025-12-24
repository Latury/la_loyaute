# 📋 Changelog

Tous les changements notables de **La Loyauté** seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

---

## [Non publié]

### À venir
- Système de modération automatique
- Commandes de musique
- Intégration d'API externes
- Base de données pour la persistance

---

## [0.1.0] - 24/12/2025

### 🎉 Première version

#### Ajouté
- Architecture complète du projet
- Structure modulaire avec séparation des responsabilités
- Fichier `principal.py` comme point d'entrée
- Gestionnaire de bot dans `noyau/gestionnaire_bot.py`
- Gestionnaire de permissions dans `noyau/gestionnaire_permissions.py`
- Système de commandes de base (prefix `!`)
- Système de commandes admin (prefix `/`)
- Événement de démarrage avec cadre professionnel
- Système de logs automatique avec horodatage
- Fonctions utilitaires dans `helpers.py`
- Configuration centralisée dans `configuration.py`
- Documentation complète (README, CHANGELOG, patchnotes)
- Fichier `.gitignore` configuré pour Python
- Template `secrets.env` pour les variables sensibles
- Fichier `requirements.txt` avec toutes les dépendances

#### Sécurité
- Token Discord stocké dans variables d'environnement
- Système de vérification des permissions pour commandes admin
- Validation des rôles avant exécution des commandes sensibles

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

*Dernière mise à jour : 24/12/2025 02:06:00*
