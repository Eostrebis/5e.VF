import os
from pathlib import Path

# Nom du fichier final
fichier_sortie = "eostrebis.md"

# rglob("*.md") cherche de manière récursive dans le dossier courant ('.')
fichiers_md = sorted(Path('../../docs/').rglob('*.md'))

with open(fichier_sortie, 'w', encoding='utf-8') as outfile:
    for chemin_fichier in fichiers_md:
        # Convertir le chemin en texte (ex: "sous_dossier/mon_fichier.md")
        fichier_str = str(chemin_fichier)

        # Sécurité : on ne s'inclut pas soi-même si le script tourne plusieurs fois
        if chemin_fichier.name == fichier_sortie:
            continue

        # 1. Écrire l'origine du fichier (avec son chemin complet depuis la racine)
        outfile.write(f"## Fichier : `{fichier_str}`\n\n")

        # 2. Lire le contenu et l'ajouter
        with open(chemin_fichier, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())

        # 3. Ajouter le séparateur
        outfile.write("\n\n---\n\n")

print(f"Terminé ! Tous les fichiers (y compris dans les sous-dossiers) ont été fusionnés dans : {fichier_sortie}")