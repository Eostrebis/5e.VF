import os
import re
from pathlib import Path


def clean_markdown():
    md_files = Path('../../docs/').rglob('*.md')
    edit_count = 0

    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned_content = content
        code_blocks = []

        def mask(match):
            code_blocks.append(match.group(0))
            return f"@@CODE_BLOCK_{len(code_blocks) - 1}@@"

        cleaned_content = re.sub(r'(?s)```.*?```|`.*?`', mask, cleaned_content)

        cleaned_content = re.sub(r' {2,}', ' ', cleaned_content)

        cleaned_content = re.sub(
            r'(?<![a-zA-Z0-9\\])__(?=\S)(.+?)(?<=\S)__(?![a-zA-Z0-9_])',
            r'**\1**',
            cleaned_content
        )

        cleaned_content = re.sub(
            r'(?<![a-zA-Z0-9\\])_(?=\S)(.+?)(?<=\S)_(?![a-zA-Z0-9_])',
            r'*\1*',
            cleaned_content
        )

        for i, block in enumerate(code_blocks):
            cleaned_content = cleaned_content.replace(f"@@CODE_BLOCK_{i}@@", block)

        if cleaned_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            edit_count += 1
            print(f"Nettoyé et uniformisé : {file_path}")

    print(f"\nTerminé ! {edit_count} fichier(s) mis à jour.")


if __name__ == "__main__":
    clean_markdown()