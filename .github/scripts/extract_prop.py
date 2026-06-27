import re
import json


def extraire_donnees_sort(contenu_texte):
    proprietes = {}
    description_lignes = []
    cle_actuelle = None
    dans_description = False

    for ligne in contenu_texte.split('\n'):
        ligne = ligne.rstrip()

        # 1. Si on est déjà dans la description, on capture tout
        if dans_description:
            description_lignes.append(ligne)
            continue

        # --- CORRECTION ---
        # On ignore les délimiteurs YAML de l'en-tête
        if ligne.strip() == '---':
            continue

        # 2. Chercher une ligne "clé: valeur"
        match_kv = re.match(r'^([a-zA-Z0-9_]+):\s*(.*)$', ligne)
        if match_kv:
            cle, valeur = match_kv.groups()
            cle_actuelle = cle

            if valeur == "[]":
                proprietes[cle] = []
            elif valeur == "":
                proprietes[cle] = ""
            elif valeur.lower() == 'true':
                proprietes[cle] = True
            elif valeur.lower() == 'false':
                proprietes[cle] = False
            else:
                proprietes[cle] = valeur
            continue

        # 3. Chercher un élément de liste (" - Valeur")
        match_liste = re.match(r'^\s*-\s+(.*)$', ligne)
        if match_liste and cle_actuelle:
            valeur_liste = match_liste.group(1)
            if isinstance(proprietes[cle_actuelle], list):
                proprietes[cle_actuelle].append(valeur_liste)
            else:
                proprietes[cle_actuelle] = [proprietes[cle_actuelle], valeur_liste]
            continue

        # 4. Passage en mode description (si la ligne n'est pas vide)
        if ligne.strip() != "":
            dans_description = True
            description_lignes.append(ligne)

    # Assembler la description
    if description_lignes:
        proprietes['description'] = '\n'.join(description_lignes).strip()

    # Filtre du template vide
    if proprietes.get("writing_status") == "empty":
        return {}

    return proprietes