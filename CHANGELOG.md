# 📋 Changelog - La Loyauté

Historique des versions et modifications du projet.

---

## [0.2.2] - 13/01/2026

### 🔧 Corrections critiques

#### 🐛 Migration Python 3.14 et discord.py 2.7.0a
- **Python 3.14.2** : Migration vers la dernière version de Python
- **discord.py 2.7.0a** : Upgrade vers la version développement (commit b9b21ca2)
- **Annotations futures** : Ajout de `from __future__ import annotations` dans tous les modules
  - `commandes/__init__.py`
  - `commandes/commandes_admin.py`
  - `commandes/commandes_configuration.py`
  - `commandes/commandes_menu.py`
  - `commandes/commandes_base.py`
  - `utilitaires/embeds_interactifs.py`
  - `evenements/__init__.py`
  - `utilitaires/__init__.py`
  - `noyau/__init__.py`

#### 🔨 Corrections de structure
- **CommandesAdmin** : Correction de l'indentation de la fonction `/sync`
  - Fonction incorrectement placée en dehors de la classe
  - Réindentation avec 4 espaces pour être dans la classe `CommandesAdmin`
- **Fonction setup()** : Déplacement hors de la classe `CommandesAdmin`
  - Fonction incorrectement indentée dans la classe
  - Placée au niveau racine du module comme requis par discord.py

#### ⚡ Résolution d'erreurs
- **TypeError** : Résolution de `unsupported type annotation <class 'discord.interactions.Interaction'>`
- **Import annotations** : Compatibilité totale avec Python 3.14+
- **Cache Python** : Nettoyage complet des `__pycache__` pour éviter les conflits

### 📝 Fichiers modifiés

```
commandes/init.py
commandes/commandes_admin.py (indentation sync + setup)
commandes/commandes_configuration.py
commandes/commandes_menu.py
commandes/commandes_base.py
utilitaires/embeds_interactifs.py
evenements/init.py
utilitaires/init.py
noyau/init.py
requirements.txt (discord.py version)
```


### 🎯 Impact
- ✅ Le bot démarre correctement avec Python 3.14.2
- ✅ Toutes les commandes slash sont chargées
- ✅ Aucune erreur d'annotation de type
- ✅ Compatibilité totale discord.py 2.7.0a

---

## [0.2.1] - 05/01/2026

### ✨ Nouveautés majeures

#### 🔧 Système de configuration dynamique
- **Gestionnaire de configuration** : Nouveau module `noyau/gestionnaire_configuration.py`
- **Configuration par serveur** : Chaque serveur Discord a sa propre configuration
- **Stockage JSON** : Configuration sauvegardée dans `configurations_serveurs.json`
- **Commandes `/config`** :
  - `/config logs-set` : Définir un salon de logs
  - `/config logs-create` : Créer automatiquement un salon privé
  - `/config logs-show` : Afficher la configuration actuelle
  - `/config logs-reset` : Désactiver les logs

#### 📊 Système de logs Discord amélioré
- **14 fonctions de logs** disponibles dans `utilitaires/logs_discord.py`
- **Configuration dynamique** : Utilise le gestionnaire de configuration
- **Logs de modération** : kick, ban, unban, timeout, warn, clear
- **Logs de membres** : arrivée, départ, changements de rôles
- **Logs de messages** : suppression, modification
- **Logs de salons** : création, suppression

#### 🎉 Nouveaux événements
- **Events messages** : `evenements/events_messages.py`
  - Détection de messages supprimés
  - Détection de messages modifiés
- **Events salons** : `evenements/events_salons.py`
  - Détection de création de salons
  - Détection de suppression de salons
- **Events membres améliorés** : `evenements/events_membres.py`
  - Détection des changements de rôles

#### 🛠️ Outils de développement
- **Nouveau dossier** : `outils_dev/`
- **Analyseur d'erreurs** : `outils_dev/analyser_erreurs.py`
  - Détecte les erreurs Pylance/Pylint
  - Analyse les imports
  - Génère un rapport détaillé
- **Détecteur de doublons** : `outils_dev/detecter_doublons.py`
  - Détecte les fichiers identiques
  - Détecte les fonctions/classes dupliquées
  - Détecte les fichiers temporaires
- **Documentation** : `outils_dev/README.md`
- **Rapports** : Générés dans `outils_dev/rapports/`

### 🔧 Améliorations

#### Architecture
- Meilleure organisation du code
- Séparation des responsabilités (configuration, logs, events)
- Documentation enrichie dans tous les modules

#### Gestion des erreurs
- Vérifications de types améliorées (Pylance)
- Gestion gracieuse des erreurs Discord
- Messages d'erreur plus clairs

#### Performance
- Chargement optimisé des configurations
- Mise en cache des données de serveurs
- Réduction des appels API Discord

### 📝 Fichiers créés

```
noyau/gestionnaire_configuration.py
commandes/commandes_configuration.py
evenements/events_messages.py
evenements/events_salons.py
outils_dev/init.py
outils_dev/analyser_erreurs.py
outils_dev/detecter_doublons.py
outils_dev/README.md
```


### 📝 Fichiers modifiés

```
utilitaires/logs_discord.py
evenements/events_membres.py
evenements/init.py
noyau/gestionnaire_bot.py
principal.py
configuration.py
.gitignore
README.md
CHANGELOG.md
patchnotes.md
FEUILLE_DE_ROUTE.md
```


### 🐛 Corrections de bugs
- Correction des types Discord pour Pylance
- Correction de la gestion des messages sans serveur (MP)
- Correction des permissions manquantes
- Correction des imports relatifs

### 🔒 Sécurité
- Configuration sensible ignorée par Git
- Vérification des permissions avant actions
- Validation des entrées utilisateur

---

## [0.2.0] - 26/12/2025

### ✨ Nouveautés
- Système de permissions personnalisé
- Système de logs Discord basique
- Commandes de modération complètes
- Gestion des événements membres

### 📝 Fichiers créés

```
noyau/gestionnaire_permissions.py
utilitaires/logs_discord.py
evenements/events_membres.py
```


---

## [0.1.0] - 25/12/2025

### 🎉 Version initiale
- Structure de base du projet
- Système de commandes slash
- Commandes administrateur de base
- Logger personnalisé
- Configuration centralisée

### 📦 Modules principaux
- `principal.py` : Point d'entrée
- `configuration.py` : Configuration globale
- `noyau/gestionnaire_bot.py` : Classe du bot
- `commandes/commandes_base.py` : Commandes basiques
- `commandes/commandes_admin.py` : Commandes admin
- `utilitaires/logger.py` : Système de logs
- `utilitaires/helpers.py` : Fonctions utilitaires

---

## 📌 Légende des symboles

- ✨ Nouvelles fonctionnalités
- 🔧 Améliorations
- 🐛 Corrections de bugs
- 📝 Documentation
- 🔒 Sécurité
- ⚡ Performance
- 🎨 Interface/Design
- 🔨 Refactoring

---

**Dernière mise à jour :** 13/01/2026
**Version actuelle :** 0.2.2
