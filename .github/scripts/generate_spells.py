import json
import os
import sys

spell_dir = "/home/runner/work/5e.VF/5e.VF/docs/sorts/"

if __name__ == '__main__':
    os.chdir(spell_dir)
    levels = {}
    spells_json = {}
    spell_dirs = [d for d in os.listdir() if os.path.isdir(d)]
    for d in spell_dirs:
        os.chdir(spell_dir+'/'+d)
        spells = [f for f in os.listdir() if os.path.isfile(f)]
        for s in spells:
            with open(s, encoding="utf8") as f:
                json_spell = {}
                spell_str = f.read()
                first_sep = spell_str.index('---')+4
                second_sep = spell_str[first_sep:].index("---")+4
                metadata = spell_str[first_sep:second_sep]
                description = spell_str[second_sep+4:]
                for line in metadata.split('\n'):
                    property = line[:line.index(':')] if ":" in line else None
                    value = line[line.index(':')+2:] if ":" in line else None
                    if property and property  != "available":
                        if not value and (property != "detailmat" or
                                          (property=='detailmat' and json_spell['Matériel'] == "true")):
                            print(f'WARNING -- spell {s[:-3]} has an empty property : {property}', file=sys.stderr)
                        json_spell[property] = value
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
                if description.startswith('\n'):
                    print(f'WARNING -- spell {s[:-3]} has a non-compliant description', file=sys.stderr)
                json_spell['description'] = description
                spells_json[s[:-3]] = json_spell
    with open("/home/runner/work/5e.VF/5e.VF/docs/spells.json", "w", encoding="utf8") as f:
        f.write(json.dumps(spells_json, ensure_ascii=False, indent=4))
    if '' in levels:
        levels.pop('')