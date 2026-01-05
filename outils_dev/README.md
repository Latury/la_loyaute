# 🛠️ Outils de Développement - La Loyauté

Ce dossier contient des scripts utilitaires pour maintenir la qualité du code du projet.

## 📦 Scripts disponibles

### 🔍 `analyser_erreurs.py`

Analyse le code Python du projet pour détecter les erreurs Pylance/Pylint.

**Utilisation :**
```bash
python outils_dev/analyser_erreurs.py

Fonctionnalités :

✅ Analyse tous les fichiers .py du projet

✅ Détecte les erreurs d'imports

✅ Intégration Pylint (optionnel)

✅ Génère un rapport détaillé dans outils_dev/rapports/

🔍 detecter_doublons.py
Détecte les doublons de code dans le projet (fichiers identiques, fonctions/classes dupliquées).

Utilisation :

python outils_dev/detecter_doublons.py

Fonctionnalités :

✅ Détecte les fichiers avec le même nom

✅ Détecte les fichiers avec contenu identique (hash MD5)

✅ Détecte les fichiers temporaires (.backup, .bak, etc.)

✅ Détecte les fonctions dupliquées

✅ Détecte les classes dupliquées

✅ Génère un rapport détaillé dans outils_dev/rapports/

📊 Rapports générés
Tous les rapports sont sauvegardés dans le dossier outils_dev/rapports/ avec un horodatage :

outils_dev/
└── rapports/
    ├── rapport_erreurs_20260105_123456.txt
    └── rapport_doublons_20260105_123456.txt

⚠️ Note : Le dossier rapports/ est ignoré par Git (voir .gitignore)

🎯 Bonnes pratiques
Avant chaque commit
Exécuter analyser_erreurs.py pour vérifier qu'il n'y a pas d'erreurs

Exécuter detecter_doublons.py pour nettoyer le code

Avant chaque release
Analyser le projet complet

Corriger toutes les erreurs critiques

Supprimer les doublons détectés

🔧 Configuration
Les scripts analysent automatiquement les dossiers suivants :

commandes/

evenements/

noyau/

utilitaires/

principal.py

configuration.py

Dossiers ignorés :

__pycache__

.venv, venv, env

.git, .vscode, .idea

outils_dev (pour éviter l'auto-analyse)

📝 Version
Version actuelle : 0.2.1
Dernière mise à jour : 05/01/2026

👤 Développeur
Développé par Latury pour le projet La Loyauté


***

## 📝 **FICHIER 5 : `.gitignore` (MIS À JOUR)**

**Remplace TOUT le contenu de `.gitignore`** :

```gitignore
# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🛡️ LA LOYAUTÉ - FICHIERS IGNORÉS PAR GIT
# ║
# ║ Liste des fichiers et dossiers à ne pas versionner
# ║ Version : 0.2.1
# ║
# ═══════════════════════════════════════════════════════════════════════════════

# ⚙️ FICHIERS SECRETS
secrets.env
.env
*.env.local

# 🐍 PYTHON
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 🌐 ENVIRONNEMENTS VIRTUELS
.venv/
venv/
env/
ENV/
env.bak/
venv.bak/

# 🔧 IDE ET ÉDITEURS
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# 📊 LOGS ET BASES DE DONNÉES
*.log
logs/
*.db
*.sqlite
*.sqlite3

# 🛠️ RAPPORTS DES OUTILS DE DÉVELOPPEMENT (NOUVEAU v0.2.1)
outils_dev/rapports/
outils_dev/*.txt

# 📦 FICHIERS TEMPORAIRES
*.tmp
*.temp
*.backup
*.bak
*.old
*.orig

# 🎯 CONFIGURATION DYNAMIQUE (NOUVEAU v0.2.1)
configurations_serveurs.json

# 📝 FICHIERS DE TESTS
test_*.py
*_test.py
.pytest_cache/
.coverage
htmlcov/

# 🔐 CERTIFICATS ET CLÉS
*.pem
*.key
*.crt

# 📦 NODE MODULES (si applicable)
node_modules/

# 🗑️ FICHIERS SYSTÈME
.Trash-*/
*.lnk
