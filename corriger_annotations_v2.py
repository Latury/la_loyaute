#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction v2 des annotations Discord
Corrige: unsupported type annotation + missing type annotation
Solution: Met les annotations entre guillemets
"""

import os
import re
import shutil
from datetime import datetime

def creer_backup(fichier):
    """Crée une sauvegarde du fichier avant modification"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"{fichier}.backup_{timestamp}"
    shutil.copy2(fichier, backup)
    print(f"✅ Backup créé: {backup}")
    return backup

def corriger_annotations_fichier(fichier):
    """Corrige les annotations discord.Interaction en les mettant entre guillemets"""

    if not os.path.exists(fichier):
        print(f"❌ Fichier non trouvé: {fichier}")
        return False

    print(f"\n🔧 Correction de {fichier}...")
    creer_backup(fichier)

    with open(fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()

    modifications = 0

    # Pattern 1: interaction: "discord.Interaction" → interaction: "discord.Interaction"
    pattern1 = r'\binteraction:\s*discord\.Interaction\b'
    if re.search(pattern1, contenu):
        contenu = re.sub(pattern1, 'interaction: "discord.Interaction"', contenu)
        modifications += len(re.findall(pattern1, contenu))

    # Pattern 2: interaction: Interaction → interaction: "discord.Interaction"
    pattern2 = r'\binteraction:\s*Interaction\b'
    if re.search(pattern2, contenu):
        contenu = re.sub(pattern2, 'interaction: "discord.Interaction"', contenu)
        modifications += len(re.findall(pattern2, contenu))

    # Pattern 3: interaction) → interaction: "discord.Interaction")
    # Pour les cas où l'annotation a été complètement supprimée
    pattern3 = r'(def\s+\w+\([^)]*\binteraction)\s*\)'
    matches3 = re.findall(pattern3, contenu)
    if matches3:
        contenu = re.sub(pattern3, r'\1: "discord.Interaction")', contenu)
        modifications += len(matches3)

    # Pattern 4: interaction, → interaction: "discord.Interaction",
    pattern4 = r'(def\s+\w+\([^)]*\binteraction)\s*,'
    matches4 = re.findall(pattern4, contenu)
    if matches4:
        contenu = re.sub(pattern4, r'\1: "discord.Interaction",', contenu)
        modifications += len(matches4)

    with open(fichier, 'w', encoding='utf-8') as f:
        f.write(contenu)

    if modifications > 0:
        print(f"✅ {fichier} corrigé! (~{modifications} modifications)")
    else:
        print(f"ℹ️ {fichier} - Aucune modification nécessaire")

    return True

def nettoyer_cache():
    """Supprime tous les fichiers de cache Python"""
    print("\n🧹 Nettoyage du cache Python...")

    suppression_count = 0

    # Supprime les dossiers __pycache__
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            suppression_count += 1
            print(f"   🗑️ Supprimé: {pycache_path}")

    # Supprime les fichiers .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                os.remove(pyc_path)
                suppression_count += 1

    print(f"✅ Cache nettoyé! ({suppression_count} éléments supprimés)")

def main():
    """Fonction principale"""
    print("═" * 80)
    print("║" + " " * 78 + "║")
    print("║" + "🛠️ SCRIPT DE CORRECTION v2 - LA LOYAUTÉ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("═" * 80)

    # Vérification du répertoire
    if not os.path.exists('commandes') or not os.path.exists('principal.py'):
        print("\n❌ ERREUR: Ce script doit être exécuté à la racine du projet!")
        return

    print("\n🎯 Démarrage des corrections...\n")

    # Correction des fichiers avec annotations
    fichiers_a_corriger = [
        'commandes/commandes_admin.py',
        'commandes/commandes_configuration.py',
        'commandes/commandes_menu.py',
        'commandes/commandes_base.py',
    ]

    for fichier in fichiers_a_corriger:
        if os.path.exists(fichier):
            corriger_annotations_fichier(fichier)

    # Nettoyage du cache
    nettoyer_cache()

    print("\n" + "═" * 80)
    print("✅ TOUTES LES CORRECTIONS SONT TERMINÉES!")
    print("═" * 80)
    print("\n📝 Prochaines étapes:")
    print("   1. Relance le bot avec: python principal.py")
    print("   2. Les annotations sont maintenant entre guillemets")
    print("   3. Les backups sont disponibles si besoin (*.backup_*)")
    print()

if __name__ == "__main__":
    main()

