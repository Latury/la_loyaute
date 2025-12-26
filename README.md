<div align="center">

# 🛡️ La Loyauté

**Bot Discord privé développé en Python**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Statut](https://img.shields.io/badge/Statut-Opérationnel-brightgreen?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-0.2.0-blue?style=for-the-badge)

*Développé par Latury*

</div>

---

## 📖 À propos

**La Loyauté** est un bot Discord privé développé exclusivement en Python avec la bibliothèque discord.py. Conçu pour offrir une expérience personnalisée et professionnelle, ce bot intègre des commandes de base, des fonctionnalités d'administration avancées et un système de logs Discord automatiques.

### ✨ Fonctionnalités principales

- 💬 **Commandes de base** : Système de commandes avec prefix `!` accessible à tous
- 👑 **Commandes administratives** : Slash commands avec prefix `/` réservées aux administrateurs
- 🛡️ **Modération avancée** : Kick, ban, timeout, warns avec historique
- 📊 **Logs Discord automatiques** : Toutes les actions enregistrées dans un salon dédié
- 👥 **Événements de membres** : Logs d'arrivées et de départs automatiques
- 🔒 **Gestion des permissions** : Système de vérification des rôles et des autorisations
- 📝 **Système de logs fichier** : Enregistrement automatique avec rotation quotidienne
- 🎨 **Embeds personnalisés** : Messages formatés et professionnels
- 🔄 **Architecture modulaire** : Code organisé, maintenable et évolutif
- 📈 **Statistiques en temps réel** : Uptime, latence, commandes exécutées, RAM utilisée
- 🎯 **Cadre de démarrage professionnel** : Affichage détaillé des informations au lancement
- 🔧 **Outils de maintenance** : Script de vérification de doublons

---

## 📂 Structure du projet

```
la_loyaute/
│
├── principal.py # Point d'entrée du bot
├── configuration.py # Configuration centralisée
├── requirements.txt # Dépendances Python
├── secrets.env # Variables d'environnement (non versionné)
├── verifier_doublons.py # Script de vérification du code
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
│ ├── messages.py # Gestion des événements de messages
│ └── events_membres.py # Événements d'arrivée/départ de membres
│
├── utilitaires/ # Outils et helpers
│ ├── init.py # Initialisation du module
│ ├── logger.py # Système de logs fichier avec rotation
│ ├── helpers.py # Fonctions utilitaires
│ └── logs_discord.py # Système de logs Discord automatiques
│
├── donnees/ # Données persistantes
│ ├── warns.json # Stockage des avertissements
│ └── (autres fichiers de données)
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
pip install -r requirements.txt
```


3. Configurez le fichier `secrets.env` avec vos identifiants

4. Lancez le bot :

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
| `/kick @membre [raison]` | Expulse un membre du serveur | Expulser des membres |
| `/ban @membre [raison]` | Bannit un membre du serveur | Bannir des membres |
| `/unban user_id [raison]` | Débannit un utilisateur par ID | Bannir des membres |
| `/timeout @membre [durée] [raison]` | Met un membre en timeout | Modérer les membres |
| `/warn @membre [raison]` | Avertit un membre (stocké) | Modérer les membres |
| `/warnings @membre` | Consulte les warns d'un membre | Modérer les membres |
| `/removewarn @membre [index]` | Supprime un warn spécifique | Modérer les membres |
| `/clearwarns @membre` | Efface tous les warns d'un membre | Modérer les membres |
| `/setlogs [#salon]` | Configure le salon de logs Discord | Administrateur |

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

Logs Discord
LOGS_CHANNEL_ID = 0 # ID du salon de logs (0 = désactivé)

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


### Configuration du salon de logs Discord

Pour activer les logs Discord :

1. Créez un salon privé (ex: `#logs-moderation`)
2. Utilisez la commande `/setlogs #logs-moderation`
3. Le bot enverra un message de confirmation
4. Toutes les actions seront loggées automatiquement

Pour désactiver les logs :

```
/setlogs
```


---

## 🛠️ Technologies utilisées

- **Python 3.11+** - Langage de programmation
- **discord.py 2.3+** - Bibliothèque Discord officielle
- **python-dotenv** - Gestion des variables d'environnement
- **psutil** - Statistiques système (RAM, CPU)
- **asyncio** - Programmation asynchrone

---

## 📊 Système de logs

### Logs fichier (console + fichiers)

Le bot génère automatiquement des fichiers de logs dans le dossier `logs/` :
- Horodatage précis (jour/mois/année heure:minutes:secondes)
- Actions importantes (démarrage, erreurs, commandes)
- Un fichier par jour avec rotation automatique
- Logs colorés dans la console pour meilleure lisibilité

Exemple de nom de fichier : `la_loyaute_26-12-2025.log`

### Logs Discord (nouveau en v0.2.0)

Le bot peut enregistrer automatiquement dans un salon Discord :
- ✅ Expulsions (kick)
- ✅ Bannissements (ban)
- ✅ Débannissements (unban)
- ✅ Timeouts
- ✅ Avertissements (warns)
- ✅ Suppressions de messages en masse
- ✅ Arrivées de membres
- ✅ Départs de membres

Tous les logs sont affichés avec des embeds colorés contenant :
- Informations complètes (membre, modérateur, raison)
- Horodatage automatique Discord
- Couleurs contextuelles (rouge = ban, vert = unban, etc.)
- IDs Discord pour traçabilité

---

## 🛡️ Système de modération

### Avertissements (Warns)

Le bot dispose d'un système d'avertissements complet :
- Stockage permanent dans `donnees/warns.json`
- Historique par membre avec date, modérateur, et raison
- Commandes de gestion : `/warn`, `/warnings`, `/removewarn`, `/clearwarns`
- Compteur d'avertissements affiché
- Logs automatiques dans Discord

### Actions de modération

Toutes les actions de modération sont :
- ✅ Vérifiées pour permissions appropriées
- ✅ Loggées dans Discord (si configuré)
- ✅ Loggées dans les fichiers
- ✅ Protégées contre l'auto-modération
- ✅ Validées avant exécution

---

## 🏗️ Architecture

### Séparation des responsabilités

- **noyau/** : Logique métier du bot (classe principale, permissions)
- **commandes/** : Commandes Discord organisées par niveau d'accès
- **evenements/** : Gestion des événements Discord (messages, membres, démarrage)
- **utilitaires/** : Fonctions réutilisables (logs, helpers, formatage)
- **donnees/** : Stockage persistant (JSON, bases de données)

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
- ✅ Vérification des hiérarchies de rôles avant modération
- ✅ Protection contre l'auto-modération (kick/ban soi-même)

---

## 🔧 Outils de maintenance

### Script de vérification des doublons

Le projet inclut un script `verifier_doublons.py` pour maintenir la qualité du code :

```
python verifier_doublons.py`
```


**Fonctionnalités :**
- Détecte les fichiers avec le même nom
- Détecte les fichiers avec contenu identique (hash MD5)
- Détecte les fichiers temporaires et backups
- Détecte les fonctions/classes dupliquées
- Génère un rapport sur le Bureau
- Ignore automatiquement `.venv`, `__pycache__`, etc.

**Utilisation recommandée :**
- Avant chaque commit Git
- Après ajout de nouveaux fichiers
- Lors de refactoring important

---

## 📈 Statistiques

Le bot collecte et affiche :
- Nombre de serveurs connectés
- Nombre d'utilisateurs accessibles
- Nombre de commandes chargées
- Latence en temps réel
- Uptime (temps de fonctionnement)
- RAM utilisée
- Commandes exécutées avec succès
- Taux d'erreur
- Statistiques des messages (traités, supprimés, modifiés)

---

## 📜 Versioning

Ce projet suit le versioning sémantique (SemVer) :
- **MAJOR** : Changements incompatibles avec versions antérieures
- **MINOR** : Nouvelles fonctionnalités compatibles
- **PATCH** : Corrections de bugs

Version actuelle : **v0.2.0** (Système de logs Discord et modération)

### Historique des versions

- **v0.2.0** (26/12/2025) : Logs Discord, modération avancée, warns, événements de membres
- **v0.1.0** (24/12/2025) : Première version opérationnelle avec commandes de base

---

## 🗺️ Roadmap

Consultez [FEUILLE_DE_ROUTE.md](FEUILLE_DE_ROUTE.md) pour voir les fonctionnalités prévues.

### Prochaines versions

- **v0.2.1** : Logs avancés (messages, rôles, salons)
- **v0.2.2** : Messages de bienvenue personnalisables
- **v0.3.0** : Améliorations UX (help, userinfo, serverinfo)
- **v0.4.0** : Auto-modération (spam, filtres, anti-raid)
- **v0.5.0** : Système de tickets
- **v0.6.0** : Niveaux et XP
- **v1.0.0** : Release finale

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

## 📞 Support et Documentation

- **Documentation complète** : Consultez les fichiers dans `/Documentation/`
- **Changelog** : [CHANGELOG.md](CHANGELOG.md) pour l'historique détaillé
- **Notes de mise à jour** : [patchnotes.md](patchnotes.md) pour les nouveautés
- **Roadmap** : [FEUILLE_DE_ROUTE.md](FEUILLE_DE_ROUTE.md) pour les plans futurs

---

<div align="center">

**Développé avec par Latury en Python**

*La Loyauté - Votre compagnon Discord de confiance*

Version 0.2.0 | Mise à jour : 26/12/2025

</div>
