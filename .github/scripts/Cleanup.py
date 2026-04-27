import os
import re
from pathlib import Path

# Chercher tous les fichiers .md de manière récursive
fichiers_md = Path('../../docs/').rglob('*.md')
compteur_modifies = 0

for chemin_fichier in fichiers_md:
    # 1. Lire le contenu du fichier
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()

    # 2. Remplacer les espaces multiples
    # L'expression r' {2,}' cible spécifiquement 2 caractères "espace" ou plus.
    # Les \n, \t et autres caractères invisibles sont ignorés.
    nouveau_contenu = re.sub(r' {2,}', ' ', contenu)

    # 3. Sauvegarder uniquement si le fichier a été modifié
    if nouveau_contenu != contenu:
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            f.write(nouveau_contenu)
        compteur_modifies += 1
        print(f"Nettoyé : {chemin_fichier}")

print(f"\nTerminé ! {compteur_modifies} fichier(s) corrigé(s).")