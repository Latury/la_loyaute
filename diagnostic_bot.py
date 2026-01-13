import os
import re
from pathlib import Path

print("=" * 80)
print("🔍 DIAGNOSTIC COMPLET DU BOT LA LOYAUTÉ")
print("=" * 80)

# 1. Vérifier les imports __future__
print("\n📋 Vérification des imports 'from __future__ import annotations'...\n")

python_files = [
    "commandes/commandes_admin.py",
    "commandes/commandes_configuration.py",
    "commandes/commandes_menu.py",
    "commandes/commandes_base.py",
    "commandes/__init__.py",
    "utilitaires/embeds_interactifs.py",
    "evenements/__init__.py",
    "utilitaires/__init__.py",
    "noyau/__init__.py"
]

files_to_fix = []

for file_path in python_files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            has_future = 'from __future__ import annotations' in content
            print(f"{'✅' if has_future else '❌'} {file_path}: {'OK' if has_future else 'MANQUANT'}")
            if not has_future:
                files_to_fix.append(file_path)

# 2. Vérifier les annotations problématiques
print("\n🔍 Recherche des annotations problématiques...\n")

problematic_annotations = []

for file_path in python_files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                # Cherche les annotations avec guillemets
                if re.search(r'interaction:\s*["\']discord\.Interaction["\']', line):
                    print(f"⚠️  {file_path}:{i} - Annotation avec guillemets trouvée")
                    problematic_annotations.append((file_path, i, line.strip()))

# 3. Afficher le début de commandes_admin.py
print("\n📄 Début de commandes/commandes_admin.py:\n")
if os.path.exists("commandes/commandes_admin.py"):
    with open("commandes/commandes_admin.py", 'r', encoding='utf-8') as f:
        for i, line in enumerate(f.readlines()[:15], 1):
            print(f"{i:3d}: {line.rstrip()}")

# 4. Proposition de correction
print("\n" + "=" * 80)
print("🔧 CORRECTION AUTOMATIQUE")
print("=" * 80 + "\n")

if files_to_fix:
    print(f"📝 {len(files_to_fix)} fichier(s) à corriger:")
    for f in files_to_fix:
        print(f"   - {f}")
    
    response = input("\n❓ Voulez-vous corriger automatiquement ? (o/N): ")
    
    if response.lower() == 'o':
        for file_path in files_to_fix:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Ajoute l'import en première ligne
            new_content = "from __future__ import annotations\n\n" + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Corrigé: {file_path}")
        
        print("\n🎉 Tous les fichiers ont été corrigés!")
        print("\n⚠️  ATTENTION: Supprimez le cache avec:")
        print("   Get-ChildItem -Path . -Recurse -Force | Where-Object { $_.PSIsContainer -and $_.Name -eq '__pycache__' } | Remove-Item -Recurse -Force")
    else:
        print("❌ Correction annulée")
else:
    print("✅ Tous les fichiers ont déjà l'import correct!")

if problematic_annotations:
    print(f"\n⚠️  {len(problematic_annotations)} annotation(s) avec guillemets trouvée(s)")
    print("Ces annotations doivent être SANS guillemets quand 'from __future__ import annotations' est présent!")
    
    response = input("\n❓ Voulez-vous enlever les guillemets ? (o/N): ")
    
    if response.lower() == 'o':
        files_modified = set()
        for file_path, _, _ in problematic_annotations:
            files_modified.add(file_path)
        
        for file_path in files_modified:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Enlève les guillemets des annotations
            content = re.sub(r'interaction:\s*["\']discord\.Interaction["\']', 'interaction: discord.Interaction', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Guillemets enlevés: {file_path}")
        
        print("\n🎉 Tous les guillemets ont été enlevés!")

print("\n" + "=" * 80)
print("✅ DIAGNOSTIC TERMINÉ")
print("=" * 80)
