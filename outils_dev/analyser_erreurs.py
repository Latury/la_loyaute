# ══════════════════════════════════════════════════════════════════════
# ║
# ║  🔍 LA LOYAUTÉ - ANALYSEUR D'ERREURS PYLANCE
# ║
# ║  Script avancé pour détecter les erreurs de type Pylance/Pyright
# ║  Analyse TOUS les fichiers Python du projet
# ║
# ║  📄 Fichier : outils_dev/analyser_erreurs.py
# ║  👤 Auteur : Latury
# ║  📅 Date : 07/01/2026
# ║  🔖 Version : 0.5.0 - Nouveau Design (Bleu Intense + Orange)
# ║
# ══════════════════════════════════════════════════════════════════════

import os
import ast
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Set, Any, Tuple

# ══════════════════════════════════════════════════════════════════════
# ║ ⚙️ CONFIGURATION
# ══════════════════════════════════════════════════════════════════════

DOSSIER_RACINE = Path(__file__).parent.parent.absolute()
DOSSIER_RAPPORTS = Path(__file__).parent / "rapports"

DOSSIERS_IGNORES = {
    '__pycache__', '.venv', 'venv', 'env', 'ENV', '.env', '.git', '.github',
    '.vscode', '.idea', 'node_modules', '.mypy_cache', '.pytest_cache',
    '.tox', '.hypothesis', 'build', 'dist', 'site', '*.egg-info', '.eggs',
    'htmlcov', '.coverage', '.cache', 'logs', 'temp'
}

FICHIERS_IGNORES = {
    '.DS_Store', 'Thumbs.db', '__init__.pyc', '.gitignore', '.gitattributes'
}

# ══════════════════════════════════════════════════════════════════════
# ║ 🎨 COULEURS CONSOLE (NOUVEAU DESIGN v0.5.0)
# ══════════════════════════════════════════════════════════════════════

class Couleurs:
    """Palette de couleurs optimisée : Bleu intense + Orange"""

    # 🔵 BLEU INTENSE - Cadres et titres principaux
    BLEU_INTENSE = '\033[1;34m'      # Bleu intense pour cadres ╔═╗
    BLEU_TITRE = '\033[1;36m'        # Cyan bold pour sous-titres

    # 🟠 ORANGE - Informations en cours / progression
    ORANGE = '\033[38;5;208m'        # Orange pour les infos en cours
    ORANGE_CLAIR = '\033[38;5;214m'  # Orange clair pour nuances

    # ✅ AUTRES COULEURS
    VERT = '\033[92m'                # Vert pour succès
    JAUNE = '\033[93m'               # Jaune pour warnings
    ROUGE = '\033[91m'               # Rouge pour erreurs
    GRIS = '\033[90m'                # Gris pour secondaire

    # 🎨 STYLES
    ENDC = '\033[0m'                 # Reset
    BOLD = '\033[1m'                 # Gras
    DIM = '\033[2m'                  # Atténué
    UNDERLINE = '\033[4m'            # Souligné

# ══════════════════════════════════════════════════════════════════════
# ║ 🔍 CLASSE : ANALYSEUR AST AVANCÉ
# ══════════════════════════════════════════════════════════════════════

class AnalyseurErreurs(ast.NodeVisitor):
    """Analyseur AST pour détecter les erreurs de type Pylance"""

    def __init__(self, fichier: str):
        self.fichier = fichier
        self.erreurs: List[Dict[str, Any]] = []
        self.variables_definies: Set[str] = set()
        self.imports: Set[str] = set()
        self.fonctions_definies: Set[str] = set()
        self.classes_definies: Set[str] = set()
        self.dans_fonction = False
        self.dans_classe = False
        self.contexte_variables: List[Set[str]] = [set()]
        self.builtins = set(dir(__builtins__))

    def visit_Import(self, node: ast.Import) -> None:
        """Enregistre les imports simples"""
        for alias in node.names:
            nom = alias.asname if alias.asname else alias.name
            self.imports.add(nom)
            self.imports.add(alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Enregistre les imports from"""
        if node.module:
            self.imports.add(node.module.split('.')[0])
        for alias in node.names:
            nom = alias.asname if alias.asname else alias.name
            if nom != '*':
                self.imports.add(nom)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Enregistre les définitions de fonctions"""
        self.fonctions_definies.add(node.name)
        ancien_etat = self.dans_fonction
        self.dans_fonction = True
        self.contexte_variables.append(set())

        for arg in node.args.args:
            self.variables_definies.add(arg.arg)
            self.contexte_variables[-1].add(arg.arg)

        self.generic_visit(node)
        self.contexte_variables.pop()
        self.dans_fonction = ancien_etat

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Enregistre les fonctions async"""
        self.fonctions_definies.add(node.name)
        ancien_etat = self.dans_fonction
        self.dans_fonction = True
        self.contexte_variables.append(set())

        for arg in node.args.args:
            self.variables_definies.add(arg.arg)
            self.contexte_variables[-1].add(arg.arg)

        self.generic_visit(node)
        self.contexte_variables.pop()
        self.dans_fonction = ancien_etat

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Enregistre les définitions de classes"""
        self.classes_definies.add(node.name)
        ancien_etat = self.dans_classe
        self.dans_classe = True
        self.contexte_variables.append(set())
        self.generic_visit(node)
        self.contexte_variables.pop()
        self.dans_classe = ancien_etat

    def visit_Assign(self, node: ast.Assign) -> None:
        """Enregistre les assignations de variables"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables_definies.add(target.id)
                if self.contexte_variables:
                    self.contexte_variables[-1].add(target.id)
            elif isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.variables_definies.add(elt.id)
                        if self.contexte_variables:
                            self.contexte_variables[-1].add(elt.id)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Enregistre les assignations avec annotations"""
        if isinstance(node.target, ast.Name):
            self.variables_definies.add(node.target.id)
            if self.contexte_variables:
                self.contexte_variables[-1].add(node.target.id)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """Enregistre les variables de boucle for"""
        if isinstance(node.target, ast.Name):
            self.variables_definies.add(node.target.id)
            if self.contexte_variables:
                self.contexte_variables[-1].add(node.target.id)
        elif isinstance(node.target, ast.Tuple):
            for elt in node.target.elts:
                if isinstance(elt, ast.Name):
                    self.variables_definies.add(elt.id)
                    if self.contexte_variables:
                        self.contexte_variables[-1].add(elt.id)
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        """Enregistre les variables de contexte with"""
        for item in node.items:
            if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                self.variables_definies.add(item.optional_vars.id)
                if self.contexte_variables:
                    self.contexte_variables[-1].add(item.optional_vars.id)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Enregistre les variables d'exception"""
        if node.name:
            self.variables_definies.add(node.name)
            if self.contexte_variables:
                self.contexte_variables[-1].add(node.name)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        """Vérifie l'utilisation de variables"""
        if isinstance(node.ctx, ast.Load):
            nom = node.id
            if (nom not in self.variables_definies and
                nom not in self.imports and
                nom not in self.fonctions_definies and
                nom not in self.classes_definies and
                nom not in self.builtins and
                not nom.startswith('_')):
                self.erreurs.append({
                    "ligne": node.lineno,
                    "colonne": node.col_offset,
                    "type": "reportUndefinedVariable",
                    "severite": "erreur",
                    "message": f"« {nom} » n'est pas défini"
                })
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Vérifie les accès aux attributs"""
        if isinstance(node.value, ast.Name):
            noms_suspects = {
                "guild", "message", "interaction", "channel",
                "author", "member", "user", "role", "voice_state"
            }
            if node.value.id in noms_suspects:
                self.erreurs.append({
                    "ligne": node.lineno,
                    "colonne": node.col_offset,
                    "type": "reportOptionalMemberAccess",
                    "severite": "avertissement",
                    "message": f"« {node.attr} » peut ne pas exister si « {node.value.id} » est None"
                })
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Vérifie les appels de fonction"""
        if isinstance(node.func, ast.Name):
            nom_fonction = node.func.id
            if (nom_fonction not in self.fonctions_definies and
                nom_fonction not in self.imports and
                nom_fonction not in self.builtins and
                not nom_fonction.startswith('_')):
                self.erreurs.append({
                    "ligne": node.lineno,
                    "colonne": node.col_offset,
                    "type": "reportUndefinedVariable",
                    "severite": "erreur",
                    "message": f"« {nom_fonction} » n'est pas défini"
                })
        self.generic_visit(node)

# ══════════════════════════════════════════════════════════════════════
# ║ 📁 FONCTIONS UTILITAIRES
# ══════════════════════════════════════════════════════════════════════

def obtenir_fichiers_python() -> List[Path]:
    """Récupère TOUS les fichiers Python du projet (sauf .venv)"""
    fichiers: List[Path] = []
    print(f"{Couleurs.ORANGE}🔍 Scan récursif du projet...{Couleurs.ENDC}")

    for root, dirs, files in os.walk(DOSSIER_RACINE):
        dirs[:] = [d for d in dirs if d not in DOSSIERS_IGNORES and not d.startswith('.')]

        for file in files:
            if file.endswith('.py') and file not in FICHIERS_IGNORES:
                chemin_complet = Path(root) / file
                fichiers.append(chemin_complet)

    return sorted(fichiers)

def analyser_fichier(chemin_fichier: Path) -> List[Dict[str, Any]]:
    """Analyse un fichier Python avec AST"""
    erreurs: List[Dict[str, Any]] = []

    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
    except Exception as e:
        erreurs.append({
            "ligne": 0,
            "colonne": 0,
            "type": "Erreur de lecture",
            "severite": "erreur",
            "message": f"Impossible de lire le fichier : {e}"
        })
        return erreurs

    try:
        arbre = ast.parse(contenu, filename=str(chemin_fichier))
    except SyntaxError as e:
        erreurs.append({
            "ligne": e.lineno or 0,
            "colonne": e.offset or 0,
            "type": "SyntaxError",
            "severite": "erreur",
            "message": f"Erreur de syntaxe : {e.msg}"
        })
        return erreurs
    except Exception as e:
        erreurs.append({
            "ligne": 0,
            "colonne": 0,
            "type": "Erreur de parsing",
            "severite": "erreur",
            "message": f"Impossible de parser : {e}"
        })
        return erreurs

    try:
        analyseur = AnalyseurErreurs(str(chemin_fichier))
        analyseur.visit(arbre)
        erreurs.extend(analyseur.erreurs)
    except Exception as e:
        erreurs.append({
            "ligne": 0,
            "colonne": 0,
            "type": "Erreur d'analyse",
            "severite": "erreur",
            "message": f"Erreur lors de l'analyse AST : {e}"
        })

    try:
        erreurs_imports = analyser_imports_manquants(contenu, str(chemin_fichier))
        erreurs.extend(erreurs_imports)
    except Exception:
        pass

    try:
        erreurs_parentheses = verifier_parentheses(contenu, str(chemin_fichier))
        erreurs.extend(erreurs_parentheses)
    except Exception:
        pass

    return erreurs

def analyser_imports_manquants(contenu: str, fichier: str) -> List[Dict[str, Any]]:
    """Détecte les imports manquants"""
    erreurs: List[Dict[str, Any]] = []
    lignes = contenu.split('\n')

    modules_connus: Dict[str, List[str]] = {
        'discord': ['Embed', 'Interaction', 'Member', 'User', 'Guild', 'TextChannel',
                   'VoiceChannel', 'Role', 'Permissions', 'Color', 'File'],
        'discord.ui': ['View', 'Button', 'Select', 'Modal', 'TextInput'],
        'discord.ext.commands': ['Cog', 'Bot', 'Context'],
        'discord.app_commands': ['CommandTree', 'command', 'describe'],
        'datetime': ['datetime', 'timedelta'],
        'typing': ['Optional', 'List', 'Dict', 'Any', 'Union', 'Tuple'],
        'pathlib': ['Path'],
        'json': ['loads', 'dumps'],
        'os': ['path', 'walk', 'makedirs'],
    }

    imports_presents: Set[str] = set()
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne.startswith('import ') or ligne.startswith('from '):
            match = re.findall(r'import\s+(\w+)', ligne)
            imports_presents.update(match)

    for num_ligne, ligne in enumerate(lignes, 1):
        if ligne.strip().startswith('#'):
            continue

        for module, classes in modules_connus.items():
            for classe in classes:
                if re.search(r'\b' + classe + r'\b', ligne) and classe not in imports_presents:
                    if not re.search(r'["\'].*\b' + classe + r'\b.*["\']', ligne):
                        erreurs.append({
                            "ligne": num_ligne,
                            "colonne": ligne.find(classe),
                            "type": "reportAttributeAccessIssue",
                            "severite": "avertissement",
                            "message": f"« {classe} » utilisé sans import (devrait venir de {module})"
                        })
                        break

    return erreurs

def verifier_parentheses(contenu: str, fichier: str) -> List[Dict[str, Any]]:
    """Détecte les parenthèses non fermées"""
    erreurs: List[Dict[str, Any]] = []
    lignes = contenu.split('\n')
    pile: List[Tuple[str, int, int]] = []
    correspondances = {'(': ')', '[': ']', '{': '}'}

    for num_ligne, ligne in enumerate(lignes, 1):
        ligne_clean = re.sub(r'["\'].*?["\']', '', ligne)
        ligne_clean = re.sub(r'#.*$', '', ligne_clean)

        for col, char in enumerate(ligne_clean):
            if char in '([{':
                pile.append((char, num_ligne, col))
            elif char in ')]}':
                if not pile:
                    erreurs.append({
                        "ligne": num_ligne,
                        "colonne": col,
                        "type": "SyntaxError",
                        "severite": "erreur",
                        "message": f"« {char} » fermante sans ouvrante correspondante"
                    })
                else:
                    ouvrante, ligne_ouvrante, col_ouvrante = pile.pop()
                    if correspondances[ouvrante] != char:
                        erreurs.append({
                            "ligne": num_ligne,
                            "colonne": col,
                            "type": "SyntaxError",
                            "severite": "erreur",
                            "message": f"« {char} » ne correspond pas à « {ouvrante} » (ligne {ligne_ouvrante})"
                        })

    for ouvrante, ligne, col in pile:
        erreurs.append({
            "ligne": ligne,
            "colonne": col,
            "type": "SyntaxError",
            "severite": "erreur",
            "message": f"« {ouvrante} » n'a pas été fermé"
        })

    return erreurs

# ══════════════════════════════════════════════════════════════════════
# ║ 📝 GÉNÉRATION DU RAPPORT
# ══════════════════════════════════════════════════════════════════════

def generer_rapport(resultats: List[Dict[str, Any]]) -> Tuple[str, int, int]:
    """Génère un rapport d'analyse"""
    DOSSIER_RAPPORTS.mkdir(exist_ok=True, parents=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_rapport = f"rapport_erreurs_{timestamp}.txt"
    chemin_rapport = DOSSIER_RAPPORTS / nom_rapport

    total_fichiers = len(resultats)
    total_erreurs = sum(len(r["erreurs"]) for r in resultats)
    fichiers_avec_erreurs = sum(1 for r in resultats if r["erreurs"])

    erreurs_par_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for resultat in resultats:
        for erreur in resultat["erreurs"]:
            type_erreur = erreur.get("type", "Autre")
            erreurs_par_type[type_erreur].append({
                "fichier": resultat["fichier"],
                "erreur": erreur
            })

    with open(chemin_rapport, 'w', encoding='utf-8') as f:
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("║  🔍 LA LOYAUTÉ - RAPPORT D'ANALYSE DES ERREURS".ljust(79) + "║\n")
        f.write("║  ⚡ Scan complet du projet (hors .venv)".ljust(79) + "║\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        f.write(f"📅 Date        : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write(f"🔖 Version     : 0.5.0 (Design Bleu Intense + Orange)\n")
        f.write(f"📁 Projet      : {DOSSIER_RACINE}\n\n")

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 📈 STATISTIQUES GÉNÉRALES".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")

        f.write(f"  📂 Fichiers Python analysés : {total_fichiers}\n")
        f.write(f"  ❌ Fichiers avec erreurs     : {fichiers_avec_erreurs}\n")
        f.write(f"  🔴 Total d'erreurs détectées : {total_erreurs}\n\n")

        if total_erreurs == 0:
            f.write("✅ Aucune erreur détectée ! Le code est propre.\n\n")
        else:
            f.write("┌" + "─" * 78 + "┐\n")
            f.write("│ 🔍 ERREURS PAR TYPE".ljust(79) + "│\n")
            f.write("└" + "─" * 78 + "┘\n\n")

            for type_err, liste_err in sorted(erreurs_par_type.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"  ▶️  {type_err} ({len(liste_err)} occurrence(s))\n\n")

                for item in liste_err[:10]:
                    fichier_str = item["fichier"]
                    erreur = item["erreur"]
                    ligne = erreur.get("ligne", "?")
                    colonne = erreur.get("colonne", "?")
                    severite = erreur.get("severite", "erreur")
                    message = erreur.get("message", "Pas de détails")

                    try:
                        fichier_relatif = Path(fichier_str).relative_to(DOSSIER_RACINE)
                    except Exception:
                        fichier_relatif = fichier_str

                    icone = "🔴" if severite == "erreur" else "⚠️"
                    f.write(f"      {icone} {fichier_relatif}\n")
                    f.write(f"         ⮑ Ligne {ligne}, Colonne {colonne}\n")
                    f.write(f"         💬 {message}\n\n")

                if len(liste_err) > 10:
                    f.write(f"      ... et {len(liste_err) - 10} autre(s)\n\n")

            f.write("┌" + "─" * 78 + "┐\n")
            f.write("│ 📋 DÉTAILS PAR FICHIER".ljust(79) + "│\n")
            f.write("└" + "─" * 78 + "┘\n")

            for resultat in resultats:
                fichier_str = resultat["fichier"]
                erreurs = resultat["erreurs"]

                if erreurs:
                    try:
                        fichier_relatif = Path(fichier_str).relative_to(DOSSIER_RACINE)
                    except Exception:
                        fichier_relatif = fichier_str

                    f.write(f"\n  📄 {fichier_relatif} ({len(erreurs)} erreur(s))\n")
                    for err in erreurs:
                        ligne = err.get("ligne", "?")
                        type_err = err.get("type", "Autre")
                        severite = err.get("severite", "erreur")
                        message = err.get("message", "Pas de détails")
                        icone = "🔴" if severite == "erreur" else "⚠️"
                        f.write(f"     {icone} Ligne {ligne} [{type_err}] : {message}\n")

        f.write("\n╔" + "═" * 78 + "╗\n")
        f.write("║ 📄 Rapport généré par : analyser_erreurs.py v0.5.0".ljust(79) + "║\n")
        f.write(f"║ 📅 Date : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}".ljust(79) + "║\n")
        f.write("╚" + "═" * 78 + "╝\n")

    return str(chemin_rapport), total_erreurs, fichiers_avec_erreurs

# ══════════════════════════════════════════════════════════════════════
# ║ 🚀 FONCTION PRINCIPALE
# ══════════════════════════════════════════════════════════════════════

def main():
    """Fonction principale"""
    print(f"\n{Couleurs.BLEU_INTENSE}╔{'═' * 78}╗{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║{' ' * 78}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║  🔍 LA LOYAUTÉ - ANALYSEUR D'ERREURS PYLANCE{' ' * 33}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║  ⚡ Version 0.5.0 - Design Bleu Intense + Orange{' ' * 29}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║{' ' * 78}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}╚{'═' * 78}╝{Couleurs.ENDC}\n")

    print(f"{Couleurs.BLEU_TITRE}📁 Projet : {Couleurs.BOLD}{DOSSIER_RACINE}{Couleurs.ENDC}")

    fichiers = obtenir_fichiers_python()
    print(f"{Couleurs.VERT}✅ {len(fichiers)} fichier(s) Python trouvé(s)\n{Couleurs.ENDC}")

    resultats: List[Dict[str, Any]] = []
    for i, fichier in enumerate(fichiers, 1):
        try:
            fichier_relatif = fichier.relative_to(DOSSIER_RACINE)
        except Exception:
            fichier_relatif = fichier

        print(f"{Couleurs.ORANGE}🔍 [{i}/{len(fichiers)}] {fichier_relatif}...{Couleurs.ENDC}", end='')

        erreurs = analyser_fichier(fichier)
        resultats.append({
            "fichier": str(fichier),
            "erreurs": erreurs
        })

        if erreurs:
            print(f" {Couleurs.JAUNE}⚠️  {len(erreurs)} erreur(s){Couleurs.ENDC}")
        else:
            print(f" {Couleurs.VERT}✅{Couleurs.ENDC}")

    print(f"\n{Couleurs.ORANGE}📝 Génération du rapport...{Couleurs.ENDC}")
    chemin_rapport, total_erreurs, fichiers_erreurs = generer_rapport(resultats)

    print(f"\n{Couleurs.BLEU_INTENSE}╔{'═' * 78}╗{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}║  📊 RÉSUMÉ FINAL{' ' * 62}║{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}╚{'═' * 78}╝{Couleurs.ENDC}\n")

    print(f"  📁 Fichiers Python analysés : {Couleurs.BOLD}{len(fichiers)}{Couleurs.ENDC}")
    print(f"  ❌ Fichiers avec erreurs     : {Couleurs.BOLD}{fichiers_erreurs}{Couleurs.ENDC}")
    print(f"  🔴 Total d'erreurs           : {Couleurs.BOLD}{total_erreurs}{Couleurs.ENDC}\n")

    if total_erreurs == 0:
        print(f"{Couleurs.VERT}✅ Aucune erreur détectée ! Le code est propre.{Couleurs.ENDC}\n")
    else:
        print(f"{Couleurs.JAUNE}⚠️  Des erreurs ont été détectées.{Couleurs.ENDC}\n")

    print(f"📄 Rapport généré : {Couleurs.BLEU_TITRE}{chemin_rapport}{Couleurs.ENDC}\n")

# ══════════════════════════════════════════════════════════════════════
# ║ 🎯 POINT D'ENTRÉE
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Couleurs.JAUNE}🛑 Analyse interrompue par l'utilisateur{Couleurs.ENDC}\n")
    except Exception as e:
        print(f"\n\n{Couleurs.ROUGE}❌ Erreur fatale : {e}{Couleurs.ENDC}\n")
        import traceback
        traceback.print_exc()
