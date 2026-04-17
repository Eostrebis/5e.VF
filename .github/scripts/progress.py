from datetime import datetime
import os
import sys
from pathlib import Path

DEBUG = False

if DEBUG:
	working_dir = "C:\\Users\\frosq\\workspace\\JdR\\5e.VF\\docs"
else:
	working_dir = "/home/runner/work/5e.VF/5e.VF/docs"

directory = Path(working_dir)

SEP = ("\\" if DEBUG else "/")

def get_words(file) -> int:
	if file.endswith('.md'):
		with open(file, encoding='utf8') as f:
			return len(f.read().split())
	return 0

def get_status(file) -> str:
	if file.endswith('.md'):
		with open(file, encoding='utf8') as f:
			lines = f.readlines()
			for line in lines:
				if line.startswith('writing_status'):
					return line[(1+len('writing_status')):].strip()

def evaluate_status(status) -> float:
	match status:
		case "empty":
			return 0
		case "wip":
			return .25
		case "completed":
			return .75
		case "finished":
			return 1
		case _:
			print(f"Status non géré : {status}", file=sys.stderr)
			return 0

def get_spell_progress():
	done = {}
	words = 0
	undone = 0
	index = len(working_dir+SEP+"sorts"+SEP)
	for subdir, dirs, files in os.walk(working_dir+SEP+"sorts"):
		if dirs:
			undone = len(files)
		else:
			done[int(subdir[index:]) if subdir[index:] != 'cantrips' else 0] = len(files)
			for file in files:
				words += get_words(subdir + SEP + file)
	total = undone + sum(done.values())
	return done, total, words

def get_classe_progress():
	done = {}
	words = 0
	classes = [d for d in os.listdir(working_dir+SEP+"classes")]
	for classe in classes:
		total_classe = 0
		done_classe = 0
		for subdir, dirs, files in os.walk(working_dir + SEP + "classes" + SEP + classe):
			for f in files:
				status = get_status(subdir+SEP+f)
				words += get_words(subdir+SEP+f)
				done_classe += evaluate_status(status)
				total_classe += 1
		done[classe] = round(done_classe / total_classe * 100, 2)
	return done, words

def get_race_progress():
	done = 0
	total = 0
	words = 0
	for race in os.listdir(working_dir + SEP + "races"):
		status = get_status(working_dir + SEP + "races" + SEP + race)
		words += get_words(working_dir + SEP + "races" + SEP + race)
		if status:
			done += evaluate_status(status)
			total += 1
	return done, total, words

def get_feat_progress():
	done = 0
	total = 0
	words = 0
	for feat in os.listdir(working_dir + SEP + "Dons"):
		status = get_status(working_dir + SEP + "Dons" + SEP + feat)
		words = get_words(working_dir + SEP + "Dons" + SEP + feat)
		if status:
			done += evaluate_status(status)
			total += 1
	return done, total, words

def get_equipment_progress():
	done = 0
	total = 0
	words = 0
	for gear in os.listdir(working_dir + SEP + "objets" + SEP + "équipement"):
		status = get_status(working_dir + SEP + "objets" + SEP + "équipement" + SEP + gear)
		words += get_words(working_dir + SEP + "objets" + SEP + "équipement" + SEP + gear)
		if status:
			done += evaluate_status(status)
			total += 1
	return done, total, words

def get_magic_item_progress():
	done = 0
	total = 0
	words = 0
	for gear in os.listdir(working_dir + SEP + "objets" + SEP + "magiques"):
		status = get_status(working_dir + SEP + "objets" + SEP + "magiques" + SEP + gear)
		words += get_words(working_dir + SEP + "objets" + SEP + "magiques" + SEP + gear)
		if status:
			done += evaluate_status(status)
			total += 1
	return done, total, words

def get_background_progress():
	done = 0
	total = 0
	words = 0
	for gear in os.listdir(working_dir + SEP + "Historiques"):
		status = get_status(working_dir + SEP + "Historiques" + SEP + gear)
		words = get_words(working_dir + SEP + "Historiques" + SEP + gear)
		if status:
			done += evaluate_status(status)
			total += 1
	return done, total, words

def create_index_file(classe_percentage, classe_done: dict[str, float], spell_percentage, spell_done, spell_total, race_done, race_total, feat_done,
					  feat_total, equip_done, equip_total, magic_item_done, magic_item_total, back_done,
					  back_total,
					  words_total):
	return f"""---
search:
  exclude: true
---
# Eostrebis

## Avancée de la Traduction

**Classes.** {list(classe_done.values()).count(100)}/{len(classe_done)} ![](https://geps.dev/progress/{int(classe_percentage)})

> [!INFO]- Détails par classe
>{">".join([f' - **{classe}.** ![](https://geps.dev/progress/{int(classe_done[classe])}) \n' for classe in sorted(classe_done)])}

**Sorts.** {sum(spell_done.values())}/{spell_total} ![](https://geps.dev/progress/{int(spell_percentage)})

> [!INFO]- Sorts traduits par niveau
>{">".join([f' - **{'Cantrips' if level == 0 else level}.** {int(spell_done[level])} \n' for level in [0,1,2,3,4,5,6,7,8,9]])}

**Races.** {int(race_done)}/{race_total} ![](https://geps.dev/progress/{int(100*race_done/race_total)})

**Dons.** {int(feat_done)}/{feat_total} ![](https://geps.dev/progress/{int(100*feat_done/feat_total)})

**Équipements.** {int(equip_done)}/{equip_total} ![](https://geps.dev/progress/{int(100*equip_done/equip_total)}) 

**Objets Magiques.** {int(magic_item_done)}/{magic_item_total} ![](https://geps.dev/progress/{int(100*magic_item_done/magic_item_total)})

**Historiques.** {int(back_done)}/{back_total} ![](https://geps.dev/progress/{int(100*back_done/back_total)})

**Nombre Total de Mots.** {words_total} (soit ~ {round(words_total/250)} pages) (soit ~ {round(words_total/480000,2)} Seigneur des Anneaux)

En cas de problème à signaler : <a href="mailto:issue@eostrebis.fr">issue@eostrebis.fr</a>"""

def read_index_file():
	with open(working_dir+'/index.md', 'r', encoding='utf-8') as f:
		return f.read()

def write_index_file(content):
	updated_content = content + f"\n\nMis à jour pour la dernière fois le {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
	with open(working_dir+'/index.md', 'w', encoding='utf-8') as f:
		f.write(updated_content)

def compute_progress():
	words_total = 0
	spell_done, spell_total, words = get_spell_progress()
	words_total += words
	race_done, race_total, words = get_race_progress()
	words_total += words
	feat_done, feat_total, words = get_feat_progress()
	words_total += words
	equip_done, equip_total, words = get_equipment_progress()
	words_total += words
	magic_item_done, magic_item_total, words = get_magic_item_progress()
	words_total += words
	back_done, back_total, words = get_background_progress()
	words_total += words
	classe_done, words = get_classe_progress()
	words_total += words
	classe_percentage = sum(classe_done.values()) / (len(classe_done))
	spell_percentage = round(100 * sum(spell_done.values()) / spell_total, 2)

	index_str = create_index_file(classe_percentage, classe_done,
					  spell_percentage, spell_done, spell_total,
					  race_done, race_total,
					  feat_done, feat_total,
					  equip_done, equip_total,
					  magic_item_done, magic_item_total,
					  back_done, back_total, words_total)

	if index_str not in read_index_file():
		write_index_file(index_str)

	print(f"Avancée des classes :\n\t ◺ Toutes classes : {classe_percentage} %")
	for classe in classe_done:
		print(f"\t\t◺ {classe} : {classe_done[classe]:.2f} %")

	print(f"Avancée des sorts :\n\t ◺ Tout niveaux : {spell_percentage} %")
	for level in spell_done:
		if level > 0:
			print(f"\t\t◺ Sorts traduits de niveau {level} : {spell_done[level]}")
		else:
			print(f"\t\t◺ Cantrips traduits : {spell_done[level]}")

	print(f"Avancée des races : {round(100 * race_done / race_total, 2)}%")
	print(f"Avancée des dons : {round(100 * feat_done / feat_total, 2)}%")
	print(f"Avancée des équipements : {round(100 * equip_done / equip_total, 2)}%")
	print(f"Avancée des objets magiques : {round(100 * magic_item_done / magic_item_total, 2)}%")
	print(f"Avancée des historiques : {round(100 * back_done / back_total, 2)}%")
	print(f"Total de mots : {words_total} (soit ~ {round(words_total/250)} pages) (soit ~ {round(words_total/480000,2)} Seigneur des Anneaux)")

if __name__ == '__main__':
	compute_progress()
