<div align="center">

# 🛡️ La Loyauté

**Bot Discord privé développé en Python**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Statut](https://img.shields.io/badge/Statut-En_Développement-yellow?style=for-the-badge)
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

---

## 📂 Structure du projet

```
la_loyaute/
│
├── principal.py # Point d'entrée du bot
├── configuration.py # Configuration centralisée
├── requirements.txt # Dépendances Python
├── secrets.env # Variables d'environnement (non versionné)
│
├── noyau/ # Cœur du bot
│ ├── init.py
│ ├── gestionnaire_bot.py # Classe principale du bot
│ └── gestionnaire_permissions.py # Gestion des permissions
│
├── commandes/ # Commandes Discord
│ ├── init.py
│ ├── commandes_base.py # Commandes publiques (prefix !)
│ └── commandes_admin.py # Commandes admin (prefix /)
│
├── evenements/ # Événements Discord
│ ├── init.py
│ ├── demarrage.py # Événement on_ready
│ └── messages.py # Événements de messages
│
├── utilitaires/ # Outils et helpers
│ ├── init.py
│ ├── logger.py # Système de logs
│ └── helpers.py # Fonctions utilitaires
│
├── donnees/ # Données persistantes
│ └── (fichiers JSON, bases de données)
│
├── logs/ # Fichiers de logs
│ └── (logs générés automatiquement)
│
└── docs/ # Documentation
├── README.md # Ce fichier
├── CHANGELOG.md # Historique des versions
├── patchnotes.md # Notes de mises à jour
└── FEUILLE_DE_ROUTE.md # Roadmap du projet
```


---

## 🚀 Utilisation

### Démarrage du bot

1. Configurez le fichier `secrets.env` avec votre token Discord
2. Lancez le bot avec la commande :

```
python principal.py
```


### Commandes disponibles

#### 💬 Commandes de base (prefix `!`)
- `!aide` - Affiche la liste des commandes disponibles
- `!info` - Affiche les informations sur le bot
- `!ping` - Vérifie la latence du bot

#### 👑 Commandes administratives (prefix `/`)
- `/clear` - Supprime des messages
- `/config` - Configure les paramètres du serveur
- `/logs` - Consulte les logs du bot

---

## ⚙️ Configuration

Le fichier `configuration.py` centralise tous les paramètres :

```
Prefix des commandes
PREFIX_BASE = "!"
PREFIX_ADMIN = "/"

Couleurs des embeds
COULEUR_PRINCIPALE = 0x5865F2
COULEUR_SUCCES = 0x57F287
COULEUR_ERREUR = 0xED4245

IDs des rôles (à configurer)
ROLE_ADMIN_ID =
ROLE_MODERATEUR_ID =
```


---

## 🛠️ Technologies utilisées

- **Python 3.11+** - Langage de programmation
- **discord.py 2.3+** - Bibliothèque Discord
- **python-dotenv** - Gestion des variables d'environnement
- **asyncio** - Programmation asynchrone

---

## 📝 Logs

Le bot génère automatiquement des fichiers de logs dans le dossier `logs/` avec :
- Horodatage précis (jour/mois/année heure:minutes:secondes)
- Actions importantes (démarrage, erreurs, commandes)
- Un fichier par jour pour faciliter le débogage

---

## 🔒 Sécurité

- Le token Discord est stocké dans `secrets.env` (non versionné)
- Système de permissions robuste pour les commandes admin
- Validation des entrées utilisateur
- Logs de sécurité pour toutes les actions sensibles

---

## 📊 Versioning

Ce projet suit le versioning sémantique (SemVer) :
- **MAJOR** : Changements incompatibles
- **MINOR** : Nouvelles fonctionnalités compatibles
- **PATCH** : Corrections de bugs

Version actuelle : **v0.1.0**

---

## 📜 Licence

Ce projet est un bot privé développé par Latury.
Tous droits réservés © 2025

---

## 👤 Auteur

**Latury**
- GitHub : [@Latury](https://github.com/Latury)
- Projet : Bot Discord privé "La Loyauté"

---

<div align="center">

**Développé par Latury en Python**

*La Loyauté - Votre compagnon Discord de confiance*

</div>
