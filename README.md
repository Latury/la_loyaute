<div align="center">

# 🛡️ La Loyauté

**Bot Discord privé développé en Python**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Statut](https://img.shields.io/badge/Statut-Opérationnel-brightgreen?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-0.1.0-blue?style=for-the-badge)

*Développé par Latury*

</div>

---

## 📖 À propos

**La Loyauté** est un bot Discord privé développé exclusivement en Python avec la bibliothèque discord.py. Conçu pour offrir une expérience personnalisée et professionnelle, ce bot intègre des commandes de base et des fonctionnalités d'administration avancées.

### ✨ Fonctionnalités principales

- 💬 **Commandes de base** : Système de commandes avec prefix `!` accessible à tous
- 👑 **Commandes administratives** : Slash commands avec prefix `/` réservées aux administrateurs
- 🛡️ **Gestion des permissions** : Système de vérification des rôles et des autorisations
- 📝 **Système de logs** : Enregistrement automatique de toutes les actions importantes
- 🎨 **Embeds personnalisés** : Messages formatés et professionnels
- 🔄 **Architecture modulaire** : Code organisé, maintenable et évolutif
- 📊 **Statistiques en temps réel** : Uptime, latence, commandes exécutées, RAM utilisée
- 🎯 **Cadre de démarrage professionnel** : Affichage détaillé des informations au lancement

---

## 📂 Structure du projet

```
la_loyaute/
│
├── principal.py # Point d'entrée du bot
├── configuration.py # Configuration centralisée
├── requirements.txt # Dépendances Python
├── secrets.env # Variables d'environnement (non versionné)
├── .gitignore # Fichiers ignorés par Git
├── LICENSE # Licence du projet
│
├── noyau/ # Cœur du bot
│ ├── init.py # Initialisation du module
│ ├── gestionnaire_bot.py # Classe principale LoyauteBot
│ └── gestionnaire_permissions.py # Gestion des permissions et rôles
│
├── commandes/ # Commandes Discord
│ ├── init.py # Initialisation du module
│ ├── commandes_base.py # Commandes publiques (prefix !)
│ └── commandes_admin.py # Commandes admin (prefix /)
│
├── evenements/ # Événements Discord
│ ├── init.py # Initialisation du module
│ ├── demarrage.py # Événement on_ready avec cadre ASCII
│ └── messages.py # Gestion des événements de messages
│
├── utilitaires/ # Outils et helpers
│ ├── init.py # Initialisation du module
│ ├── logger.py # Système de logs avec rotation
│ └── helpers.py # Fonctions utilitaires
│
├── donnees/ # Données persistantes
│ └── (fichiers JSON, bases de données)
│
├── logs/ # Fichiers de logs
│ └── (logs générés automatiquement)
│
└── Documentation/
├── README.md # Ce fichier
├── CHANGELOG.md # Historique des versions
├── patchnotes.md # Notes de mises à jour
└── FEUILLE_DE_ROUTE.md # Roadmap du projet
```


---

## 🚀 Utilisation

### Prérequis

- Python 3.11 ou supérieur
- Un compte Discord Developer avec un bot créé
- Token Discord du bot

### Installation

1. Clonez le dépôt (si vous y avez accès)
2. Installez les dépendances :

```
python principal.py
```

Le bot affichera un cadre de démarrage professionnel avec toutes les informations importantes.

### Commandes disponibles

#### 💬 Commandes de base (prefix `!`)

| Commande | Description |
|----------|-------------|
| `!aide` | Affiche la liste des commandes disponibles |
| `!info` | Informations détaillées sur le bot |
| `!ping` | Teste la latence du bot |
| `!stats` | Statistiques complètes (uptime, RAM, commandes) |
| `!serveur` | Informations sur le serveur Discord |
| `!utilisateur [@mention]` | Profil détaillé d'un utilisateur |

#### 👑 Commandes administratives (prefix `/`)

| Commande | Description | Permissions requises |
|----------|-------------|---------------------|
| `/clear [nombre]` | Supprime des messages (max 100) | Gérer les messages |
| `/logs [nombre]` | Affiche les logs récents du bot | Administrateur |
| `/config` | Affiche la configuration du bot | Administrateur |
| `/reload [extension]` | Recharge une extension | Administrateur |
| `/shutdown` | Arrête le bot proprement | Administrateur |

---

## ⚙️ Configuration

Le fichier `configuration.py` centralise tous les paramètres :

```
Prefix des commandes
PREFIX_BASE = "!" # Commandes publiques
PREFIX_ADMIN = "/" # Commandes administratives

Couleurs des embeds
COULEUR_PRINCIPALE = 0x5865F2 # Bleu Discord
COULEUR_SUCCES = 0x57F287 # Vert
COULEUR_ERREUR = 0xED4245 # Rouge

IDs des rôles (à configurer dans secrets.env)
ROLE_ADMIN_ID = 123456789012345678
ROLE_MODERATEUR_ID = 123456789012345678
```


### Variables d'environnement (secrets.env)

```
DISCORD_TOKEN=votre_token_ici
GUILD_ID=votre_serveur_id
ROLE_ADMIN_ID=0
ROLE_MODERATEUR_ID=0
PREFIX_BASE=!
DEBUG_MODE=True
LOG_LEVEL=INFO
```


---

## 🛠️ Technologies utilisées

- **Python 3.11+** - Langage de programmation
- **discord.py 2.3+** - Bibliothèque Discord officielle
- **python-dotenv** - Gestion des variables d'environnement
- **psutil** - Statistiques système (RAM, CPU)
- **asyncio** - Programmation asynchrone

---

## 📝 Logs

Le bot génère automatiquement des fichiers de logs dans le dossier `logs/` :
- Horodatage précis (jour/mois/année heure:minutes:secondes)
- Actions importantes (démarrage, erreurs, commandes)
- Un fichier par jour avec rotation automatique
- Logs colorés dans la console pour meilleure lisibilité

Exemple de nom de fichier : `la_loyaute_24-12-2025.log`

---

## 🏗️ Architecture

### Séparation des responsabilités

- **noyau/** : Logique métier du bot (classe principale, permissions)
- **commandes/** : Commandes Discord organisées par niveau d'accès
- **evenements/** : Gestion des événements Discord (messages, démarrage)
- **utilitaires/** : Fonctions réutilisables (logs, helpers, formatage)

### Patterns utilisés

- **Cogs** : Organisation modulaire des commandes et événements
- **Decorateurs** : Vérification des permissions avant exécution
- **Async/Await** : Programmation asynchrone pour performances optimales
- **Singleton** : Configuration centralisée accessible partout

---

## 🔒 Sécurité

- ✅ Token Discord stocké dans `secrets.env` (non versionné)
- ✅ Système de permissions robuste pour les commandes admin
- ✅ Validation des entrées utilisateur
- ✅ Logs de sécurité pour toutes les actions sensibles
- ✅ Gestion des erreurs avec messages explicites

---

## 📊 Statistiques

Le bot collecte et affiche :
- Nombre de serveurs connectés
- Nombre d'utilisateurs accessibles
- Nombre de commandes chargées
- Latence en temps réel
- Uptime (temps de fonctionnement)
- RAM utilisée
- Commandes exécutées avec succès
- Taux d'erreur

---

## 📜 Versioning

Ce projet suit le versioning sémantique (SemVer) :
- **MAJOR** : Changements incompatibles avec versions antérieures
- **MINOR** : Nouvelles fonctionnalités compatibles
- **PATCH** : Corrections de bugs

Version actuelle : **v0.1.0** (Première version opérationnelle)

---

## 🗺️ Roadmap

Consultez [FEUILLE_DE_ROUTE.md](FEUILLE_DE_ROUTE.md) pour voir les fonctionnalités prévues.

---

## 📄 Licence

Ce projet est un bot privé développé par Latury.
Tous droits réservés © 2025

---

## 👤 Auteur

**Latury**
- GitHub : [@Latury](https://github.com/Latury)
- Projet : Bot Discord privé "La Loyauté"

---

<div align="center">

**Développé avec par Latury en Python**

*La Loyauté - Votre compagnon Discord de confiance*

Version 0.1.0 | Mise à jour : 24/12/2025

</div>


