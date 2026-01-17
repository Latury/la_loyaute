# 🗺️ **Feuille de Route - La Loyauté**

**Roadmap détaillée du développement du bot Discord.**

---

## 🎯 **État actuel** _(13/01/2026)_

| Version    | Statut          | Date         | Progression |
| ---------- | --------------- | ------------ | ----------- |
| **v0.2.2** | ✅ Stable       | 13/01/2026   | **100%**    |
| **v0.3.0** | 🔄 **En cours** | Février 2026 | **0%**      |

### ✅ **Versions publiées**

| Version    | Date       | Description                                                                                                                           |
| ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **v0.2.2** | 13/01/2026 | **Corrections Pylance + outils dev**<br>23 imports doublons supprimés<br>Lanceur .exe PowerShell 7<br>Cache nettoyé → v0.2.2 affichée |
| **v0.2.1** | 05/01/2026 | **Configuration dynamique**<br>Config par serveur (JSON)<br>14 types de logs Discord<br>Outils dev (analyseur + doublons)             |
| **v0.2.0** | 26/12/2025 | **Logs + Permissions**<br>Système permissions personnalisé<br>Logs modération basiques                                                |
| **v0.1.0** | 25/12/2025 | **Fondations**<br>Architecture cogs + commandes slash                                                                                 |

---

## 🚀 **Versions futures**

### **v0.3.0 - Interface Configuration Interactive** _(Priorité #1)_

**Objectif :** Menu de configuration visuel (style DraftBot)
**Estimation :** 2-3 semaines

```
🎨 Fonctionnalités prévues :
├─ Menu principal avec Select Menu Discord
├─ Embeds interactifs avec boutons
├─ Configuration par catégories (Logs, Modération, Économie...)
├─ Prévisualisation en temps réel
├─ Système de navigation (breadcrumbs)
├─ Validation des configurations
├─ Export/Import JSON
└─ Sauvegarde automatique

📝 Commandes :
├─ /config → Menu principal interactif
├─ /config export → Exporter en JSON
└─ /config import → Importer config
```

---

### **v0.4.0 - Système d'Économie** _(Priorité #2)_

**Objectif :** Monnaie virtuelle + boutique
**Estimation :** 3-4 semaines

```
💰 Fonctionnalités :
├─ Monnaie virtuelle "coins"
├─ Gains : messages, commandes, événements
├─ Boutique d'items
├─ Inventaire personnel
├─ Transferts entre membres
├─ Récompenses quotidiennes
└─ Classement des plus riches

📝 Commandes :
├─ /balance [membre] → Voir solde
├─ /daily → Récompense quotidienne
├─ /shop → Ouvrir boutique
├─ /buy <item> → Acheter item
├─ /inventory → Voir inventaire
├─ /give <membre> <montant> → Donner argent
└─ /leaderboard coins → Classement richesse
```

---

### **v0.5.0 - Système de Niveaux et XP**

**Objectif :** Progression des membres
**Estimation :** 2-3 semaines

```
📈 Fonctionnalités :
├─ Système d'expérience (XP)
├─ Niveaux avec progression
├─ Rôles automatiques par niveau
├─ Multiplicateurs d'XP
├─ Carte de profil personnalisée
├─ Classement XP
└─ Configuration des gains XP

📝 Commandes :
├─ /rank [membre] → Voir niveau
└─ /leaderboard xp → Classement XP
```

---

### **v0.6.0 - Giveaways & Récompenses**

**Objectif :** Tirages au sort automatiques
**Estimation :** 2 semaines

```
🎁 Fonctionnalités :
├─ Création de giveaways
├─ Participation avec réactions
├─ Tirage au sort automatique
├─ Giveaways récurrents
└─ Conditions (rôle, niveau...)

📝 Commandes :
├─ /giveaway create → Créer giveaway
├─ /giveaway end → Terminer
└─ /giveaway reroll → Retirer gagnant
```

---

### **v0.7.0 - Mini-Jeux**

**Objectif :** Gagner des coins en jouant
**Estimation :** 3 semaines

```
🎮 Jeux prévus :
├─ Roulette (/roulette <mise> <couleur>)
├─ Pile/face (/coinflip <mise>)
├─ Dés (/dice <mise>)
├─ Pierre-papier-ciseaux (/rps <membre> <mise>)
├─ Blackjack (/blackjack <mise>)
└─ Slots machine (/slots <mise>)
```

---

## 📊 **Statistiques du projet**

| Métrique              | Valeur  |
| --------------------- | ------- |
| **Versions publiées** | 4/10    |
| **Lignes de code**    | ~5,000  |
| **Fichiers Python**   | 27      |
| **Commandes**         | 18      |
| **Cogs chargés**      | 8/8     |
| **Progrès global**    | **40%** |

| Version    | Progression |
| ---------- | ----------- |
| v0.1.0     | ✅ 100%     |
| v0.2.0     | ✅ 100%     |
| v0.2.1     | ✅ 100%     |
| **v0.2.2** | ✅ **100%** |
| v0.3.0     | 🔄 0%       |
| v0.4.0+    | ⏳ 0%       |

---

## 🎯 **Priorités actuelles**

### **Court terme (1-2 mois)**

1. **v0.3.0** - Interface config interactive _(Priorité ABSOLUE)_
2. Corrections bugs signalés
3. Optimisation performances

### **Moyen terme (3-6 mois)**

1. v0.4.0 - Économie
2. v0.5.0 - Niveaux XP
3. v0.6.0 - Giveaways

### **Long terme (6-12 mois)**

1. v0.7.0 - Mini-jeux
2. v0.8.0 - Lecteur musique
3. v1.0.0 - Dashboard web

---

## 🛠️ **Notes de développement**

### **Conventions de code** 🎨

```
✅ Commentaires avec emojis
✅ Numérotation des fonctions
✅ Type hints (Pylance)
✅ Documentation modules
✅ Gestion erreurs complète
```

### **Workflow Git** 🔄

```
main → Versions stables
dev → Développement actif
feature/* → Nouvelles fonctionnalités
tags → Versions publiées
```

### **Releases** 📦

- **0.x.0** → Nouvelles fonctionnalités majeures
- **0.x.y** → Corrections/améliorations
- **x.0.0** → Changements structurels

---

## 👥 **Contributions**

- **Développeur principal** : Latury
- **Contributions ouvertes** : À partir de v1.0.0

---

## 📝 **Légende des symboles**

| Symbole | Signification             |
| ------- | ------------------------- |
| 🪄      | Nouvelles fonctionnalités |
| 🤖      | Améliorations             |
| 🚧      | Corrections de bugs       |
| 🗃️      | Documentation             |
| 🔐      | Sécurité                  |
| 🔋      | Performance               |
| 🎨      | Interface/Design          |
| 🔧      | restructuration           |
| 🛠️      | Fonctionnalités           |
| 🧬      | Version du bot            |
| ❌      | Les erreurs               |

---

## 🔗 **Liens utiles**

- [README.md](README.md) → Documentation
- [CHANGELOG.md](CHANGELOG.md) → Historique
- [patchnotes.md](patchnotes.md) → Notes versions

**Dernière mise à jour :** 13/01/2026
**Prochaine révision :** Lors de v0.3.0
