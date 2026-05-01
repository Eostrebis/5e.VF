import spacy
from collections import Counter
import re
from pathlib import Path

nlp = spacy.load("fr_core_news_md")

nlp.max_length = 5000000


def analyser_dossier(chemin_dossier):
	texte_global = ""
	dossier = Path(chemin_dossier)

	# 2. Chercher tous les fichiers .md et .txt (même cachés dans des sous-dossiers)
	fichiers_trouves = list(dossier.rglob('*.md'))

	print(f"-> {len(fichiers_trouves)} fichiers trouvés. Début de la lecture...")

	# 3. Lire et assembler le texte de tous les fichiers
	for fichier in fichiers_trouves:
		try:
			with open(fichier, 'r', encoding='utf-8') as f:
				# On ajoute un espace entre chaque fichier pour ne pas coller les mots
				texte_global += f.read() + " "
		except Exception as e:
			print(f"Impossible de lire le fichier {fichier.name} : {e}")

	if not texte_global.strip():
		print("Erreur : Aucun texte n'a pu être extrait des fichiers.")
		return

	print("-> Lecture terminée. Nettoyage et lemmatisation en cours (ça peut prendre quelques minutes)...")

	# 4. Nettoyage du Markdown (liens, gras, balises images...)
	texte_nettoye = re.sub(r'\[\[.*?\]\]|\*\*|__|\!\[\[.*?\]\]', ' ', texte_global)

	# 5. Analyse par Spacy (le gros du travail)
	doc = nlp(texte_nettoye)

	# 6. Extraction des mots uniques (lemmes) en ignorant la ponctuation et les "mots vides" (le, la, de, et...)
	lemmes = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
	frequences = Counter(lemmes)

	# 7. Affichage des résultats
	print(f"\n" + "=" * 30)
	print(f"RÉSULTATS DE L'ANALYSE")
	print(f"=" * 30)
	print(f"Total de mots analysés : {len(doc)}")
	print(f"Total de mots UNIQUES (racines) : {len(frequences)}")

	print("\n--- TOP 50 DES MOTS LES PLUS FRÉQUENTS ---")
	for mot, compte in frequences.most_common(50):
		print(f"{mot}: {compte} fois")


# Remplace le chemin ci-dessous par le chemin réel de ton dossier sur ton ordinateur
# Exemple sous Windows : r"C:\Users\TonNom\Documents\MonHistoire"
# Exemple sous Mac/Linux : "/Users/TonNom/Documents/MonHistoire"
chemin_de_ton_dossier = r"C:\Users\frosq\Documents\eostrebis-test\5e.VF\docs"

analyser_dossier(chemin_de_ton_dossier)