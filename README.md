# 🛡️ La Loyauté - Bot Discord

Bot Discord privé développé en Python avec discord.py, offrant des fonctionnalités de modération avancées et un système de logs complet.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-blue?logo=discord)
![Version](https://img.shields.io/badge/Version-0.2.1-green)
![Statut](https://img.shields.io/badge/Statut-En%20développement-yellow)

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Structure du projet](#-structure-du-projet)
- [Configuration](#️-configuration)
- [Utilisation](#-utilisation)
- [Commandes disponibles](#-commandes-disponibles)
- [Outils de développement](#-outils-de-développement)
- [Développement](#-développement)

---

## ✨ Fonctionnalités

### 🔧 Système de configuration (v0.2.1)
- ✅ Configuration dynamique par serveur
- ✅ Sauvegarde automatique en JSON
- ✅ Commandes `/config` complètes
- ✅ Création automatique de salon de logs

### 🛡️ Modération
- ✅ Kick, Ban, Unban
- ✅ Timeout (mute temporaire)
- ✅ Système d'avertissements (warns)
- ✅ Clear de messages
- ✅ Logs de toutes les actions

### 📊 Système de logs Discord
- ✅ 14 types de logs différents
- ✅ Logs de modération (kick, ban, warn, etc.)
- ✅ Logs de membres (arrivée, départ, rôles)
- ✅ Logs de messages (suppression, modification)
- ✅ Logs de salons (création, suppression)
- ✅ Configuration par serveur

### 🎉 Événements
- ✅ Arrivée/départ de membres
- ✅ Modification de rôles
- ✅ Messages supprimés/modifiés
- ✅ Création/suppression de salons

### 🛠️ Outils de développement (v0.2.1)
- ✅ Analyseur d'erreurs Pylance/Pylint
- ✅ Détecteur de doublons de code
- ✅ Rapports détaillés automatiques

---

## 📁 Structure du projet

```
la_loyaute/
│
├── 📦 commandes/ # Commandes du bot
│ ├── init.py
│ ├── commandes_base.py # Commandes basiques (ping, info, etc.)
│ ├── commandes_admin.py # Commandes de modération
│ └── commandes_configuration.py # Commandes /config (v0.2.1)
│
├── 🎉 evenements/ # Gestionnaires d'événements
│ ├── init.py
│ ├── demarrage.py # Événements de démarrage
│ ├── messages.py # Traitement des messages
│ ├── events_membres.py # Événements des membres
│ ├── events_messages.py # Logs de messages (v0.2.1)
│ └── events_salons.py # Logs de salons (v0.2.1)
│
├── 🤖 noyau/ # Noyau du bot
│ ├── init.py
│ ├── gestionnaire_bot.py # Classe principale du bot
│ ├── gestionnaire_permissions.py # Système de permissions
│ └── gestionnaire_configuration.py # Config dynamique (v0.2.1)
│
├── 🔧 utilitaires/ # Utilitaires
│ ├── init.py
│ ├── logger.py # Système de logs console
│ ├── helpers.py # Fonctions utilitaires
│ └── logs_discord.py # Logs Discord (v0.2.1)
│
├── 🛠️ outils_dev/ # Outils de développement (v0.2.1)
│ ├── init.py
│ ├── analyser_erreurs.py # Analyseur d'erreurs
│ ├── detecter_doublons.py # Détecteur de doublons
│ ├── README.md # Documentation des outils
│ └── rapports/ # Rapports générés (ignoré par Git)
│
├── 📝 Fichiers de configuration
│ ├── principal.py # Point d'entrée principal
│ ├── configuration.py # Configuration globale
│ ├── secrets.env # Variables secrètes (ignoré par Git)
│ └── configurations_serveurs.json # Config serveurs (v0.2.1, ignoré)
│
├── 📚 Documentation
│ ├── README.md # Ce fichier
│ ├── CHANGELOG.md # Historique des versions
│ ├── patchnotes.md # Notes de versions
│ └── FEUILLE_DE_ROUTE.md # Roadmap du projet
│
└── 🔧 Fichiers de projet
├── .gitignore
├── LICENSE
└── requirements.txt
```

---

## ⚙️ Configuration

### Fichier `secrets.env`

```env
# TOKEN DISCORD
DISCORD_TOKEN=votre_token_ici

# CONFIGURATION
NIVEAU_LOG=INFO

Obtenir un token Discord
Aller sur Discord Developer Portal

Créer une nouvelle application

Aller dans "Bot" → "Add Bot"

Copier le token

Activer les Privileged Gateway Intents :

Presence Intent

Server Members Intent

Message Content Intent

📖 Utilisation
Première utilisation
Inviter le bot sur votre serveur

Configurer les logs : /config logs-create

Le bot créera automatiquement un salon privé 📋-logs

Tester avec /ping

Configuration des logs

/config logs-set #mon-salon     → Définir un salon existant
/config logs-create             → Créer un salon automatiquement
/config logs-show               → Voir la configuration
/config logs-reset              → Désactiver les logs

📜 Commandes disponibles
Commandes basiques

| Commande            | Description                 |
| ------------------- | --------------------------- |
| /ping               | Vérifie la latence du bot   |
| /info               | Informations sur le bot     |
| /serveur            | Informations sur le serveur |
| /userinfo [@membre] | Informations sur un membre  |

Commandes de modération

| Commande                        | Description            | Permissions         |
| ------------------------------- | ---------------------- | ------------------- |
| /kick @membre [raison]          | Expulser un membre     | Exclure des membres |
| /ban @membre [raison]           | Bannir un membre       | Bannir des membres  |
| /unban ID [raison]              | Débannir un membre     | Bannir des membres  |
| /timeout @membre durée [raison] | Mute temporaire        | Timeout des membres |
| /warn @membre raison            | Avertir un membre      | Gérer les messages  |
| /warns @membre                  | Liste des warns        | Gérer les messages  |
| /clear nombre                   | Supprimer des messages | Gérer les messages  |

Commandes de configuration (v0.2.1)

| Commande                | Description              | Permissions    |
| ----------------------- | ------------------------ | -------------- |
| /config logs-set #salon | Définir le salon de logs | Administrateur |
| /config logs-create     | Créer un salon de logs   | Administrateur |
| /config logs-show       | Voir la configuration    | Administrateur |
| /config logs-reset      | Désactiver les logs      | Administrateur |

🛠️ Outils de développement
Analyseur d'erreurs
Détecte les erreurs Pylance/Pylint dans le code :

python outils_dev/analyser_erreurs.py

Génère un rapport dans outils_dev/rapports/

Détecteur de doublons
Détecte les doublons de code :

python outils_dev/detecter_doublons.py

Génère un rapport dans outils_dev/rapports/

👨‍💻 Développement
Architecture
Le bot utilise une architecture modulaire :

Commandes : Cogs Discord.py

Événements : Gestionnaires d'événements séparés

Noyau : Logique métier centrale

Utilitaires : Fonctions réutilisables

Ajouter une nouvelle commande
Créer un nouveau fichier dans commandes/

Créer une classe héritant de commands.Cog

Ajouter les commandes avec @app_commands.command()

Charger le cog dans principal.py

Ajouter un nouvel événement
Créer un nouveau fichier dans evenements/

Créer une classe héritant de commands.Cog

Utiliser @commands.Cog.listener()

Charger le cog dans principal.py

Standards de code
✅ Commentaires détaillés avec emojis

✅ Numérotation des fonctions

✅ Gestion des erreurs complète

✅ Type hints Pylance

✅ Documentation des modules

📊 Logs Discord
Le bot enregistre automatiquement :

🚫 Actions de modération

👥 Événements de membres

💬 Messages supprimés/modifiés

🏗️ Création/suppression de salons

🎭 Changements de rôles

🔒 Sécurité
✅ Token Discord dans .env (non versionné)

✅ Configuration serveurs non versionnée

✅ Vérification des permissions

✅ Validation des entrées utilisateur

✅ Logs de toutes les actions sensibles

📝 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

👤 Auteur
Latury

GitHub : @Latury

🆘 Support
Pour obtenir de l'aide ou signaler un bug :

Ouvrir une issue sur GitHub

Consulter la FEUILLE_DE_ROUTE.md

📌 Versions
Actuelle : 0.2.1 (05/01/2026)

Précédente : 0.2.0 (26/12/2025)

Initiale : 0.1.0 (25/12/2025)

Voir CHANGELOG.md pour l'historique complet.

Développé avec Python par Latury


***

## 🔍 **CORRECTIONS APPLIQUÉES :**

1. ✅ `__init__.py` avec underscores corrects
2. ✅ Fermeture des code blocks
3. ✅ "Obtenir un token Discord" en sous-section (###)
4. ✅ **AJOUT DU TABLEAU DES COMMANDES DE MODÉRATION** (kick, ban, timeout, warn, etc.)
5. ✅ Formatage Markdown corrigé partout
6. ✅ Structure cohérente
7. ✅ Liens internes fonctionnels

***



