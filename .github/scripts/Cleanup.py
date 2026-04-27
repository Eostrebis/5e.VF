import os
import re
from pathlib import Path


def nettoyer_markdown():
    fichiers_md = Path('../../docs/').rglob('*.md')
    compteur_modifies = 0

    for chemin_fichier in fichiers_md:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()

        nouveau_contenu = contenu
        code_blocks = []

        # 1. Masquer les blocs de code (en ligne `code` et multilignes ```code```)
        # Cela protège l'indentation (les espaces) et les underscores dans le code.
        def masquer(match):
            code_blocks.append(match.group(0))
            return f"@@CODE_BLOCK_{len(code_blocks) - 1}@@"

        # (?s) permet au point (.) d'inclure les sauts de ligne pour les gros blocs
        nouveau_contenu = re.sub(r'(?s)```.*?```|`.*?`', masquer, nouveau_contenu)

        # 2. Supprimer les espaces multiples (le code masqué n'est pas affecté)
        nouveau_contenu = re.sub(r' {2,}', ' ', nouveau_contenu)

        # 3. Uniformiser le gras : __texte__ devient **texte**
        # Les "lookarounds" (?<!...) et (?=...) s'assurent qu'on ne touche qu'aux
        # vraies balises Markdown et pas à des mots collés.
        nouveau_contenu = re.sub(
            r'(?<![a-zA-Z0-9\\])__(?=\S)(.+?)(?<=\S)__(?![a-zA-Z0-9_])',
            r'**\1**',
            nouveau_contenu
        )

        # 4. Uniformiser l'italique : _texte_ devient *texte*
        nouveau_contenu = re.sub(
            r'(?<![a-zA-Z0-9\\])_(?=\S)(.+?)(?<=\S)_(?![a-zA-Z0-9_])',
            r'*\1*',
            nouveau_contenu
        )

        # 5. Restaurer les blocs de code intacts
        for i, block in enumerate(code_blocks):
            nouveau_contenu = nouveau_contenu.replace(f"@@CODE_BLOCK_{i}@@", block)

        # 6. Sauvegarder si des modifications ont été faites
        if nouveau_contenu != contenu:
            with open(chemin_fichier, 'w', encoding='utf-8') as f:
                f.write(nouveau_contenu)
            compteur_modifies += 1
            print(f"Nettoyé et uniformisé : {chemin_fichier}")

    print(f"\nTerminé ! {compteur_modifies} fichier(s) mis à jour.")


if __name__ == "__main__":
    nettoyer_markdown()