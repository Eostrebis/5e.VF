import argparse
import re
from pathlib import Path


def update_property(property, old, new):
    md_files = Path('../../docs/').rglob('*.md')
    edit_count = 0

    pattern = re.compile(
        rf'^({re.escape(property)}:\s*){re.escape(old)}$',
        re.MULTILINE
    )

    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            updated_content, update_count = pattern.subn(rf'\g<1>{new}', content)

            if update_count > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                edit_count += 1
                print(f"Modifié : {file_path}")

        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path} : {e}")

    print(f"\nTerminé ! {edit_count} fichier(s) mis à jour.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remplace la valeur d'une propriété dans l'en-tête de fichiers Markdown.")

    parser.add_argument("property", help="Le nom de la propriété (ex: school)")
    parser.add_argument("old", help="La valeur actuelle à remplacer (ex: Transmutation)")
    parser.add_argument("new", help="La nouvelle valeur voulue (ex: Évocation)")

    args = parser.parse_args()

    update_property(args.property, args.old, args.new)
