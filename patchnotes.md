# 🔄 Notes de mise à jour

Bienvenue dans les notes de mise à jour de **La Loyauté** ! Ce fichier présente les nouveautés, améliorations et corrections de chaque version de manière accessible.

---

## 🎊 Version 0.2.0 - Système de Logs Discord et Modération Avancée
**Date de sortie :** 26 décembre 2025
**Statut :** ✅ Version stable et opérationnelle

### 🌟 Nouveautés majeures

#### 📊 Système de logs Discord automatiques

La Loyauté peut maintenant enregistrer toutes les actions importantes directement dans un salon Discord dédié !

**Configuration simple :**
- Utilisez `/setlogs #nom-du-salon` pour activer les logs
- Utilisez `/setlogs` sans paramètre pour les désactiver
- Les logs apparaissent instantanément avec des embeds colorés

**Ce qui est automatiquement loggé :**

- 👢 **Expulsions** (kick) : Qui a été expulsé, par qui, et pourquoi
- 🔨 **Bannissements** (ban) : Avec la raison et le modérateur responsable
- ✅ **Débannissements** (unban) : Quand un utilisateur est débanni
- ⏱️ **Timeouts** : Durée exacte et raison de la mise en silence
- ⚠️ **Avertissements** (warns) : Compteur d'avertissements avec historique
- 🗑️ **Suppressions de messages** : Combien de messages supprimés et par qui
- 👋 **Arrivées de membres** : Âge du compte, nombre total de membres
- 👋 **Départs de membres** : Temps passé sur le serveur

**Logs visuels professionnels :**
- Embeds Discord avec couleurs contextuelles (rouge pour ban, vert pour unban, etc.)
- Informations complètes (IDs, noms, raisons, timestamps)
- Footer avec le nom du bot
- Horodatage automatique Discord

---

#### 🛡️ Commandes de modération complètes

9 nouvelles commandes puissantes pour gérer votre serveur :

##### **`/kick @membre [raison]`** - Expulser un membre
- Expulse un membre du serveur (il peut revenir avec une invitation)
- Raison optionnelle enregistrée dans les logs
- Log automatique dans le salon configuré
- Vérification des permissions (le modérateur ne peut pas kick quelqu'un de rang supérieur)

**Exemple :**

```
/kick @Membre Spam répété malgré avertissements
```


##### **`/ban @membre [raison]`** - Bannir un membre
- Bannit définitivement un membre du serveur
- Raison optionnelle pour traçabilité
- Le membre ne peut plus revenir sans débannissement
- Log automatique avec détails complets

**Exemple :**

```
/ban @Troll Propos inappropriés et harcèlement
```


##### **`/unban user_id [raison]`** - Débannir un utilisateur
- Retire le bannissement d'un utilisateur via son ID
- Raison optionnelle (ex: "Ban injustifié", "Membre excusé")
- Log automatique du débannissement

**Exemple :**

```
/unban 123456789012345678 Ban injustifié après vérification
```


##### **`/timeout @membre [durée] [raison]`** - Mettre en timeout
- Met un membre en silence temporaire
- Durée : `1m`, `5m`, `10m`, `1h`, `1d`, `1w` (minutes, heures, jours, semaines)
- Le membre ne peut plus écrire ni parler pendant la durée
- Log avec durée exacte et raison

**Exemples :**

```
/timeout @Membre 10m Flood dans le salon général
/timeout @Membre 1h Insultes envers un autre membre
/timeout @Membre 1d Multiples infractions
```


##### **`/warn @membre [raison]`** - Avertir un membre
- Ajoute un avertissement à l'historique du membre
- Stockage permanent dans `donnees/warns.json`
- Compteur d'avertissements affiché
- Log automatique avec numéro d'avertissement

**Exemple :**

```
/warn @Membre Langage inapproprié
```


##### **`/warnings @membre`** - Consulter les avertissements
- Affiche l'historique complet des warns d'un membre
- Liste numérotée avec date, modérateur, et raison
- Compteur total d'avertissements
- Embed formaté proprement

**Exemple :**

```
/removewarn @Membre 2
```


##### **`/clearwarns @membre`** - Effacer tous les avertissements
- Supprime tous les warns d'un membre
- Demande de confirmation
- Utile pour "ardoise propre" après bonne conduite
- Log de l'action

**Exemple :**

```
/clearwarns @Membre
```


##### **`/setlogs [#salon]`** - Configurer le salon de logs
- Active les logs en spécifiant un salon
- Désactive les logs si aucun salon n'est spécifié
- Envoie un message de test pour confirmer
- Configuration sauvegardée dans `configuration.py`

**Exemples :**

```
/setlogs #logs-moderation → Active les logs
/setlogs → Désactive les logs
```


---

#### 👥 Événements de membres automatiques

Nouveau module `evenements/events_membres.py` qui détecte :

**Arrivée d'un membre :**
- Détection automatique via `on_member_join`
- Log avec :
  - Nom complet et mention du membre
  - ID Discord
  - Âge du compte (créé il y a X jours)
  - Nombre total de membres sur le serveur
  - Horodatage précis

**Départ d'un membre :**
- Détection automatique via `on_member_remove`
- Log avec :
  - Nom complet du membre parti
  - ID Discord
  - Temps passé sur le serveur (X jours)
  - Nombre restant de membres
  - Horodatage précis

---

#### 📝 Système de warns avec stockage

Nouveau système d'avertissements avec persistance :

**Stockage :**
- Fichier `donnees/warns.json` créé automatiquement
- Structure par serveur et par utilisateur
- Historique complet avec :
  - Date et heure précises
  - Modérateur responsable (nom et ID)
  - Raison de l'avertissement
  - Numéro séquentiel

**Gestion :**
- Ajout via `/warn`
- Consultation via `/warnings`
- Suppression unitaire via `/removewarn`
- Suppression totale via `/clearwarns`

**Exemple de stockage :**

```
{
"123456789012345678": {
"987654321098765432": [
{
"date": "26/12/2025 02:15:30",
"moderateur": "Admin#1234",
"moderateur_id": "111222333444555666",
"raison": "Spam dans le salon général"
}
]
}
}
```


---

#### 🔧 Outil de vérification de doublons

Nouveau script `verifier_doublons.py` pour maintenir la qualité du code :

**Fonctionnalités :**
- Détecte les fichiers avec le même nom
- Détecte les fichiers avec contenu identique (hash MD5)
- Détecte les fichiers temporaires et backups (.bak, .backup, etc.)
- Détecte les fonctions Python définies dans plusieurs fichiers
- Détecte les classes Python dupliquées
- Ignore automatiquement `.venv`, `__pycache__`, `.git`, etc.

**Utilisation :**

```
python verifier_doublons.py
```


**Résultat :**
- Rapport complet généré sur le Bureau : `rapport_doublons_la_loyaute.txt`
- Statistiques du projet (nombre de fichiers, taille totale)
- Verdict final (projet propre ou problèmes détectés)
- Recommandations d'actions à entreprendre

---

### 🔧 Améliorations techniques

#### Architecture
- Nouveau module `utilitaires/logs_discord.py` avec 10 fonctions de logs
- Nouveau module `evenements/events_membres.py` pour événements de membres
- Extension `evenements.events_membres` chargée automatiquement au démarrage
- Dossier `donnees/` créé pour stockage des warns

#### Configuration
- Nouvelle variable `LOGS_CHANNEL_ID` dans `configuration.py`
- Documentation sur comment obtenir l'ID d'un salon Discord
- Valeur par défaut à 0 (logs désactivés)

#### Sécurité
- Vérification des permissions avant toute action de modération
- Impossibilité de kick/ban soi-même ou le bot
- Impossibilité de modérer un membre avec un rôle supérieur
- Logs de toutes les actions sensibles
- Stockage sécurisé des warns avec horodatage

#### Performance
- Gestion asynchrone des logs Discord
- Vérification de l'existence du salon avant envoi
- Gestion des erreurs si salon supprimé ou inaccessible
- Cache des informations pour éviter appels API répétés

---

### 📚 Documentation mise à jour

- README.md : Arborescence du projet mise à jour avec nouveaux fichiers
- README.md : Tableau des commandes admin complété avec 9 nouvelles commandes
- CHANGELOG.md : Historique détaillé de la version 0.2.0
- FEUILLE_DE_ROUTE.md : Progression et prochaines étapes
- Commentaires dans le code avec explications détaillées

---

### 🐛 Corrections

- Suppression du fichier backup `commandes_admin.py.backup_20251224_064816`
- Script `verifier_doublons.py` ajouté au `.gitignore`
- Aucun doublon critique détecté dans le projet
- Architecture validée et propre

---

### 💡 Ce que vous pouvez faire maintenant

**Configurez les logs Discord :**
1. Créez un salon `#logs-moderation` sur votre serveur
2. Utilisez `/setlogs #logs-moderation` pour activer
3. Testez avec `/warn @Membre Test` pour voir le résultat

**Testez les commandes de modération :**

```
/kick @Membre Raison de test
/ban @Membre Test de bannissement
/timeout @Membre 5m Test de timeout
/warn @Membre Test d'avertissement
/warnings @Membre
```


**Vérifiez votre projet :**

```
python verifier_doublons.py
```


---

## 🎊 Version 0.1.0 - Lancement Initial
**Date de sortie :** 24 décembre 2025
**Statut :** ✅ Version stable et opérationnelle

### 🌟 Nouveautés majeures

#### 🏗️ Architecture & Fondations
La Loyauté fait ses premiers pas avec une architecture professionnelle et modulaire :
- Structure de projet claire avec séparation des responsabilités
- 4 modules principaux (noyau, commandes, événements, utilitaires)
- 15 fichiers Python organisés logiquement
- Documentation complète en français

#### 💬 Système de commandes de base (prefix `!`)

Découvrez les 6 commandes accessibles à tous les utilisateurs :

- **`!aide`** - Votre guide complet
- **`!info`** - Carte d'identité du bot
- **`!ping`** - Test de réactivité
- **`!stats`** - Tableau de bord complet
- **`!serveur`** - Informations sur votre serveur
- **`!utilisateur [@mention]`** - Profil d'un membre

#### 👑 Commandes administratives (prefix `/`)

5 puissantes slash commands pour les administrateurs :

- **`/clear [nombre]`** - Nettoyage de messages
- **`/logs [nombre]`** - Consultation des logs
- **`/config`** - Configuration du bot
- **`/reload [extension]`** - Rechargement à chaud
- **`/shutdown`** - Arrêt propre du bot

---

## 🎯 Prochaines étapes - Version 0.2.1

La version suivante apportera :
- 📝 **Logs de messages supprimés** avec contenu complet et pièces jointes
- ✏️ **Logs de messages modifiés** avec avant/après en diff
- 🎭 **Logs de rôles ajoutés/retirés** aux membres
- 🏗️ **Logs de salons créés/modifiés/supprimés**
- 🔒 **Logs de permissions modifiées** sur le serveur

Puis version 0.2.2 :
- 👋 **Messages de bienvenue** personnalisables avec variables
- 👋 **Messages d'au revoir** personnalisables
- 🎨 **Attribution automatique de rôle** aux nouveaux membres

Restez à l'écoute pour les prochaines mises à jour !

---

## 📞 Support

Si vous rencontrez un problème ou avez une suggestion :
- Utilisez `!aide` pour voir toutes les commandes
- Consultez le README.md pour la documentation complète
- Vérifiez les logs avec `/logs` si vous êtes admin
- Utilisez `/config` pour voir votre configuration actuelle

---

*Développé avec passion par Latury 🛡️*

*Version 0.2.0 | 26/12/2025*

