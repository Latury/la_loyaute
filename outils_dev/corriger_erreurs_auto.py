# ══════════════════════════════════════════════════════════════════════
# ║
# ║  🔧 LA LOYAUTÉ - CORRECTEUR AUTOMATIQUE D'ERREURS
# ║
# ║  Corrige automatiquement les erreurs détectées dans le projet
# ║  - Supprime les imports en double
# ║  - Ajoute les fonctions setup() manquantes
# ║  - Crée des backups avant modification
# ║
# ║  📄 Fichier : outils_dev/corriger_erreurs_auto.py
# ║  👤 Auteur : Latury
# ║  📅 Date : 13/01/2026
# ║  🔖 Version : 1.0.0
# ║
# ══════════════════════════════════════════════════════════════════════

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Any

# ══════════════════════════════════════════════════════════════════════
# ║ 📁 CONFIGURATION
# ══════════════════════════════════════════════════════════════════════

DOSSIER_RACINE = Path(__file__).parent.parent
DOSSIER_BACKUPS = DOSSIER_RACINE / "outils_dev" / "backups"
DOSSIER_RAPPORTS = DOSSIER_RACINE / "outils_dev" / "rapports"

# Créer les dossiers si nécessaire
DOSSIER_BACKUPS.mkdir(exist_ok=True, parents=True)
DOSSIER_RAPPORTS.mkdir(exist_ok=True, parents=True)

# ══════════════════════════════════════════════════════════════════════
# ║ 🎨 COULEURS
# ══════════════════════════════════════════════════════════════════════

class Couleurs:
    """Couleurs pour l'affichage terminal"""
    BLEU_INTENSE = "\033[1;34m"
    BLEU_TITRE = "\033[1;36m"
    ORANGE = "\033[38;5;208m"
    VERT = "\033[92m"
    JAUNE = "\033[93m"
    ROUGE = "\033[91m"
    GRIS = "\033[90m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

# ══════════════════════════════════════════════════════════════════════
# ║ 🔧 FONCTIONS DE CORRECTION
# ══════════════════════════════════════════════════════════════════════

def creer_backup(fichier: Path) -> Path:
    """Crée un backup horodaté du fichier"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_backup = f"{fichier.stem}_backup_{timestamp}{fichier.suffix}"
    chemin_backup = DOSSIER_BACKUPS / nom_backup

    shutil.copy2(fichier, chemin_backup)
    return chemin_backup


def supprimer_imports_doubles(contenu: str) -> Tuple[str, int]:
    """Supprime les imports en double"""
    lignes = contenu.split('\n')
    imports_vus = set()
    nouvelles_lignes = []
    nb_supprimes = 0

    for ligne in lignes:
        ligne_stripped = ligne.strip()

        # Si c'est un import
        if ligne_stripped.startswith(('import ', 'from ')):
            # Normaliser pour comparaison (enlever espaces multiples)
            import_normalise = ' '.join(ligne_stripped.split())

            if import_normalise not in imports_vus:
                imports_vus.add(import_normalise)
                nouvelles_lignes.append(ligne)
            else:
                # Import en double trouvé
                nb_supprimes += 1
                print(f"      {Couleurs.ORANGE}🗑️  Supprimé : {ligne_stripped[:60]}...{Couleurs.ENDC}")
        else:
            nouvelles_lignes.append(ligne)

    return '\n'.join(nouvelles_lignes), nb_supprimes


def ajouter_fonction_setup(contenu: str, nom_classe: str) -> Tuple[str, bool]:
    """Ajoute la fonction setup() si elle manque"""
    # Vérifier si setup() existe déjà
    if re.search(r'async\s+def\s+setup\s*\(', contenu):
        return contenu, False

    # Vérifier si la classe existe
    if f"class {nom_classe}" not in contenu:
        return contenu, False

    # Ajouter la fonction setup à la fin
    setup_function = f'''

# ══════════════════════════════════════════════════════════════════════
# ║ ⚙️  SETUP DU COG
# ══════════════════════════════════════════════════════════════════════

async def setup(bot):
    """Charge le cog {nom_classe}"""
    await bot.add_cog({nom_classe}(bot))
'''

    contenu_modifie = contenu.rstrip() + setup_function
    return contenu_modifie, True


def corriger_fichier(chemin_fichier: Path) -> Dict[str, Any]:
    """Corrige un fichier Python"""
    resultat = {
        'fichier': str(chemin_fichier.relative_to(DOSSIER_RACINE)),
        'imports_supprimes': 0,
        'setup_ajoute': False,
        'backup_cree': False,
        'erreur': None
    }

    try:
        # Lire le contenu
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu_original = f.read()

        contenu_modifie = contenu_original
        modifications = False

        # 1. Supprimer les imports en double
        contenu_modifie, nb_imports = supprimer_imports_doubles(contenu_modifie)
        if nb_imports > 0:
            resultat['imports_supprimes'] = nb_imports
            modifications = True

        # 2. Ajouter setup() si c'est un fichier de commandes/événements
        nom_fichier = chemin_fichier.stem
        if chemin_fichier.parent.name in ['commandes', 'evenements']:
            # Détecter le nom de la classe
            match = re.search(r'class\s+(\w+)\s*\(', contenu_modifie)
            if match:
                nom_classe = match.group(1)
                contenu_modifie, setup_ajoute = ajouter_fonction_setup(contenu_modifie, nom_classe)
                if setup_ajoute:
                    resultat['setup_ajoute'] = True
                    modifications = True

        # Sauvegarder seulement si des modifications ont été faites
        if modifications:
            # Créer un backup
            backup = creer_backup(chemin_fichier)
            resultat['backup_cree'] = True

            # Écrire le fichier corrigé
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                f.write(contenu_modifie)

        return resultat

    except Exception as e:
        resultat['erreur'] = str(e)
        return resultat


# ══════════════════════════════════════════════════════════════════════
# ║ 📊 ANALYSE ET CORRECTION DU PROJET
# ══════════════════════════════════════════════════════════════════════

def obtenir_fichiers_python() -> List[Path]:
    """Récupère tous les fichiers Python du projet (sauf .venv)"""
    fichiers = []
    dossiers_ignores = {'.venv', 'venv', '__pycache__', '.git', 'build', 'dist'}

    for root, dirs, files in os.walk(DOSSIER_RACINE):
        # Filtrer les dossiers à ignorer
        dirs[:] = [d for d in dirs if d not in dossiers_ignores]

        for file in files:
            if file.endswith('.py'):
                fichiers.append(Path(root) / file)

    return sorted(fichiers)


def generer_rapport(resultats: List[Dict]) -> Path:
    """Génère un rapport des corrections"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fichier_rapport = DOSSIER_RAPPORTS / f"rapport_corrections_{timestamp}.txt"

    total_fichiers = len(resultats)
    fichiers_corriges = sum(1 for r in resultats if r['imports_supprimes'] > 0 or r['setup_ajoute'])
    total_imports = sum(r['imports_supprimes'] for r in resultats)
    total_setup = sum(1 for r in resultats if r['setup_ajoute'])
    erreurs = [r for r in resultats if r['erreur']]

    with open(fichier_rapport, 'w', encoding='utf-8') as f:
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("║  🔧 RAPPORT DE CORRECTION AUTOMATIQUE - LA LOYAUTÉ".ljust(79) + "║\n")
        f.write("║  ⚡ Version 1.0.0".ljust(79) + "║\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")

        f.write(f"📅 Date        : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write(f"📁 Projet      : {DOSSIER_RACINE}\n")
        f.write(f"📊 Fichiers    : {total_fichiers} analysés\n\n")

        f.write("┌" + "─" * 78 + "┐\n")
        f.write("│ 📈 STATISTIQUES".ljust(79) + "│\n")
        f.write("└" + "─" * 78 + "┘\n\n")
        f.write(f"  ✅ Fichiers corrigés         : {fichiers_corriges}\n")
        f.write(f"  🗑️  Imports en double supprimés : {total_imports}\n")
        f.write(f"  ➕ Fonctions setup() ajoutées : {total_setup}\n")
        f.write(f"  ❌ Erreurs rencontrées       : {len(erreurs)}\n\n")

        if fichiers_corriges > 0:
            f.write("╔" + "═" * 78 + "╗\n\n")
            f.write("┌" + "─" * 78 + "┐\n")
            f.write("│ 📋 DÉTAIL DES CORRECTIONS".ljust(79) + "│\n")
            f.write("└" + "─" * 78 + "┘\n\n")

            for r in resultats:
                if r['imports_supprimes'] > 0 or r['setup_ajoute']:
                    f.write(f"  📄 {r['fichier']}\n")
                    if r['imports_supprimes'] > 0:
                        f.write(f"     🗑️  {r['imports_supprimes']} import(s) en double supprimé(s)\n")
                    if r['setup_ajoute']:
                        f.write(f"     ➕ Fonction setup() ajoutée\n")
                    f.write(f"\n")

        if erreurs:
            f.write("╔" + "═" * 78 + "╗\n\n")
            f.write("┌" + "─" * 78 + "┐\n")
            f.write("│ ❌ ERREURS".ljust(79) + "│\n")
            f.write("└" + "─" * 78 + "┘\n\n")

            for r in erreurs:
                f.write(f"  📄 {r['fichier']}\n")
                f.write(f"     ❌ {r['erreur']}\n\n")

        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║ 📄 Rapport généré par : corriger_erreurs_auto.py v1.0.0".ljust(79) + "║\n")
        f.write(f"║ 📅 Date : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}".ljust(79) + "║\n")
        f.write("╚" + "═" * 78 + "╝\n")

    return fichier_rapport


# ══════════════════════════════════════════════════════════════════════
# ║ 🚀 FONCTION PRINCIPALE
# ══════════════════════════════════════════════════════════════════════

def main():
    """Fonction principale"""
    print(f"\n{Couleurs.BLEU_INTENSE}{'═' * 80}{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}{'═' * 80}{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}  🔧 CORRECTEUR AUTOMATIQUE D'ERREURS - LA LOYAUTÉ{'  ' * 17}{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}  ⚡ Version 1.0.0{'  ' * 32}{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}{'═' * 80}{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}{'═' * 80}{Couleurs.ENDC}\n")

    print(f"{Couleurs.BLEU_TITRE}📁 Projet : {Couleurs.BOLD}{DOSSIER_RACINE}{Couleurs.ENDC}\n")

    # Récupérer les fichiers Python
    print(f"{Couleurs.ORANGE}🔍 Scan du projet...{Couleurs.ENDC}")
    fichiers = obtenir_fichiers_python()
    print(f"{Couleurs.VERT}✅ {len(fichiers)} fichier(s) Python trouvé(s){Couleurs.ENDC}\n")

    # Demander confirmation
    print(f"{Couleurs.JAUNE}⚠️  ATTENTION :{Couleurs.ENDC}")
    print(f"{Couleurs.JAUNE}   • Des backups seront créés dans : {DOSSIER_BACKUPS}{Couleurs.ENDC}")
    print(f"{Couleurs.JAUNE}   • Les fichiers seront modifiés directement{Couleurs.ENDC}\n")

    reponse = input(f"{Couleurs.BLEU_TITRE}Continuer ? (o/n) : {Couleurs.ENDC}").lower()

    if reponse != 'o':
        print(f"\n{Couleurs.ROUGE}❌ Correction annulée{Couleurs.ENDC}\n")
        return

    print(f"\n{Couleurs.ORANGE}🔧 Correction en cours...{Couleurs.ENDC}\n")

    # Corriger chaque fichier
    resultats = []
    for i, fichier in enumerate(fichiers, 1):
        fichier_relatif = fichier.relative_to(DOSSIER_RACINE)
        print(f"{Couleurs.ORANGE}[{i}/{len(fichiers)}] {fichier_relatif}...{Couleurs.ENDC}")

        resultat = corriger_fichier(fichier)
        resultats.append(resultat)

        if resultat['imports_supprimes'] > 0:
            print(f"      {Couleurs.VERT}✅ {resultat['imports_supprimes']} import(s) en double supprimé(s){Couleurs.ENDC}")
        if resultat['setup_ajoute']:
            print(f"      {Couleurs.VERT}✅ Fonction setup() ajoutée{Couleurs.ENDC}")
        if resultat['erreur']:
            print(f"      {Couleurs.ROUGE}❌ Erreur : {resultat['erreur']}{Couleurs.ENDC}")
        if not resultat['imports_supprimes'] and not resultat['setup_ajoute'] and not resultat['erreur']:
            print(f"      {Couleurs.GRIS}✓ Aucune correction nécessaire{Couleurs.ENDC}")

    # Générer le rapport
    print(f"\n{Couleurs.ORANGE}📝 Génération du rapport...{Couleurs.ENDC}")
    fichier_rapport = generer_rapport(resultats)

    # Statistiques finales
    fichiers_corriges = sum(1 for r in resultats if r['imports_supprimes'] > 0 or r['setup_ajoute'])
    total_imports = sum(r['imports_supprimes'] for r in resultats)
    total_setup = sum(1 for r in resultats if r['setup_ajoute'])

    print(f"\n{Couleurs.BLEU_INTENSE}{'═' * 80}{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}  📊 RÉSUMÉ FINAL{'  ' * 33}{Couleurs.ENDC}")
    print(f"{Couleurs.BLEU_INTENSE}{'═' * 80}{Couleurs.ENDC}\n")

    print(f"  📁 Fichiers analysés           : {Couleurs.BOLD}{len(fichiers)}{Couleurs.ENDC}")
    print(f"  ✅ Fichiers corrigés           : {Couleurs.BOLD}{fichiers_corriges}{Couleurs.ENDC}")
    print(f"  🗑️  Imports en double supprimés : {Couleurs.BOLD}{total_imports}{Couleurs.ENDC}")
    print(f"  ➕ Fonctions setup() ajoutées   : {Couleurs.BOLD}{total_setup}{Couleurs.ENDC}\n")

    if fichiers_corriges > 0:
        print(f"{Couleurs.VERT}✅ Corrections terminées avec succès !{Couleurs.ENDC}")
    else:
        print(f"{Couleurs.VERT}✅ Aucune correction nécessaire{Couleurs.ENDC}")

    print(f"\n📄 Rapport détaillé : {Couleurs.BLEU_TITRE}{fichier_rapport}{Couleurs.ENDC}")
    print(f"💾 Backups sauvegardés dans : {Couleurs.BLEU_TITRE}{DOSSIER_BACKUPS}{Couleurs.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Couleurs.JAUNE}⚠️  Correction interrompue par l'utilisateur{Couleurs.ENDC}\n")
    except Exception as e:
        print(f"\n\n{Couleurs.ROUGE}❌ Erreur critique : {e}{Couleurs.ENDC}\n")
        import traceback
        traceback.print_exc()
