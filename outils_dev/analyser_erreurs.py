# ═══════════════════════════════════════════════════════════════════════════════
# ║
# ║ 🔍 LA LOYAUTÉ - ANALYSEUR D'ERREURS PYLANCE
# ║
# ║ Script pour analyser les erreurs Pylance/Pylint dans le projet
# ║ Développé par Latury
# ║ Version : 0.2.1
# ║
# ═══════════════════════════════════════════════════════════════════════════════

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ═══════════════════════════════════════════════════════════════════════════════
# ║ ⚙️ CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Dossiers à analyser
DOSSIERS_A_ANALYSER = [
    "commandes",
    "evenements",
    "noyau",
    "utilitaires"
]

# Fichiers Python à la racine
FICHIERS_RACINE = [
    "principal.py",
    "configuration.py"
]

# Extensions à analyser
EXTENSIONS = [".py"]

# Dossier de sortie des rapports
DOSSIER_RAPPORTS = "outils_dev/rapports"


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎨 CODES DE COULEURS CONSOLE
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
# ║ 📁 FONCTION 01 – Récupération des fichiers Python
# ║ Description : Récupère tous les fichiers .py du projet
# ═══════════════════════════════════════════════════════════════════════════════

def obtenir_fichiers_python():
    """Récupère tous les fichiers Python du projet"""
    fichiers = []

    # Fichiers à la racine
    for fichier in FICHIERS_RACINE:
        if os.path.exists(fichier):
            fichiers.append(fichier)

    # Fichiers dans les dossiers
    for dossier in DOSSIERS_A_ANALYSER:
        if os.path.exists(dossier):
            for root, dirs, files in os.walk(dossier):
                for file in files:
                    if file.endswith(".py"):
                        chemin = os.path.join(root, file)
                        fichiers.append(chemin)

    return sorted(fichiers)


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🔍 FONCTION 02 – Analyse avec Pylint
# ║ Description : Analyse un fichier avec Pylint
# ═══════════════════════════════════════════════════════════════════════════════

def analyser_avec_pylint(fichier):
    """Analyse un fichier avec Pylint"""
    try:
        resultat = subprocess.run(
            ["pylint", fichier, "--output-format=json"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if resultat.stdout:
            return json.loads(resultat.stdout)
        return []

    except subprocess.TimeoutExpired:
        print(f"{Couleurs.WARNING}⏱️  Timeout pour {fichier}{Couleurs.ENDC}")
        return []

    except FileNotFoundError:
        print(f"{Couleurs.WARNING}⚠️  Pylint non installé{Couleurs.ENDC}")
        return None

    except Exception as e:
        print(f"{Couleurs.FAIL}❌ Erreur Pylint pour {fichier}: {e}{Couleurs.ENDC}")
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📊 FONCTION 03 – Analyse manuelle des imports
# ║ Description : Vérifie les imports manquants
# ═══════════════════════════════════════════════════════════════════════════════

def analyser_imports(fichier):
    """Analyse les imports d'un fichier"""
    erreurs = []

    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            lignes = f.readlines()

        for num_ligne, ligne in enumerate(lignes, 1):
            ligne = ligne.strip()

            # Détection d'imports suspects
            if ligne.startswith("from") or ligne.startswith("import"):
                # Vérifier si c'est un import relatif mal formé
                if "from ." in ligne and ".." in ligne:
                    erreurs.append({
                        "ligne": num_ligne,
                        "type": "Import relatif suspect",
                        "message": ligne
                    })

    except Exception as e:
        print(f"{Couleurs.FAIL}❌ Erreur lecture {fichier}: {e}{Couleurs.ENDC}")

    return erreurs


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 📝 FONCTION 04 – Génération du rapport
# ║ Description : Génère un rapport détaillé
# ═══════════════════════════════════════════════════════════════════════════════

def generer_rapport(resultats):
    """Génère un rapport d'analyse"""

    # Créer le dossier de rapports si nécessaire
    os.makedirs(DOSSIER_RAPPORTS, exist_ok=True)

    # Nom du fichier de rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_rapport = f"rapport_erreurs_{timestamp}.txt"
    chemin_rapport = os.path.join(DOSSIER_RAPPORTS, nom_rapport)

    # Statistiques
    total_fichiers = len(resultats)
    total_erreurs = sum(len(r["erreurs"]) for r in resultats)
    fichiers_avec_erreurs = sum(1 for r in resultats if r["erreurs"])

    # Grouper par type d'erreur
    erreurs_par_type = defaultdict(list)
    for resultat in resultats:
        for erreur in resultat["erreurs"]:
            type_erreur = erreur.get("type", "Autre")
            erreurs_par_type[type_erreur].append({
                "fichier": resultat["fichier"],
                "erreur": erreur
            })

    # Écriture du rapport
    with open(chemin_rapport, 'w', encoding='utf-8') as f:
        f.write("═" * 80 + "\n")
        f.write("║\n")
        f.write("║ 🔍 LA LOYAUTÉ - RAPPORT D'ANALYSE DES ERREURS\n")
        f.write("║\n")
        f.write("═" * 80 + "\n\n")

        f.write(f"📅 Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"📊 Version : 0.2.1\n\n")

        f.write("─" * 80 + "\n")
        f.write("📈 STATISTIQUES GÉNÉRALES\n")
        f.write("─" * 80 + "\n\n")

        f.write(f"📁 Fichiers analysés : {total_fichiers}\n")
        f.write(f"❌ Fichiers avec erreurs : {fichiers_avec_erreurs}\n")
        f.write(f"🔴 Total d'erreurs : {total_erreurs}\n\n")

        if total_erreurs == 0:
            f.write("✅ Aucune erreur détectée ! Le code est propre.\n\n")
        else:
            f.write("─" * 80 + "\n")
            f.write("🔍 ERREURS PAR TYPE\n")
            f.write("─" * 80 + "\n\n")

            for type_err, liste_err in sorted(erreurs_par_type.items()):
                f.write(f"▶️  {type_err} ({len(liste_err)} occurrence(s))\n\n")

                for item in liste_err:
                    fichier = item["fichier"]
                    erreur = item["erreur"]
                    ligne = erreur.get("ligne", "?")
                    message = erreur.get("message", "Pas de détails")

                    f.write(f"   📄 Fichier : {fichier}\n")
                    f.write(f"   📍 Ligne {ligne}\n")
                    f.write(f"   💬 {message}\n\n")

        f.write("─" * 80 + "\n")
        f.write("📋 DÉTAILS PAR FICHIER\n")
        f.write("─" * 80 + "\n\n")

        for resultat in resultats:
            fichier = resultat["fichier"]
            erreurs = resultat["erreurs"]

            if erreurs:
                f.write(f"📄 {fichier} ({len(erreurs)} erreur(s))\n")
                for err in erreurs:
                    ligne = err.get("ligne", "?")
                    type_err = err.get("type", "Autre")
                    message = err.get("message", "Pas de détails")
                    f.write(f"   • Ligne {ligne} [{type_err}] : {message}\n")
                f.write("\n")

        f.write("═" * 80 + "\n")
        f.write("FIN DU RAPPORT\n")
        f.write("═" * 80 + "\n")

    return chemin_rapport, total_erreurs, fichiers_avec_erreurs


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🚀 FONCTION PRINCIPALE
# ║ Description : Lance l'analyse complète
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Fonction principale"""
    print(f"\n{Couleurs.HEADER}{'═' * 80}{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║ 🔍 LA LOYAUTÉ - ANALYSEUR D'ERREURS PYLANCE{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}{'═' * 80}{Couleurs.ENDC}\n")

    print(f"{Couleurs.OKCYAN}📁 Récupération des fichiers Python...{Couleurs.ENDC}")
    fichiers = obtenir_fichiers_python()
    print(f"{Couleurs.OKGREEN}✅ {len(fichiers)} fichier(s) trouvé(s)\n{Couleurs.ENDC}")

    resultats = []

    for i, fichier in enumerate(fichiers, 1):
        print(f"{Couleurs.OKCYAN}🔍 [{i}/{len(fichiers)}] Analyse de {fichier}...{Couleurs.ENDC}")

        erreurs = []

        # Analyse des imports
        erreurs_imports = analyser_imports(fichier)
        erreurs.extend(erreurs_imports)

        # Analyse Pylint (optionnel)
        erreurs_pylint = analyser_avec_pylint(fichier)
        if erreurs_pylint is not None and erreurs_pylint:
            for err in erreurs_pylint:
                erreurs.append({
                    "ligne": err.get("line", "?"),
                    "type": err.get("type", "Autre"),
                    "message": err.get("message", "Pas de détails")
                })

        resultats.append({
            "fichier": fichier,
            "erreurs": erreurs
        })

        if erreurs:
            print(f"{Couleurs.WARNING}   ⚠️  {len(erreurs)} erreur(s) détectée(s){Couleurs.ENDC}")
        else:
            print(f"{Couleurs.OKGREEN}   ✅ Aucune erreur{Couleurs.ENDC}")

    print(f"\n{Couleurs.OKCYAN}📝 Génération du rapport...{Couleurs.ENDC}")
    chemin_rapport, total_erreurs, fichiers_erreurs = generer_rapport(resultats)

    print(f"\n{Couleurs.HEADER}{'═' * 80}{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}║ 📊 RÉSUMÉ{Couleurs.ENDC}")
    print(f"{Couleurs.HEADER}{'═' * 80}{Couleurs.ENDC}\n")

    print(f"📁 Fichiers analysés : {len(fichiers)}")
    print(f"❌ Fichiers avec erreurs : {fichiers_erreurs}")
    print(f"🔴 Total d'erreurs : {total_erreurs}\n")

    if total_erreurs == 0:
        print(f"{Couleurs.OKGREEN}✅ Aucune erreur détectée ! Le code est propre.{Couleurs.ENDC}\n")
    else:
        print(f"{Couleurs.WARNING}⚠️  Des erreurs ont été détectées.{Couleurs.ENDC}\n")

    print(f"📄 Rapport généré : {Couleurs.OKBLUE}{chemin_rapport}{Couleurs.ENDC}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# ║ 🎯 POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Couleurs.WARNING}🛑 Analyse interrompue par l'utilisateur{Couleurs.ENDC}\n")
    except Exception as e:
        print(f"\n\n{Couleurs.FAIL}❌ Erreur fatale : {e}{Couleurs.ENDC}\n")
