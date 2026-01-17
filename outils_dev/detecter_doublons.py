# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🔍 LA LOYAUTÉ - DÉTECTEUR DE DOUBLONS
# ║ Outils Dev | Script d'analyse complète pour détecter les doublons de code
# ║ Développé par Latury
# ║ Version 0.5.0
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🔍 FICHIER : detecter_doublons.py
# ║ 📦 MODULE : outils_dev
# ║ 📝 DESCRIPTION : Script d'analyse complète pour détecter les doublons de code
# ║ 👤 AUTEUR : Latury
# ║ 📅 DATE : 15 janvier 2026
# ║ 🔖 VERSION : 0.5.0
# ║
# ╚═══════════════════════════════════════════════════════════════════════════════

import logging
import os
import hashlib
import re
import ast
import traceback
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any, Optional
from couleurs_terminal import Couleurs

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ ⚙️ CONFIGURATION
# ║ 📝 Chemins, extensions et paramètres d'analyse
# ╚═══════════════════════════════════════════════════════════════════════════════

DOSSIER_RACINE = Path(__file__).parent.parent.absolute()
DOSSIER_RAPPORTS = Path(__file__).parent / "rapports"
EXTENSIONS_CODE = {'.py', '.json', '.md', '.txt', '.yml', '.yaml', '.toml', '.ini', '.cfg'}

DOSSIERS_IGNORES = {
    '__pycache__', '.venv', 'venv', 'env', 'ENV', '.env', '.git', '.github',
    '.vscode', '.idea', 'node_modules', '.mypy_cache', '.pytest_cache',
    '.tox', '.hypothesis', 'build', 'dist', 'site', '*.egg-info', '.eggs',
    'htmlcov', '.coverage', '.cache', 'logs', 'temp', '.tmp'
}

FICHIERS_IGNORES = {
    '.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes', '__init__.pyc'
}

PATTERNS_TEMPORAIRES = [
    '.backup', '.bak', '.tmp', '.temp', '.old', '~', '.swp', '.swo', '.orig', '.cache'
]

SEUIL_SIMILARITE = 80

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🛠️ FONCTIONS UTILITAIRES
# ║ 📝 Fonctions de support pour l'analyse
# ╚═══════════════════════════════════════════════════════════════════════════════

def calculer_hash_fichier(chemin_fichier: Path) -> str:
    """Calcule le hash MD5 d'un fichier"""
    try:
        hash_md5 = hashlib.md5()
        with open(chemin_fichier, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return ""

def calculer_hash_contenu_normalise(contenu: str) -> str:
    """Calcule le hash du contenu normalisé (sans espaces/commentaires)"""
    try:
        contenu_clean = re.sub(r'#.*$', '', contenu, flags=re.MULTILINE)
        contenu_clean = re.sub(r'""".*?"""', '', contenu_clean, flags=re.DOTALL)
        contenu_clean = re.sub(r"'''.*?'''", '', contenu_clean, flags=re.DOTALL)
        contenu_clean = re.sub(r'\s+', ' ', contenu_clean)
        contenu_clean = '\n'.join([line.strip() for line in contenu_clean.split('\n') if line.strip()])
        return hashlib.md5(contenu_clean.encode()).hexdigest()
    except Exception:
        return hashlib.md5(contenu.encode()).hexdigest()

def lire_fichier_texte(chemin_fichier: Path) -> str:
    """Lit un fichier texte avec gestion des encodages"""
    encodages = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    for encoding in encodages:
        try:
            with open(chemin_fichier, 'r', encoding=encoding) as f:
                return f.read()
        except Exception:
            continue
    return ""

def extraire_definitions_python(contenu: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """Extrait les fonctions et classes Python avec leur contenu"""
    if not contenu:
        return [], []

    fonctions: List[Tuple[str, str]] = []
    classes: List[Tuple[str, str]] = []

    try:
        arbre = ast.parse(contenu)
        lignes = contenu.split('\n')

        for node in ast.walk(arbre):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    debut = node.lineno
                    fin = node.end_lineno
                    if fin and debut <= fin:
                        code_fonction = '\n'.join(lignes[debut-1:fin])
                        fonctions.append((node.name, code_fonction))

            elif isinstance(node, ast.ClassDef):
                if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    debut = node.lineno
                    fin = node.end_lineno
                    if fin and debut <= fin:
                        code_classe = '\n'.join(lignes[debut-1:fin])
                        classes.append((node.name, code_classe))

    except SyntaxError:
        try:
            fonctions_regex = re.findall(
                r'((?:async\s+)?def\s+(\w+)\s*\([^)]*\):.*?)(?=\n(?:async\s+)?def\s|\nclass\s|\Z)',
                contenu,
                re.DOTALL
            )
            fonctions = [(m[1], m[0]) for m in fonctions_regex]

            classes_regex = re.findall(
                r'(class\s+(\w+)\s*[\(:][^:]*:.*?)(?=\nclass\s|\n(?:async\s+)?def\s|\Z)',
                contenu,
                re.DOTALL
            )
            classes = [(m[1], m[0]) for m in classes_regex]
        except Exception:
            pass

    return fonctions, classes

def calculer_similarite(texte1: str, texte2: str) -> float:
    """Calcule la similarité entre deux textes (coefficient de Jaccard)"""
    try:
        t1 = set(texte1.lower().split())
        t2 = set(texte2.lower().split())

        if not t1 or not t2:
            return 0.0

        intersection = len(t1 & t2)
        union = len(t1 | t2)

        return (intersection / union) * 100 if union > 0 else 0.0
    except Exception:
        return 0.0

def est_fichier_temporaire(nom_fichier: str) -> bool:
    """Vérifie si un fichier est temporaire"""
    nom_lower = nom_fichier.lower()
    return any(pattern in nom_lower for pattern in PATTERNS_TEMPORAIRES)

def formater_taille(taille_octets: int) -> str:
    """Formate une taille en format lisible"""
    taille: float = float(taille_octets)
    for unite in ['o', 'Ko', 'Mo', 'Go']:
        if taille < 1024.0:
            return f"{taille:.2f} {unite}"
        taille /= 1024.0
    return f"{taille:.2f} To"

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🔍 FONCTION 01 – analyser_projet
# ║ 📊 Analyse complète du projet pour détecter les doublons
# ╚═══════════════════════════════════════════════════════════════════════════════

def analyser_projet(dossier_racine: Path) -> Dict:
    """Analyse complète du projet"""
    print(f"\n{Couleurs.BLEU_INTENSE}╔{'═' * 78}╗{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║{' ' * 78}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║  🔍 ANALYSE DU PROJET LA LOYAUTÉ{' ' * 44}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║  🔋 Version 0.5.0 - Design Bleu Intense + Orange{' ' * 29}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║{' ' * 78}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}╚{'═' * 78}╝{Couleurs.ENDC}\n")

    print(f"{Couleurs.BLEU_TITRE}📁 Dossier analysé : {Couleurs.BOLD}{dossier_racine}{Couleurs.ENDC}")
    print(f"{Couleurs.ORANGE}⏳ Scan récursif en cours...{Couleurs.ENDC}\n")

    resultats: Dict[str, Any] = {
        'tous_fichiers': [],
        'fichiers_par_nom': defaultdict(list),
        'fichiers_par_hash': defaultdict(list),
        'fichiers_par_hash_normalise': defaultdict(list),
        'fichiers_temporaires': [],
        'fonctions_par_nom': defaultdict(list),
        'fonctions_par_code': defaultdict(list),
        'classes_par_nom': defaultdict(list),
        'classes_par_code': defaultdict(list),
        'fonctions_similaires': [],
        'taille_totale': 0,
        'stats': {
            'fichiers_python': 0,
            'fichiers_json': 0,
            'fichiers_md': 0,
            'fichiers_config': 0,
            'autres': 0
        },
        'dossiers_analyses': set()
    }

    compteur_fichiers = 0

    for root, dirs, files in os.walk(dossier_racine):
        dirs[:] = [d for d in dirs if d not in DOSSIERS_IGNORES and not d.startswith('.')]

        dossier_relatif = Path(root).relative_to(dossier_racine)
        if str(dossier_relatif) != '.':
            resultats['dossiers_analyses'].add(str(dossier_relatif))

        for file in files:
            if file in FICHIERS_IGNORES or file.startswith('.'):
                continue

            chemin_complet = Path(root) / file
            chemin_relatif = chemin_complet.relative_to(dossier_racine)

            compteur_fichiers += 1
            if compteur_fichiers % 5 == 0:
                print(f"{Couleurs.ORANGE}  📂 {compteur_fichiers} fichiers analysés...{Couleurs.ENDC}", end='\r')

            try:
                taille = chemin_complet.stat().st_size
            except Exception:
                taille = 0

            resultats['taille_totale'] += taille

            resultats['tous_fichiers'].append({
                'chemin': str(chemin_relatif),
                'nom': file,
                'taille': taille
            })

            ext = chemin_complet.suffix.lower()
            if ext == '.py':
                resultats['stats']['fichiers_python'] += 1
            elif ext == '.json':
                resultats['stats']['fichiers_json'] += 1
            elif ext == '.md':
                resultats['stats']['fichiers_md'] += 1
            elif ext in {'.yml', '.yaml', '.toml', '.ini', '.cfg'}:
                resultats['stats']['fichiers_config'] += 1
            else:
                resultats['stats']['autres'] += 1

            if est_fichier_temporaire(file):
                resultats['fichiers_temporaires'].append(str(chemin_relatif))

            resultats['fichiers_par_nom'][file].append(str(chemin_relatif))

            if ext in EXTENSIONS_CODE:
                hash_fichier = calculer_hash_fichier(chemin_complet)
                if hash_fichier:
                    resultats['fichiers_par_hash'][hash_fichier].append(str(chemin_relatif))

                contenu = lire_fichier_texte(chemin_complet)
                if contenu:
                    hash_normalise = calculer_hash_contenu_normalise(contenu)
                    resultats['fichiers_par_hash_normalise'][hash_normalise].append(str(chemin_relatif))

                    if ext == '.py':
                        fonctions, classes = extraire_definitions_python(contenu)

                        for nom_fonction, code_fonction in fonctions:
                            resultats['fonctions_par_nom'][nom_fonction].append({
                                'fichier': str(chemin_relatif),
                                'code': code_fonction
                            })

                            hash_fonction = calculer_hash_contenu_normalise(code_fonction)
                            resultats['fonctions_par_code'][hash_fonction].append({
                                'fichier': str(chemin_relatif),
                                'nom': nom_fonction,
                                'code': code_fonction
                            })

                        for nom_classe, code_classe in classes:
                            resultats['classes_par_nom'][nom_classe].append({
                                'fichier': str(chemin_relatif),
                                'code': code_classe
                            })

                            hash_classe = calculer_hash_contenu_normalise(code_classe)
                            resultats['classes_par_code'][hash_classe].append({
                                'fichier': str(chemin_relatif),
                                'nom': nom_classe,
                                'code': code_classe
                            })

    print(f"\n{Couleurs.ORANGE}🔍 Analyse des similarités entre fonctions...{Couleurs.ENDC}")
    fonctions_liste = list(resultats['fonctions_par_nom'].items())

    comparaisons = 0
    total_comparaisons = len(fonctions_liste) * (len(fonctions_liste) - 1) // 2

    for i, (nom1, occurrences1) in enumerate(fonctions_liste):
        for j, (nom2, occurrences2) in enumerate(fonctions_liste[i+1:], i+1):
            comparaisons += 1
            if comparaisons % 100 == 0:
                print(f"{Couleurs.ORANGE}  🔄 {comparaisons}/{total_comparaisons} comparaisons...{Couleurs.ENDC}", end='\r')

            if nom1 != nom2:
                for occ1 in occurrences1:
                    for occ2 in occurrences2:
                        similarite = calculer_similarite(occ1['code'], occ2['code'])
                        if similarite >= SEUIL_SIMILARITE:
                            resultats['fonctions_similaires'].append({
                                'fonction1': nom1,
                                'fichier1': occ1['fichier'],
                                'fonction2': nom2,
                                'fichier2': occ2['fichier'],
                                'similarite': similarite
                            })

    print(f"\n{Couleurs.VERT}✅ Analyse terminée : {compteur_fichiers} fichiers analysés{Couleurs.ENDC}")
    print(f"{Couleurs.VERT}💾 Taille totale : {formater_taille(resultats['taille_totale'])}{Couleurs.ENDC}")
    print(f"{Couleurs.VERT}📁 Dossiers analysés : {len(resultats['dossiers_analyses'])}{Couleurs.ENDC}\n")

    return resultats

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 📊 FONCTION 02 – generer_rapport
# ║ 📋 Génération du rapport détaillé d'analyse
# ╚═══════════════════════════════════════════════════════════════════════════════

def generer_rapport(resultats: Dict, fichier_sortie: Path) -> int:
    """Génère le rapport détaillé"""
    print(f"{Couleurs.ORANGE}📝 Génération du rapport détaillé...{Couleurs.ENDC}")

    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("║  🔍 RAPPORT D'ANALYSE DE DOUBLONS - LA LOYAUTÉ".ljust(79) + "║\n")
        f.write("║  🔋 Version 0.5.0 - Design Bleu Intense + Orange".ljust(79) + "║\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        f.write(f"📅 Date        : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write(f"📁 Projet      : {DOSSIER_RACINE}\n")
        f.write(f"📊 Fichiers    : {len(resultats['tous_fichiers'])} analysés\n")
        f.write(f"📂 Dossiers    : {len(resultats['dossiers_analyses'])} analysés\n")
        f.write(f"💾 Taille      : {formater_taille(resultats['taille_totale'])}\n\n")

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 📈 STATISTIQUES PAR TYPE".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")
        f.write(f"  • Fichiers Python (.py)          : {resultats['stats']['fichiers_python']}\n")
        f.write(f"  • Fichiers JSON (.json)          : {resultats['stats']['fichiers_json']}\n")
        f.write(f"  • Fichiers Markdown (.md)        : {resultats['stats']['fichiers_md']}\n")
        f.write(f"  • Fichiers Config (.yml/.toml)   : {resultats['stats']['fichiers_config']}\n")
        f.write(f"  • Autres fichiers                : {resultats['stats']['autres']}\n\n")

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 📂 DOSSIERS ANALYSÉS".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")
        for dossier in sorted(resultats['dossiers_analyses'])[:15]:
            f.write(f"  • {dossier}\n")
        if len(resultats['dossiers_analyses']) > 15:
            f.write(f"  ... et {len(resultats['dossiers_analyses']) - 15} autre(s)\n")
        f.write("\n")

        f.write("╔" + "═" * 78 + "╗\n\n")

        doublons_nom: Dict[str, List[str]] = {
            nom: chemins
            for nom, chemins in resultats['fichiers_par_nom'].items()
            if len(chemins) > 1
        }

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 🔴 SECTION 1 : FICHIERS AVEC LE MÊME NOM".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        if doublons_nom:
            f.write(f"⚠️  {len(doublons_nom)} nom(s) en double détecté(s) !\n\n")
            for nom, chemins in sorted(doublons_nom.items()):
                f.write(f"  ┌─ 📄 {nom}\n")
                f.write(f"  │  Occurrences : {len(chemins)}\n")
                for chemin in sorted(chemins):
                    f.write(f"  │  ➜ {chemin}\n")
                f.write(f"  └─\n\n")
        else:
            f.write("✅ Aucun fichier avec le même nom\n\n")

        f.write("╔" + "═" * 78 + "╗\n\n")

        doublons_hash: Dict[str, List[str]] = {
            hash_val: chemins
            for hash_val, chemins in resultats['fichiers_par_hash'].items()
            if len(chemins) > 1
        }

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 🔴 SECTION 2 : FICHIERS IDENTIQUES (CONTENU EXACT)".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        if doublons_hash:
            f.write(f"🚨 {len(doublons_hash)} groupe(s) de fichiers identiques détecté(s) !\n\n")
            for i, (hash_val, chemins) in enumerate(sorted(doublons_hash.items()), 1):
                f.write(f"  ┌─ Groupe #{i}\n")
                f.write(f"  │  Hash MD5 : {hash_val}\n")
                f.write(f"  │  Copies   : {len(chemins)}\n")
                for chemin in sorted(chemins):
                    f.write(f"  │  ➜ {chemin}\n")
                f.write(f"  └─ 🔴 ACTION : Supprimer les doublons !\n\n")
        else:
            f.write("✅ Aucun fichier identique\n\n")

        f.write("╔" + "═" * 78 + "╗\n\n")

        doublons_normalise: Dict[str, List[str]] = {
            hash_val: chemins
            for hash_val, chemins in resultats['fichiers_par_hash_normalise'].items()
            if len(chemins) > 1 and hash_val not in doublons_hash
        }

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 🟡 SECTION 3 : FICHIERS QUASI-IDENTIQUES".ljust(79) + "│\n")
        f.write("│ (Code identique avec différences d'espacement/commentaires)".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        if doublons_normalise:
            f.write(f"⚠️  {len(doublons_normalise)} groupe(s) quasi-identique(s) détecté(s)\n\n")
            for i, (hash_val, chemins) in enumerate(sorted(doublons_normalise.items())[:20], 1):
                f.write(f"  ┌─ Groupe #{i}\n")
                f.write(f"  │  Fichiers : {len(chemins)}\n")
                for chemin in sorted(chemins):
                    f.write(f"  │  ➜ {chemin}\n")
                f.write(f"  └─ 🟡 Vérifier si consolidation possible\n\n")

            if len(doublons_normalise) > 20:
                f.write(f"  ... et {len(doublons_normalise) - 20} autre(s) groupe(s)\n\n")
        else:
            f.write("✅ Aucun fichier quasi-identique\n\n")

        f.write("╔" + "═" * 78 + "╗\n\n")

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ ⚠️  SECTION 4 : FICHIERS TEMPORAIRES".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        if resultats['fichiers_temporaires']:
            f.write(f"⚠️  {len(resultats['fichiers_temporaires'])} fichier(s) temporaire(s) détecté(s) :\n\n")
            for fichier in sorted(resultats['fichiers_temporaires']):
                f.write(f"  ➜ {fichier}\n")
            f.write("\n🔴 ACTION : Supprimer ces fichiers\n\n")
        else:
            f.write("✅ Aucun fichier temporaire\n\n")

        f.write("╔" + "═" * 78 + "╗\n\n")

        fonctions_dupliquees_code: Dict[str, List[Dict[str, Any]]] = {
            hash_code: fonctions
            for hash_code, fonctions in resultats['fonctions_par_code'].items()
            if len(fonctions) > 1
        }

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 🔴 SECTION 5 : FONCTIONS DUPLIQUÉES (CODE IDENTIQUE)".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        if fonctions_dupliquees_code:
            f.write(f"🚨 {len(fonctions_dupliquees_code)} fonction(s) dupliquée(s) !\n\n")
            for i, (hash_code, fonctions) in enumerate(sorted(fonctions_dupliquees_code.items())[:25], 1):
                noms = set([f['nom'] for f in fonctions])
                f.write(f"  ┌─ Groupe #{i}\n")
                f.write(f"  │  Noms        : {', '.join(sorted(noms))}\n")
                f.write(f"  │  Occurrences : {len(fonctions)}\n")
                for func in fonctions:
                    f.write(f"  │  ➜ {func['fichier']} → def {func['nom']}()\n")
                f.write(f"  └─ 🔴 ACTION : Factoriser dans un module commun\n\n")

            if len(fonctions_dupliquees_code) > 25:
                f.write(f"  ... et {len(fonctions_dupliquees_code) - 25} autre(s) fonction(s)\n\n")
        else:
            f.write("✅ Aucune fonction dupliquée\n\n")

        f.write("╔" + "═" * 78 + "╗\n\n")

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 🟡 SECTION 6 : FONCTIONS SIMILAIRES".ljust(79) + "│\n")
        f.write(f"│ (Similarité ≥ {SEUIL_SIMILARITE}%)".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        if resultats['fonctions_similaires']:
            f.write(f"⚠️  {len(resultats['fonctions_similaires'])} paire(s) similaire(s) détectée(s)\n\n")
            for i, similaire in enumerate(sorted(resultats['fonctions_similaires'],
                                                key=lambda x: x['similarite'],
                                                reverse=True)[:20], 1):
                f.write(f"  ┌─ Paire #{i}\n")
                f.write(f"  │  Similarité : {similaire['similarite']:.1f}%\n")
                f.write(f"  │  ➜ {similaire['fichier1']} → def {similaire['fonction1']}()\n")
                f.write(f"  │  ➜ {similaire['fichier2']} → def {similaire['fonction2']}()\n")
                f.write(f"  └─ 🟡 Vérifier si factorisation possible\n\n")

            if len(resultats['fonctions_similaires']) > 20:
                f.write(f"  ... et {len(resultats['fonctions_similaires']) - 20} autre(s) paire(s)\n\n")
        else:
            f.write("✅ Aucune fonction similaire\n\n")

        f.write("╔" + "═" * 78 + "╗\n\n")

        classes_dupliquees_code: Dict[str, List[Dict[str, Any]]] = {
            hash_code: classes
            for hash_code, classes in resultats['classes_par_code'].items()
            if len(classes) > 1
        }

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 🟠 SECTION 7 : CLASSES DUPLIQUÉES".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        if classes_dupliquees_code:
            f.write(f"⚠️  {len(classes_dupliquees_code)} classe(s) dupliquée(s)\n\n")
            for i, (hash_code, classes) in enumerate(sorted(classes_dupliquees_code.items())[:15], 1):
                noms = set([c['nom'] for c in classes])
                f.write(f"  ┌─ Groupe #{i}\n")
                f.write(f"  │  Noms        : {', '.join(sorted(noms))}\n")
                f.write(f"  │  Occurrences : {len(classes)}\n")
                for classe in classes:
                    f.write(f"  │  ➜ {classe['fichier']} → class {classe['nom']}\n")
                f.write(f"  └─ 🟠 ACTION : Factoriser dans un module commun\n\n")

            if len(classes_dupliquees_code) > 15:
                f.write(f"  ... et {len(classes_dupliquees_code) - 15} autre(s) classe(s)\n\n")
        else:
            f.write("✅ Aucune classe dupliquée\n\n")

        f.write("╔" + "═" * 78 + "╗\n\n")

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 📊 RÉSUMÉ FINAL".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        problemes = 0

        if doublons_nom:
            f.write(f"  🔴 Fichiers en double (nom)     : {len(doublons_nom)}\n")
            problemes += len(doublons_nom)
        else:
            f.write(f"  ✅ Fichiers en double (nom)     : 0\n")

        if doublons_hash:
            f.write(f"  🔴 Fichiers identiques          : {len(doublons_hash)}\n")
            problemes += len(doublons_hash)
        else:
            f.write(f"  ✅ Fichiers identiques          : 0\n")

        if doublons_normalise:
            f.write(f"  🟡 Fichiers quasi-identiques    : {len(doublons_normalise)}\n")
        else:
            f.write(f"  ✅ Fichiers quasi-identiques    : 0\n")

        if resultats['fichiers_temporaires']:
            f.write(f"  ⚠️  Fichiers temporaires         : {len(resultats['fichiers_temporaires'])}\n")
        else:
            f.write(f"  ✅ Fichiers temporaires         : 0\n")

        if fonctions_dupliquees_code:
            f.write(f"  🔴 Fonctions dupliquées         : {len(fonctions_dupliquees_code)}\n")
            problemes += len(fonctions_dupliquees_code)
        else:
            f.write(f"  ✅ Fonctions dupliquées         : 0\n")

        if resultats['fonctions_similaires']:
            f.write(f"  🟡 Fonctions similaires         : {len(resultats['fonctions_similaires'])}\n")
        else:
            f.write(f"  ✅ Fonctions similaires         : 0\n")

        if classes_dupliquees_code:
            f.write(f"  🟠 Classes dupliquées           : {len(classes_dupliquees_code)}\n")
        else:
            f.write(f"  ✅ Classes dupliquées           : 0\n")

        f.write("\n" + "─" * 80 + "\n\n")

        if problemes > 0:
            f.write("🚨 VERDICT : PROBLÈMES CRITIQUES DÉTECTÉS !\n")
            f.write(f"   {problemes} problème(s) nécessitant une action\n")
            f.write("   ACTION : Consultez les sections ci-dessus\n\n")
        else:
            f.write("✅ VERDICT : PROJET PROPRE !\n")
            f.write("   Aucun doublon critique détecté\n\n")

        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║ 📄 Rapport généré par : detecter_doublons.py v0.5.0".ljust(79) + "║\n")
        f.write(f"║ 📅 Date : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}".ljust(79) + "║\n")
        f.write("╚" + "═" * 78 + "╝\n")

    return problemes

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🚀 FONCTION 03 – main
# ║ 📝 Point d'entrée principal du script
# ╚═══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal"""
    print(f"\n{Couleurs.BLEU_INTENSE}╔{'═' * 78}╗{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║{' ' * 78}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║  🔍 DÉTECTEUR DE DOUBLONS - LA LOYAUTÉ{' ' * 39}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║  🔋 Version 0.5.0 - Design Bleu Intense + Orange{' ' * 29}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║{' ' * 78}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}╚{'═' * 78}╝{Couleurs.ENDC}")

    DOSSIER_RAPPORTS.mkdir(exist_ok=True)

    try:
        resultats = analyser_projet(DOSSIER_RACINE)
    except Exception as e:
        print(f"\n{Couleurs.ROUGE}❌ Erreur lors de l'analyse : {e}{Couleurs.ENDC}")
        import traceback
        traceback.print_exc()
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fichier_rapport = DOSSIER_RAPPORTS / f"rapport_doublons_{timestamp}.txt"

    try:
        problemes = generer_rapport(resultats, fichier_rapport)
    except Exception as e:
        print(f"\n{Couleurs.ROUGE}❌ Erreur lors de l'analyse : {e}{Couleurs.ENDC}")
        logging.error(f"Erreur analyse doublons : {e}", exc_info=True)
    return

    print(f"\n{Couleurs.BLEU_INTENSE}{'┌' + '─' * 78 + '┐'}{Couleurs.ENDC}")
    if problemes > 0:
        print(f"{Couleurs.JAUNE}│ ⚠️  ANALYSE TERMINÉE - {problemes} PROBLÈME(S) DÉTECTÉ(S)".ljust(87) + f"│{Couleurs.ENDC}")
    else:
        print(f"{Couleurs.VERT}│ ✅ ANALYSE TERMINÉE - PROJET PROPRE".ljust(87) + f"│{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}{'└' + '─' * 78 + '┘'}{Couleurs.ENDC}\n")

    print(f"📄 Rapport complet : {Couleurs.BLEU_TITRE}{fichier_rapport}{Couleurs.ENDC}\n")

# ╔═══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 POINT D'ENTRÉE
# ║ 📝 Exécution du script
# ╚═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Couleurs.JAUNE}🛑 Analyse interrompue par l'utilisateur{Couleurs.ENDC}\n")
    except Exception as e:
        print(f"\n\n{Couleurs.ROUGE}❌ Erreur critique : {e}{Couleurs.ENDC}\n")
        traceback.print_exc()


# ╔══════════════════════════════════════════════════════════════════════════════
# ║
# ╚══════════════════════════════════════════════════════════════════════════════
