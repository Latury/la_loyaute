<div align="center">

# 🛡️ **La Loyauté**

**Bot Discord privé développé en Python**

![Python](https://img.shields.io/badge/Python-3.14.2-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-2.7.0a-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Version](https://img.shields.io/badge/Version-0.2.2-yellow?style=for-the-badge&logo=git&logoColor=white)
![Statut](https://img.shields.io/badge/Statut-Stable-00FF00?style=for-the-badge&logo=discord&logoColor=white)

_Développé par [Latury](https://github.com/Latury)_

</div>

---

## 🎯 **Vue d'ensemble**

**La Loyauté** est un bot Discord **privé** conçu pour la modération avancée et la gestion de serveurs.
**Version actuelle :** `0.2.2` (13/01/2026)

### ✨ **Fonctionnalités principales**

#### **⚙️ Configuration dynamique (v0.2.1+)**

```
🔧 Config par serveur (JSON automatique)
📊 Salon logs privé (création auto)
📝 Commandes /config complètes
⏱️ Pas de redémarrage requis
```

### **🛡️ Modération complète**

```
🚫 kick/ban/unban
🔇 timeout (mute temporaire)
⚠️ warns (système complet)
🧹 clear (100 messages max)
📊 Logs de toutes les actions
```

#### **📊 14 types de logs Discord**

```
👥 Membres : join/leave/changements rôles
🗑️ Messages : delete/edit
📢 Salons : create/delete
🔨 Modération : kick/ban/warn/clear
```

#### **🛠️ Outils de développement (v0.2.1+)**

```
🔍 analysererreurs.py → Pylance/Pylint
🔎 detecterdoublons.py → Code dupliqué
📊 Rapports automatisés
🧹 Nettoyage cache
```

---

## 🏗️ **Structure du projet**

```
la_loyaute/
├── 📁 commandes/ # Commandes slash
│ ├── init.py
│ ├── commandes_base.py # ping, info
│ ├── commandes_admin.py # kick/ban/clear
│ └── commandes_configuration.py # config logs
├── 📁 evenements/ # Événements Discord
│ ├── init.py
│ ├── events_membres.py
│ ├── events_messages.py
│ └── events_salons.py
├── 📁 noyau/ # Logique métier
│ ├── init.py
│ ├── gestionnaire_bot.py
│ ├── gestionnaire_permissions.py
│ └── gestionnaire_configuration.py
├── 📁 utilitaires/ # Fonctions communes
│ ├── init.py
│ ├── logger.py
│ ├── helpers.py
│ └── logs_discord.py # 14 fonctions logs
├── 📁 outils_dev/ # 🔧 Outils développement
│ ├── init.py
│ ├── analyser_erreurs.py # Pylance/Pylint
│ ├── detecter_doublons.py # 23 doublons supprimés
│ ├── corriger_erreurs_auto.py # 12 setup() ajoutés
│ └── README.md
├── 📁 rapports/ # Rapports générés (Git ignore)
├── 📁 configurations/ # Config serveurs (Git ignore)
├── 🎯 principal.py # Point d'entrée
├── ⚙️ configuration.py # VERSION_BOT = "0.2.2"
├── 🚀 LaLoyauteBOT.bat # Lanceur .exe
├── 📄 README.md # ← Ce fichier
├── 📋 CHANGELOG.md
├── 📝 patchnotes.md
└── 🗺️ FEUILLE_DE_ROUTE.md
```

---

## 📋 **Commandes disponibles**

### **Commandes basiques** (👤 Tout le monde)

| Commande             | Description        |
| -------------------- | ------------------ |
| `/ping`              | Vérifie la latence |
| `/info`              | Informations bot   |
| `/userinfo <membre>` | Infos membre       |

### **Commandes modération** (🛡️ Modérateur)

| Commande                             | Description        |
| ------------------------------------ | ------------------ |
| `/kick <membre> [raison]`            | Expulser           |
| `/ban <membre> [raison]`             | Bannir             |
| `/unban <ID> [raison]`               | Débannir           |
| `/timeout <membre> <durée> [raison]` | Mute temporaire    |
| `/warn <membre> <raison>`            | Avertissement      |
| `/clear <nombre>`                    | Supprimer messages |

### **Commandes configuration** (👑 Admin)

| Commande                   | Description      |
| -------------------------- | ---------------- |
| `/config logs-set <salon>` | Définir logs     |
| `/config logs-create`      | Créer salon logs |
| `/config logs-show`        | Voir config      |
| `/config logs-reset`       | Désactiver logs  |

### **Commandes admin** (🔧 Admin)

| Commande              | Description    |
| --------------------- | -------------- |
| `/sync`               | Sync commandes |
| `/reload <extension>` | Recharger cog  |
| `/logs [nombre]`      | Voir logs bot  |
| `/shutdown`           | Arrêter bot    |

---

## 📈 **Performances v0.2.2**

| Métrique               | Valeur |
| ---------------------- | ------ |
| **Cogs chargés**       | 8/8    |
| **Commandes slash**    | 18     |
| **Types de logs**      | 14     |
| **Serveurs supportés** | ∞      |
| **Mémoire**            | ~50MB  |
| **Latence moyenne**    | <100ms |

---

## 🛠️ **Outils de développement**

### **1. Analyseur d'erreurs** `outils_dev/analyser_erreurs.py`

```
🔍 Détecte :
├─ Erreurs Pylance/Pylint
├─ Imports manquants
├─ Types incompatibles
└─ Génère rapport détaillé
```

### **2. Détecteur de doublons** `outils_dev/detecter_doublons.py`

```
🖱️ Double-clic → Bot lancé
🧹 Nettoie cache auto
🐍 Active venv
📊 Logs colorés
```

---

## 🎯 **Prochain développement : v0.3.0**

**Interface Configuration Interactive** (Priorité #1)

```
🎨 Menu SelectMenu + boutons
📱 Prévisualisation temps réel
💾 Export/Import JSON
⏱️ Estimation : 2-3 semaines
```

**Détails :** [FEUILLE_DE_ROUTE.md](FEUILLE_DE_ROUTE.md)

---

## 📚 **Documentation complète**

| Fichier                                    | Description         |
| ------------------------------------------ | ------------------- |
| [CHANGELOG.md](CHANGELOG.md)               | Historique versions |
| [patchnotes.md](patchnotes.md)             | Notes techniques    |
| [FEUILLE_DE_ROUTE.md](FEUILLE_DE_ROUTE.md) | Roadmap détaillée   |

---

## 👨‍💻 **Auteur**

**Latury**
[![GitHub](https://img.shields.io/badge/GitHub-Latury-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Latury)

**Version actuelle :** `0.2.2` _(13/01/2026)_
**Statut :** 🟢 **Stable**
