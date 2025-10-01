import json
import os

spell_dir = "C:\\Users\\User\\Documents\\Gautier\\5e.VF\\5e\\docs\\sorts"

if __name__ == '__main__':
    os.chdir(spell_dir)
    levels = {}
    spells_json = {}
    spell_dirs = [d for d in os.listdir() if os.path.isdir(d)]
    for d in spell_dirs:
        os.chdir(spell_dir+'\\'+d)
        spells = [f for f in os.listdir() if os.path.isfile(f)]
        for s in spells:
            with open(s, encoding="utf8") as f:
                json_spell = {}
                spell_str = f.read()
                metadata = spell_str[spell_str.index("---")+4:spell_str.rindex("---")-1]
                for line in metadata.split('\n'):
                    if ':' in line and line[:line.index(':')] != "available":
                        json_spell[line[:line.index(':')]] = line[line.index(':') + 2:]
                available_start = spell_str.index("available:")+len("available")
                available_end = spell_str[available_start:].index("level") + available_start
                availables = spell_str[available_start:available_end].replace("-","")\
                    .replace("\n",",")\
                    .replace(":","")\
                    .replace(" ","")\
                    .replace("[]","")[1:-1].split(',')
                if '' in availables:
                    availables.remove('')
                json_spell["available"] = availables
                if json_spell["level"] in levels:
                    levels[json_spell["level"]] += 1
                else:
                    levels[json_spell["level"]] = 1
                spells_json[s[:-3]] = json_spell
    with open("C:\\Users\\User\\Documents\\Gautier\\5e.VF\\5e\\docs\\spells.json", "w", encoding="utf8") as f:
        f.write(json.dumps(spells_json, ensure_ascii=False, indent=4))
        print(spells_json)
    print(sum(levels.values()))
    if '' in levels:
        levels.pop('')
    print(sum(levels.values()))
    print(levels)