# 🗺️ Feuille de Route - La Loyauté

Roadmap détaillée du développement du bot Discord.

---

## 📊 État actuel : Version 0.2.1 ✅

**Date de release :** 05/01/2026
**Statut :** Stable

---

## ✅ Versions publiées

### 🎉 v0.2.1 - Configuration Dynamique (05/01/2026) ✅

**Fonctionnalités implémentées :**
- ✅ Système de configuration dynamique par serveur
- ✅ Commandes `/config` complètes (logs-set, logs-create, logs-show, logs-reset)
- ✅ Gestionnaire de configuration avec sauvegarde JSON
- ✅ 14 types de logs Discord (modération, membres, messages, salons)
- ✅ Outils de développement (analyseur d'erreurs, détecteur de doublons)
- ✅ Correction complète des erreurs Pylance
- ✅ Documentation enrichie (README, CHANGELOG, patchnotes)

### 🔄 v0.2.0 - Logs et Permissions (26/12/2025) ✅
- ✅ Système de permissions
- ✅ Logs Discord de base
- ✅ Événements membres

### 🎉 v0.1.0 - Fondations (25/12/2025) ✅
- ✅ Architecture de base
- ✅ Commandes slash
- ✅ Système de modération basique

---

## 🚀 Versions futures

### 📋 v0.3.0 - Interface Configuration Interactive (En cours de planification)

**Objectif :** Menu de configuration visuel style DraftBot

**Fonctionnalités prévues :**
- 🔲 Menu principal avec Select Menu Discord
- 🔲 Embeds interactifs avec boutons
- 🔲 Configuration par catégories (Logs, Modération, Économie, etc.)
- 🔲 Prévisualisation en temps réel
- 🔲 Système de navigation avec breadcrumbs
- 🔲 Validation des configurations
- 🔲 Export/import de configuration

**Commandes :**
- `/config` → Menu principal interactif
- `/config export` → Exporter la config en JSON
- `/config import` → Importer une config

**Estimation :** 2-3 semaines

---

### 💰 v0.4.0 - Système d'Économie (Planifiée)

**Objectif :** Économie virtuelle avec monnaie et boutique

**Fonctionnalités prévues :**
- 🔲 Monnaie virtuelle (coins)
- 🔲 Système de gains (messages, commandes, événements)
- 🔲 Boutique d'items
- 🔲 Inventaire personnel
- 🔲 Transferts entre membres
- 🔲 Système de récompenses quotidiennes
- 🔲 Classement des plus riches

**Commandes :**
- `/balance [@membre]` → Voir le solde
- `/daily` → Récompense quotidienne
- `/shop` → Ouvrir la boutique
- `/buy <item>` → Acheter un item
- `/inventory` → Voir son inventaire
- `/give @membre <montant>` → Donner de l'argent
- `/leaderboard coins` → Classement richesse

**Estimation :** 3-4 semaines

---

### 📈 v0.5.0 - Système de Niveaux et XP (Planifiée)

**Objectif :** Progression des membres avec niveaux et rôles

**Fonctionnalités prévues :**
- 🔲 Système d'expérience (XP)
- 🔲 Niveaux avec progression
- 🔲 Rôles automatiques par niveau
- 🔲 Multiplicateurs d'XP
- 🔲 Carte de profil personnalisée
- 🔲 Classement des niveaux
- 🔲 Configuration des gains XP

**Commandes :**
- `/rank [@membre]` → Voir le niveau
- `/leaderboard xp` → Classement XP
- `/config xp` → Configurer le système XP

**Estimation :** 2-3 semaines

---

### 🎁 v0.6.0 - Système de Récompenses (Planifiée)

**Objectif :** Giveaways et récompenses automatiques

**Fonctionnalités prévues :**
- 🔲 Création de giveaways
- 🔲 Participation avec réactions
- 🔲 Tirage au sort automatique
- 🔲 Giveaways récurrents
- 🔲 Conditions de participation (rôle, niveau, etc.)
- 🔲 Récompenses multiples

**Commandes :**
- `/giveaway create` → Créer un giveaway
- `/giveaway end` → Terminer un giveaway
- `/giveaway reroll` → Retirer un gagnant

**Estimation :** 2 semaines

---

### 🎮 v0.7.0 - Mini-jeux (Planifiée)

**Objectif :** Jeux intégrés pour gagner des coins

**Fonctionnalités prévues :**
- 🔲 Roulette
- 🔲 Pile ou face
- 🔲 Dés
- 🔲 Pierre-papier-ciseaux
- 🔲 Blackjack
- 🔲 Slots machine

**Commandes :**
- `/roulette <mise> <couleur>` → Jouer à la roulette
- `/coinflip <mise> <pile/face>` → Pile ou face
- `/dice <mise>` → Lancer de dés
- `/rps @membre <mise>` → Pierre-papier-ciseaux
- `/blackjack <mise>` → Jouer au blackjack
- `/slots <mise>` → Machine à sous

**Estimation :** 3 semaines

---

### 🎵 v0.8.0 - Lecteur de Musique (Planifiée)

**Objectif :** Lecture de musique dans les salons vocaux

**Fonctionnalités prévues :**
- 🔲 Lecture YouTube/Spotify
- 🔲 Queue de lecture
- 🔲 Contrôles (pause, skip, etc.)
- 🔲 Playlists sauvegardées
- 🔲 Recherche de musique
- 🔲 Filtres audio

**Commandes :**
- `/play <recherche/url>` → Jouer une musique
- `/pause` → Mettre en pause
- `/resume` → Reprendre
- `/skip` → Passer
- `/queue` → Voir la queue
- `/playlist` → Gérer les playlists

**Estimation :** 4-5 semaines

---

### 🎫 v0.9.0 - Système de Tickets (Planifiée)

**Objectif :** Support utilisateur avec tickets privés

**Fonctionnalités prévues :**
- 🔲 Création de tickets
- 🔲 Salons privés automatiques
- 🔲 Système de catégories
- 🔲 Panel de gestion
- 🔲 Logs des tickets
- 🔲 Transcription automatique

**Commandes :**
- `/ticket create [raison]` → Créer un ticket
- `/ticket close` → Fermer un ticket
- `/ticket add @membre` → Ajouter quelqu'un
- `/ticket remove @membre` → Retirer quelqu'un

**Estimation :** 2-3 semaines

---

### 🌐 v1.0.0 - Dashboard Web (Planifiée)

**Objectif :** Interface web pour gérer le bot

**Fonctionnalités prévues :**
- 🔲 Dashboard complet
- 🔲 Authentification Discord OAuth2
- 🔲 Configuration visuelle
- 🔲 Statistiques en temps réel
- 🔲 Gestion des serveurs
- 🔲 Logs consultables
- 🔲 Gestion de la boutique

**Technologies :**
- Backend : FastAPI (Python)
- Frontend : React + Tailwind CSS
- Base de données : PostgreSQL

**Estimation :** 6-8 semaines

---

## 📊 Statistiques du projet

### Versions actuelles
- **Version stable** : 0.2.1
- **Dernière mise à jour** : 05/01/2026
- **Prochaine version** : 0.3.0 (planifiée)

### Progrès global

```
v0.1.0 ████████████████████ 100% ✅
v0.2.0 ████████████████████ 100% ✅
v0.2.1 ████████████████████ 100% ✅
v0.3.0 ░░░░░░░░░░░░░░░░░░░░ 0% 🔲
v0.4.0 ░░░░░░░░░░░░░░░░░░░░ 0% 🔲
v0.5.0 ░░░░░░░░░░░░░░░░░░░░ 0% 🔲
```


---

## 🎯 Priorités actuelles

### Court terme (1-2 mois)
1. **v0.3.0** - Interface configuration interactive
2. Correction des bugs reportés
3. Optimisation des performances

### Moyen terme (3-6 mois)
1. **v0.4.0** - Système d'économie
2. **v0.5.0** - Système de niveaux
3. **v0.6.0** - Récompenses et giveaways

### Long terme (6-12 mois)
1. **v0.7.0** - Mini-jeux
2. **v0.8.0** - Lecteur de musique
3. **v0.9.0** - Système de tickets
4. **v1.0.0** - Dashboard web

---

## 💡 Idées en réflexion

### Fonctionnalités possibles
- 🤔 Système de suggestions
- 🤔 Auto-modération (spam, flood, etc.)
- 🤔 Sondages avancés
- 🤔 Système de réactions personnalisées
- 🤔 Salons temporaires
- 🤔 Système d'anniversaires
- 🤔 Intégration Twitch (notifications)
- 🤔 Système de backup automatique
- 🤔 Multi-langue

### Améliorations techniques
- 🤔 Migration vers PostgreSQL
- 🤔 Système de cache Redis
- 🤔 API REST pour extensions
- 🤔 Tests automatisés (pytest)
- 🤔 CI/CD avec GitHub Actions
- 🤔 Documentation générée automatiquement

---

## 📝 Notes de développement

### Conventions de code
- ✅ Commentaires avec emojis
- ✅ Numérotation des fonctions
- ✅ Type hints Pylance
- ✅ Documentation des modules
- ✅ Gestion des erreurs complète

### Workflow Git
1. Branche `main` : versions stables
2. Branche `dev` : développement actif
3. Branches feature : nouvelles fonctionnalités
4. Tags : versions publiées

### Releases
- **Versions mineures** (0.x.0) : nouvelles fonctionnalités majeures
- **Patches** (0.x.y) : corrections et améliorations
- **Versions majeures** (x.0.0) : changements structurels importants

---

## 🤝 Contributions

Ce projet est actuellement développé en solo par **Latury**.

Des contributions pourront être acceptées à partir de la **v1.0.0**.

---

## 📌 Liens utiles

- [README.md](README.md) - Documentation
- [CHANGELOG.md](CHANGELOG.md) - Historique
- [patchnotes.md](patchnotes.md) - Notes de versions

---

**Dernière mise à jour :** 05/01/2026
**Prochaine révision :** Lors de la v0.3.0
