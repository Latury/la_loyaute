# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🔍 LA LOYAUTÉ - DÉTECTEUR DE DOUBLONS
# ║
# ║ Script d'analyse complète pour détecter les doublons de code
# ║ Développé par Latury
# ║ Version : 0.2.1
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import os
import hashlib
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# ═══════════════════════════════════════════════════════════════════════════════
# ║ ⚙️ CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Dossier racine du projet
DOSSIER_RACINE = Path(__file__).parent.parent.absolute()

# Dossier de sortie pour les rapports
DOSSIER_RAPPORTS = Path(__file__).parent / "rapports"

# Extensions à analyser
EXTENSIONS_CODE = ['.py', '.json', '.md', '.txt', '.yml', '.yaml', '.toml']

# ⛔ DOSSIERS À IGNORER
DOSSIERS_IGNORES = [
    '__pycache__',
    '.venv',
    'venv',
    'env',
    '.git',
    '.vscode',
    '.idea',
    'node_modules',
    '.mypy_cache',
    '.pytest_cache',
    'build',
    'dist',
    '*.egg-info',
    'outils_dev'  # ← NOUVEAU : ignore le dossier des outils
]

# ⛔ FICHIERS À IGNORER
FICHIERS_IGNORES = [
    '.DS_Store',
    'Thumbs.db',
    '.gitignore',
    '.gitattributes',
    'detecter_doublons.py',  # Ne pas s'analyser soi-même
    'analyser_erreurs.py'
]

# Patterns de fichiers temporaires
PATTERNS_TEMPORAIRES = [
    '.backup',
    '.bak',
    '.tmp',
    '.temp',
    '.old',
    '~',
    '.swp',
    '.swo',
    '.orig'
]


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎨 COULEURS CONSOLE
# ═══════════════════════════════════════════════════════════════════════════════

class Couleurs:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🛠️ FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def calculer_hash_fichier(chemin_fichier):
    """Calcule le hash MD5 d'un fichier"""
    try:
        hash_md5 = hashlib.md5()
        with open(chemin_fichier, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return None


def lire_fichier_texte(chemin_fichier):
    """Lit un fichier texte avec gestion des encodages"""
    encodages = ['utf-8', 'latin-1', 'cp1252']
    for encoding in encodages:
        try:
            with open(chemin_fichier, 'r', encoding=encoding) as f:
                return f.read()
        except:
            continue
    return None


def extraire_definitions_python(contenu):
    """Extrait les fonctions et classes Python"""
    if not contenu:
        return [], []

    fonctions = re.findall(r'^\s*def\s+(\w+)\s*\(', contenu, re.MULTILINE)
    classes = re.findall(r'^\s*class\s+(\w+)\s*[\(:]', contenu, re.MULTILINE)

    return fonctions, classes


def est_fichier_temporaire(nom_fichier):
    """Vérifie si un fichier est temporaire"""
    nom_lower = nom_fichier.lower()
    return any(pattern in nom_lower for pattern in PATTERNS_TEMPORAIRES)


def formater_taille(taille_octets):
    """Formate une taille en format lisible"""
    for unite in ['o', 'Ko', 'Mo', 'Go']:
        if taille_octets < 1024.0:
            return f"{taille_octets:.2f} {unite}"
        taille_octets /= 1024.0
    return f"{taille_octets:.2f} To"


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔍 ANALYSE DU PROJET
# ═══════════════════════════════════════════════════════════════════════════════

def analyser_projet(dossier_racine):
    """Analyse complète du projet"""
    print(f"\n{Couleurs.HEADER}{'═' * 80}{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║ 🔍 ANALYSE DU PROJET LA LOYAUTÉ{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}{'═' * 80}{Couleurs.ENDC}\n")

    print(f"{Couleurs.OKCYAN}📁 Dossier analysé : {dossier_racine}{Couleurs.ENDC}")
    print(f"{Couleurs.OKCYAN}⏳ Analyse en cours...{Couleurs.ENDC}\n")

    resultats = {
        'tous_fichiers': [],
        'fichiers_par_nom': defaultdict(list),
        'fichiers_par_hash': defaultdict(list),
        'fichiers_temporaires': [],
        'fonctions_par_nom': defaultdict(list),
        'classes_par_nom': defaultdict(list),
        'taille_totale': 0,
        'stats': {
            'fichiers_python': 0,
            'fichiers_json': 0,
            'fichiers_md': 0,
            'autres': 0
        }
    }

    compteur_fichiers = 0

    for root, dirs, files in os.walk(dossier_racine):
        # Filtrer les dossiers à ignorer
        dirs[:] = [d for d in dirs if d not in DOSSIERS_IGNORES and not d.startswith('.')]

        for file in files:
            if file in FICHIERS_IGNORES or file.startswith('.'):
                continue

            chemin_complet = os.path.join(root, file)
            chemin_relatif = os.path.relpath(chemin_complet, dossier_racine)

            compteur_fichiers += 1
            if compteur_fichiers % 10 == 0:
                print(f"{Couleurs.OKCYAN} 📂 {compteur_fichiers} fichiers analysés...{Couleurs.ENDC}", end='\r')

            try:
                taille = os.path.getsize(chemin_complet)
            except:
                taille = 0

            resultats['taille_totale'] += taille

            resultats['tous_fichiers'].append({
                'chemin': chemin_relatif,
                'nom': file,
                'taille': taille
            })

            # Statistiques par extension
            ext = os.path.splitext(file)[1].lower()
            if ext == '.py':
                resultats['stats']['fichiers_python'] += 1
            elif ext == '.json':
                resultats['stats']['fichiers_json'] += 1
            elif ext == '.md':
                resultats['stats']['fichiers_md'] += 1
            else:
                resultats['stats']['autres'] += 1

            # Détecter fichiers temporaires
            if est_fichier_temporaire(file):
                resultats['fichiers_temporaires'].append(chemin_relatif)

            # Grouper par nom
            resultats['fichiers_par_nom'][file].append(chemin_relatif)

            # Analyse approfondie pour fichiers de code
            if ext in EXTENSIONS_CODE:
                hash_fichier = calculer_hash_fichier(chemin_complet)
                if hash_fichier:
                    resultats['fichiers_par_hash'][hash_fichier].append(chemin_relatif)

                # Analyse Python
                if ext == '.py':
                    contenu = lire_fichier_texte(chemin_complet)
                    if contenu:
                        fonctions, classes = extraire_definitions_python(contenu)

                        for fonction in fonctions:
                            resultats['fonctions_par_nom'][fonction].append(chemin_relatif)

                        for classe in classes:
                            resultats['classes_par_nom'][classe].append(chemin_relatif)

    print(f"\n{Couleurs.OKGREEN}✅ Analyse terminée : {compteur_fichiers} fichiers{Couleurs.ENDC}")
    print(f"{Couleurs.OKGREEN}💾 Taille totale : {formater_taille(resultats['taille_totale'])}{Couleurs.ENDC}\n")

    return resultats


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📊 GÉNÉRATION DU RAPPORT
# ═══════════════════════════════════════════════════════════════════════════════

def generer_rapport(resultats, fichier_sortie):
    """Génère le rapport détaillé"""
    print(f"{Couleurs.OKCYAN}📝 Génération du rapport...{Couleurs.ENDC}")

    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        # EN-TÊTE
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("║" + "🔍 RAPPORT D'ANALYSE DE DOUBLONS - LA LOYAUTÉ".center(78) + "║\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        f.write(f"📅 Date : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write(f"📁 Projet : {DOSSIER_RACINE}\n")
        f.write(f"📊 Fichiers analysés : {len(resultats['tous_fichiers'])}\n")
        f.write(f"💾 Taille totale : {formater_taille(resultats['taille_totale'])}\n\n")

        f.write("📈 Statistiques :\n")
        f.write(f" - Fichiers Python : {resultats['stats']['fichiers_python']}\n")
        f.write(f" - Fichiers JSON : {resultats['stats']['fichiers_json']}\n")
        f.write(f" - Fichiers Markdown : {resultats['stats']['fichiers_md']}\n")
        f.write(f" - Autres : {resultats['stats']['autres']}\n\n")
        f.write("═" * 80 + "\n\n")

        # SECTION 1 : FICHIERS AVEC MÊME NOM
        doublons_nom = {
            nom: chemins
            for nom, chemins in resultats['fichiers_par_nom'].items()
            if len(chemins) > 1
        }

        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║ 🔴 SECTION 1 : FICHIERS AVEC LE MÊME NOM" + " " * 34 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        if doublons_nom:
            f.write(f"⚠️ {len(doublons_nom)} nom(s) en double !\n\n")
            for nom, chemins in sorted(doublons_nom.items()):
                f.write(f"┌─ 📄 {nom}\n")
                f.write(f"│ Occurrences : {len(chemins)}\n")
                for chemin in sorted(chemins):
                    f.write(f"│ ➜ {chemin}\n")
                f.write(f"└─\n\n")
        else:
            f.write("✅ Aucun fichier avec le même nom\n\n")

        f.write("═" * 80 + "\n\n")

        # SECTION 2 : FICHIERS IDENTIQUES
        doublons_hash = {
            hash_val: chemins
            for hash_val, chemins in resultats['fichiers_par_hash'].items()
            if len(chemins) > 1
        }

        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║ 🔴 SECTION 2 : FICHIERS IDENTIQUES (MÊME CONTENU)" + " " * 24 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        if doublons_hash:
            f.write(f"🚨 {len(doublons_hash)} groupe(s) de fichiers identiques !\n\n")
            for i, (hash_val, chemins) in enumerate(sorted(doublons_hash.items()), 1):
                f.write(f"┌─ Groupe #{i}\n")
                f.write(f"│ Hash : {hash_val}\n")
                f.write(f"│ Copies : {len(chemins)}\n")
                for chemin in sorted(chemins):
                    f.write(f"│ ➜ {chemin}\n")
                f.write(f"└─ 🔴 ACTION : Supprimer les doublons !\n\n")
        else:
            f.write("✅ Aucun fichier identique\n\n")

        f.write("═" * 80 + "\n\n")

        # SECTION 3 : FICHIERS TEMPORAIRES
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║ ⚠️ SECTION 3 : FICHIERS TEMPORAIRES" + " " * 39 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        if resultats['fichiers_temporaires']:
            f.write(f"⚠️ {len(resultats['fichiers_temporaires'])} fichier(s) temporaire(s) :\n\n")
            for fichier in sorted(resultats['fichiers_temporaires']):
                f.write(f" ➜ {fichier}\n")
            f.write("\n")
        else:
            f.write("✅ Aucun fichier temporaire\n\n")

        f.write("═" * 80 + "\n\n")

        # SECTION 4 : FONCTIONS DUPLIQUÉES
        fonctions_dupliquees = {
            nom: fichiers
            for nom, fichiers in resultats['fonctions_par_nom'].items()
            if len(fichiers) > 1
        }

        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║ 🟡 SECTION 4 : FONCTIONS DUPLIQUÉES" + " " * 39 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        if fonctions_dupliquees:
            f.write(f"ℹ️ {len(fonctions_dupliquees)} fonction(s) dupliquée(s)\n\n")
            for nom, fichiers in sorted(list(fonctions_dupliquees.items())[:30]):
                f.write(f"┌─ def {nom}()\n")
                f.write(f"│ Dans {len(fichiers)} fichier(s) :\n")
                for fichier in sorted(fichiers):
                    f.write(f"│ ➜ {fichier}\n")
                f.write(f"└─\n\n")
            if len(fonctions_dupliquees) > 30:
                f.write(f"... et {len(fonctions_dupliquees) - 30} autre(s)\n\n")
        else:
            f.write("✅ Aucune fonction dupliquée\n\n")

        f.write("═" * 80 + "\n\n")

        # SECTION 5 : CLASSES DUPLIQUÉES
        classes_dupliquees = {
            nom: fichiers
            for nom, fichiers in resultats['classes_par_nom'].items()
            if len(fichiers) > 1
        }

        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║ 🟠 SECTION 5 : CLASSES DUPLIQUÉES" + " " * 41 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        if classes_dupliquees:
            f.write(f"⚠️ {len(classes_dupliquees)} classe(s) dupliquée(s)\n\n")
            for nom, fichiers in sorted(classes_dupliquees.items()):
                f.write(f"┌─ class {nom}\n")
                f.write(f"│ Dans {len(fichiers)} fichier(s) :\n")
                for fichier in sorted(fichiers):
                    f.write(f"│ ➜ {fichier}\n")
                f.write(f"└─\n\n")
        else:
            f.write("✅ Aucune classe dupliquée\n\n")

        f.write("═" * 80 + "\n\n")

        # RÉSUMÉ
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║ 📊 RÉSUMÉ FINAL" + " " * 60 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        problemes = 0
        if doublons_nom:
            f.write(f" 🔴 Fichiers en double (nom) : {len(doublons_nom)}\n")
            problemes += 1
        else:
            f.write(f" ✅ Fichiers en double (nom) : 0\n")

        if doublons_hash:
            f.write(f" 🔴 Fichiers identiques : {len(doublons_hash)}\n")
            problemes += 1
        else:
            f.write(f" ✅ Fichiers identiques : 0\n")

        if resultats['fichiers_temporaires']:
            f.write(f" ⚠️ Fichiers temporaires : {len(resultats['fichiers_temporaires'])}\n")
        else:
            f.write(f" ✅ Fichiers temporaires : 0\n")

        f.write("\n" + "─" * 80 + "\n\n")

        if problemes > 0:
            f.write("🚨 VERDICT : PROBLÈMES DÉTECTÉS !\n")
            f.write(" ACTION : Consultez les sections ci-dessus\n\n")
        else:
            f.write("✅ VERDICT : PROJET PROPRE !\n")
            f.write(" Aucun doublon détecté\n\n")

        f.write("═" * 80 + "\n")
        f.write(f"📄 Rapport généré par : detecter_doublons.py v0.2.1\n")
        f.write(f"📅 Date : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write("═" * 80 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🚀 FONCTION PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal"""
    print(f"\n{Couleurs.HEADER}╔{'═' * 78}╗{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║{' ' * 78}║{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║{'🔍 DÉTECTEUR DE DOUBLONS - LA LOYAUTÉ'.center(78)}║{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║{'Version 0.2.1'.center(78)}║{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║{' ' * 78}║{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}╚{'═' * 78}╝{Couleurs.ENDC}")

    # Créer le dossier de rapports
    DOSSIER_RAPPORTS.mkdir(exist_ok=True)

    # Analyser
    try:
        resultats = analyser_projet(DOSSIER_RACINE)
    except Exception as e:
        print(f"\n{Couleurs.FAIL}❌ Erreur lors de l'analyse : {e}{Couleurs.ENDC}")
        return

    # Générer le rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fichier_rapport = DOSSIER_RAPPORTS / f"rapport_doublons_{timestamp}.txt"

    try:
        generer_rapport(resultats, fichier_rapport)
    except Exception as e:
        print(f"\n{Couleurs.FAIL}❌ Erreur génération rapport : {e}{Couleurs.ENDC}")
        return

    # Résumé
    print(f"\n{Couleurs.HEADER}{'═' * 80}{Couleurs.ENDC}")
    print(f"{Couleurs.OKGREEN}✅ ANALYSE TERMINÉE AVEC SUCCÈS{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}{'═' * 80}{Couleurs.ENDC}\n")
    print(f"📄 Rapport : {Couleurs.OKBLUE}{fichier_rapport}{Couleurs.ENDC}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Couleurs.WARNING}🛑 Analyse interrompue{Couleurs.ENDC}\n")
    except Exception as e:
        print(f"\n\n{Couleurs.FAIL}❌ Erreur critique : {e}{Couleurs.ENDC}\n")
