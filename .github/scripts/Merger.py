import os
from pathlib import Path

output_file = "eostrebis_spells.md"

md_files = sorted(Path('../../docs/sorts/').rglob('*.md'))

with open(output_file, 'w', encoding='utf-8') as outfile:
    for file_path in md_files:
        str_path = str(file_path)

        if file_path.name == output_file:
            continue

        outfile.write(f"## Fichier : `{str_path}`\n\n")

        with open(file_path, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())

        outfile.write("\n\n---\n\n")

print(f"Terminé ! Tous les fichiers (y compris dans les sous-dossiers) ont été fusionnés dans : {output_file}")
