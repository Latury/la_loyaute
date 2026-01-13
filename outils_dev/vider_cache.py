#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 VIDEr-CACHE - La Loyauté BOT
Nettoie TOUS les caches Python du projet
Auteur : Latury | Version : 1.0.0
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

def nettoyer_cache_repertoire(dossier: Path, verbose: bool = True):
    """Nettoie un dossier et ses sous-dossiers"""
    caches_supprimes = []

    for item in dossier.rglob("__pycache__"):
        try:
            shutil.rmtree(item)
            caches_supprimes.append(str(item))
        except Exception:
            pass

    # Cache pip, pytest, etc.
    caches_speciaux = ["__pycache__", ".pytest_cache", ".mypy_cache", ".coverage"]
    for cache in caches_speciaux:
        for item in dossier.rglob(cache):
            try:
                shutil.rmtree(item)
                caches_supprimes.append(str(item))
            except Exception:
                pass

    return caches_supprimes

def main():
    # Dossier racine (là où est ce script)
    projet_path = Path(__file__).parent.absolute()

    print("🧹 VIDEr-CACHE - La Loyauté BOT v1.0.0")
    print(f"📁 Projet : {projet_path}")
    print("-" * 60)

    # Nettoyage principal
    caches = nettoyer_cache_repertoire(projet_path)

    if caches:
        print(f"✅ {len(caches)} cache(s) supprimé(s) :")
        for cache in caches[:10]:  # Top 10
            print(f"   🗑️  {cache}")
        if len(caches) > 10:
            print(f"   ... et {len(caches)-10} autre(s)")
    else:
        print("ℹ️  Aucun cache trouvé")

    # Vérif venv
    venv_path = projet_path / ".venv"
    if venv_path.exists():
        venv_caches = nettoyer_cache_repertoire(venv_path)
        if venv_caches:
            print(f"\n🔧 {len(venv_caches)} cache(s) supprimé(s) dans .venv")

    print("\n🚀 Projet propre ! Relance : python principal.py")
    print(f"📅 Nettoyé le : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    main()
