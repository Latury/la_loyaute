# 🗺️ Feuille de route - La Loyauté

Ce document présente la vision et les étapes de développement du bot Discord **La Loyauté**.

---

## 🎯 Vision du projet

Créer un bot Discord privé professionnel, modulaire et évolutif, offrant des fonctionnalités d'administration et d'interaction avancées pour une expérience Discord optimale. L'objectif est de fournir un outil complet, stable et facile à maintenir.

---

## ✅ Version 0.1.0 - Fondations (TERMINÉE)
**Statut :** ✅ Terminé et opérationnel
**Date de sortie :** 24/12/2025

- [x] Architecture modulaire complète du projet
- [x] Système de commandes de base avec prefix `!` (6 commandes)
- [x] Système de commandes admin avec slash commands `/` (5 commandes)
- [x] Gestionnaire de permissions avec rôles et décorateurs
- [x] Système de logs automatique avec rotation et couleurs
- [x] Configuration centralisée avec support `.env`
- [x] Documentation complète (README, CHANGELOG, patchnotes, feuille de route)
- [x] Cadre de démarrage ASCII professionnel
- [x] Embeds Discord personnalisés avec footer
- [x] Gestion des événements de messages (création, suppression, modification)
- [x] Statistiques en temps réel (uptime, RAM, latence, commandes)
- [x] Tests complets et validation du fonctionnement

---

## ✅ Version 0.2.0 - Logs Discord et Modération (TERMINÉE)
**Statut :** ✅ Terminé et opérationnel
**Date de sortie :** 26/12/2025

- [x] Système de logs Discord automatiques avec embeds
- [x] 10 fonctions de logs dans `utilitaires/logs_discord.py`
- [x] Commandes de modération : `/kick`, `/ban`, `/unban`, `/timeout`
- [x] Système de warns avec `/warn`, `/warnings`, `/removewarn`, `/clearwarns`
- [x] Commande `/setlogs` pour configuration du salon de logs
- [x] Événements de membres avec `on_member_join` et `on_member_remove`
- [x] Stockage des warns dans `donnees/warns.json`
- [x] Script `verifier_doublons.py` pour maintenance du code
- [x] Variable `LOGS_CHANNEL_ID` dans configuration
- [x] Extension `evenements.events_membres` chargée automatiquement
- [x] Documentation mise à jour (README, CHANGELOG, patchnotes)
- [x] Tests complets des nouvelles fonctionnalités

---

## 🔄 Version 0.2.1 - Logs Avancés (EN COURS)
**Statut :** 🚧 Planifié
**Priorité :** HAUTE
**Durée estimée :** 1-2 heures

### Objectifs
Compléter le système de logs avec tous les événements Discord importants

### Fonctionnalités prévues
- [ ] Logs de messages supprimés avec contenu complet
- [ ] Logs de messages modifiés avec avant/après en diff
- [ ] Logs de pièces jointes dans messages supprimés
- [ ] Logs de rôles ajoutés/retirés aux membres
- [ ] Logs de salons créés/modifiés/supprimés
- [ ] Logs de bannissements manuels (via interface Discord)
- [ ] Logs de permissions modifiées
- [ ] Amélioration des embeds de logs avec plus de détails

### Fichiers à modifier
- `utilitaires/logs_discord.py` : Ajouter nouvelles fonctions de logs
- `evenements/events_membres.py` : Ajouter événements de rôles
- Créer `evenements/events_salons.py` : Gestion des événements de salons
- Créer `evenements/events_moderation.py` : Logs de modération Discord native
- `principal.py` : Charger les nouvelles extensions

---

## 📋 Version 0.2.2 - Messages de Bienvenue (PLANIFIÉE)
**Statut :** 📋 Planifié
**Priorité :** HAUTE
**Durée estimée :** 1-2 heures

### Objectifs
Personnaliser l'accueil et le départ des membres

### Fonctionnalités prévues
- [ ] Messages de bienvenue personnalisables avec embeds
- [ ] Messages d'au revoir personnalisables
- [ ] Variables dynamiques (`{membre}`, `{serveur}`, `{total}`, `{date}`)
- [ ] Commande `/setwelcome` pour configuration
- [ ] Commande `/setgoodbye` pour configuration
- [ ] Prévisualisation des messages avant activation
- [ ] Attribution automatique d'un rôle par défaut
- [ ] Salon de bienvenue configurable
- [ ] Stockage de la configuration dans `donnees/welcome.json`

### Fichiers à créer/modifier
- `evenements/events_membres.py` : Ajouter envoi de messages personnalisés
- `commandes/commandes_admin.py` : Ajouter `/setwelcome`, `/setgoodbye`, `/setrole`
- `donnees/welcome.json` : Configuration des messages
- `configuration.py` : Variables pour messages par défaut

---

## 🎨 Version 0.3.0 - Améliorations UX (PLANIFIÉE)
**Statut :** 💡 Idée
**Priorité :** MOYENNE
**Durée estimée :** 2-3 heures

### Objectifs
Améliorer l'expérience utilisateur avec des commandes plus riches

### Fonctionnalités prévues
- [ ] Commande `/help` interactive avec pagination et boutons
- [ ] Commande `/userinfo @membre` ultra-détaillée
- [ ] Commande `/serverinfo` complète avec statistiques
- [ ] Commande `/avatar @membre` pour afficher l'avatar en HD
- [ ] Commande `/banner @membre` pour afficher la bannière
- [ ] Commande `/remind` pour rappels programmés
- [ ] Amélioration des embeds (couleurs cohérentes, thumbnails)
- [ ] Système de pagination réutilisable pour longues listes
- [ ] Boutons interactifs sur certaines commandes

### Fichiers à créer/modifier
- `commandes/commandes_base.py` : Ajouter `/userinfo`, `/serverinfo`, `/avatar`
- `utilitaires/pagination.py` : Système de pagination avec boutons
- `utilitaires/rappels.py` : Gestion des rappels programmés
- `commandes/commandes_admin.py` : Améliorer `/help` avec pagination

---

## 🛡️ Version 0.4.0 - Auto-Modération (PLANIFIÉE)
**Statut :** 💡 Idée
**Priorité :** MOYENNE
**Durée estimée :** 3-4 heures

### Objectifs
Automatiser la modération pour réduire la charge des modérateurs

### Fonctionnalités prévues
- [ ] Détection et suppression automatique de spam
- [ ] Filtre de mots interdits personnalisable
- [ ] Anti-raid avec détection de comptes suspects
- [ ] Quarantaine automatique des nouveaux comptes (< 7 jours)
- [ ] Auto-warn sur infractions répétées
- [ ] Limites de mentions (@everyone, @here, mentions multiples)
- [ ] Limites d'emojis dans un message
- [ ] Détection de CAPS LOCK excessif
- [ ] Commandes de configuration `/automod`, `/setfilter`, `/antiraid`
- [ ] Whitelist de salons/rôles exemptés

### Fichiers à créer/modifier
- Créer `noyau/automoderation.py` : Logique de modération automatique
- Créer `utilitaires/filtre_mots.py` : Système de filtre de mots
- Créer `utilitaires/detection_spam.py` : Détection de spam
- `evenements/messages.py` : Intégrer les vérifications d'automod
- `commandes/commandes_admin.py` : Commandes de configuration
- `donnees/automod.json` : Configuration de l'automodération
- `donnees/filtre.json` : Liste des mots interdits

---

## 🎫 Version 0.5.0 - Système de Tickets (PLANIFIÉE)
**Statut :** 💡 Idée
**Priorité :** MOYENNE
**Durée estimée :** 3-4 heures

### Objectifs
Créer un système de support avec tickets Discord

### Fonctionnalités prévues
- [ ] Création de tickets via bouton ou commande `/ticket`
- [ ] Catégories de tickets (Support, Report, Question, Autre)
- [ ] Panel de création avec menu déroulant
- [ ] Salon privé créé automatiquement
- [ ] Permissions automatiques (membre + staff)
- [ ] Commandes dans les tickets : `/close`, `/claim`, `/unclaim`, `/add`, `/remove`
- [ ] Fermeture avec transcription sauvegardée
- [ ] Système de priority (basse, normale, haute, urgente)
- [ ] Statistiques des tickets par membre/staff
- [ ] Historique des tickets fermés
- [ ] Configuration via `/ticketsetup`, `/ticketconfig`

### Fichiers à créer/modifier
- Créer `noyau/gestionnaire_tickets.py` : Logique de gestion des tickets
- Créer `commandes/commandes_tickets.py` : Commandes de tickets
- Créer `evenements/events_tickets.py` : Événements liés aux tickets
- Créer `utilitaires/transcription.py` : Sauvegarde des conversations
- `donnees/tickets.json` : Configuration et historique
- `configuration.py` : Variables pour tickets

---

## ⭐ Version 0.6.0 - Système de Niveaux/XP (PLANIFIÉE)
**Statut :** 💡 Idée
**Priorité :** BASSE
**Durée estimée :** 4-5 heures

### Objectifs
Récompenser l'activité des membres avec un système de progression

### Fonctionnalités prévues
- [ ] Gain d'XP par message (avec cooldown anti-spam)
- [ ] Système de niveaux progressifs (formule exponentielle)
- [ ] Commande `/rank` pour voir son niveau et progression
- [ ] Commande `/leaderboard` pour classement des membres
- [ ] Attribution automatique de rôles par niveau
- [ ] Messages de level-up personnalisables (DM ou salon)
- [ ] Configuration des gains d'XP par salon
- [ ] Système de boost d'XP (événements, rôles VIP)
- [ ] XP pour temps passé en vocal
- [ ] Commandes admin `/setxp`, `/addxp`, `/removexp`, `/resetxp`
- [ ] Statistiques détaillées par membre
- [ ] Carte de profil avec image générée
- [ ] Base de données SQLite pour stockage

### Fichiers à créer/modifier
- Créer `noyau/systeme_niveaux.py` : Logique XP et niveaux
- Créer `commandes/commandes_niveaux.py` : Commandes de niveaux
- Créer `utilitaires/generateur_carte.py` : Génération d'images de profil
- Créer `donnees/niveaux.db` : Base de données SQLite
- `evenements/messages.py` : Ajout d'XP sur message
- `configuration.py` : Configuration des niveaux

---

## 🏆 Version 1.0.0 - Release Finale (FUTURE)
**Statut :** 💡 Idée
**Priorité :** À définir

### Objectifs
Bot mature, stable et complet prêt pour la production

### Fonctionnalités prévues
- [ ] Tests approfondis de toutes les fonctionnalités
- [ ] Documentation complète (README, Wiki, tutoriels)
- [ ] Polish final des embeds et messages
- [ ] Optimisations de performance
- [ ] Gestion avancée des erreurs
- [ ] Commandes de diagnostic pour débogage
- [ ] Monitoring et alertes
- [ ] Dashboard web (optionnel)
- [ ] API REST pour intégrations (optionnel)
- [ ] Multi-langue (français/anglais)
- [ ] Migration vers base de données PostgreSQL (optionnel)

---

## 💡 Boîte à idées (non priorisées)

Fonctionnalités suggérées pour évaluation future :

### Modération
- [ ] Anti-phishing avec détection de liens suspects
- [ ] Détection d'invitations Discord non autorisées
- [ ] Système de captcha pour nouveaux membres
- [ ] Logs de messages édités/supprimés avec cache

### Divertissement
- [ ] Mini-jeux (pierre-papier-ciseaux, dés, pendu, morpion)
- [ ] Commandes de fun (memes, gifs, blagues, citations)
- [ ] Système d'économie virtuelle (monnaie du serveur)
- [ ] Casino avec jeux d'argent virtuel (blackjack, slots)

### Utilitaires
- [ ] Traduction automatique de messages
- [ ] Conversion d'unités (température, devises, distances)
- [ ] Calculs mathématiques avancés
- [ ] Générateur de QR codes
- [ ] Raccourcisseur d'URLs
- [ ] Informations météo en temps réel
- [ ] Recherche Google/Wikipedia intégrée

### Social
- [ ] Profils utilisateurs enrichis avec bio
- [ ] Système de badges et achievements
- [ ] Mariages et relations virtuelles
- [ ] Inventaires personnels
- [ ] Sondages avancés avec graphiques

### Musique (version future)
- [ ] Commandes de musique (YouTube, Spotify)
- [ ] Lecteur audio dans salons vocaux
- [ ] Playlists personnalisées
- [ ] File d'attente et contrôles
- [ ] Paroles en temps réel

---

## 📝 Notes importantes

- Les fonctionnalités ci-dessus sont des **idées** et non des engagements
- Les priorités peuvent évoluer selon les besoins
- De nouvelles idées seront ajoutées au fil du temps
- Chaque version sera testée et documentée avant release
- Le projet restera modulaire pour faciliter l'évolution

---

## 🎯 Priorités actuelles

Pour le moment, concentrons-nous sur :
1. ✅ Stabilisation de la v0.1.0 (FAIT)
2. ✅ Système de logs Discord v0.2.0 (FAIT)
3. 🚧 Logs avancés pour v0.2.1 (EN COURS)
4. 📋 Messages de bienvenue pour v0.2.2
5. 💡 Planification des versions 0.3.0+

---

## 💭 Vos suggestions

Vous avez des idées pour améliorer La Loyauté ? Notez-les ici :

- [ ] _Ajoutez vos suggestions ici..._
- [ ]
- [ ]

---

*Dernière mise à jour : 26/12/2025 02:40:00*
*Document vivant - Sera mis à jour régulièrement*
