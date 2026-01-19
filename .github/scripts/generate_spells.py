import json
import os
import sys

spell_dir = "/home/runner/work/5e.VF/5e.VF/docs/sorts/"


def read_spell(spell, verbose=False):
    json_spell = {}
    first_sep = spell.index('---') + 4
    second_sep = spell[first_sep:].index("---") + 4
    metadata = spell[first_sep:second_sep]
    description = spell[second_sep + 4:]
    for line in metadata.split('\n'):
        property = line[:line.index(':')] if ":" in line else None
        value = line[line.index(':') + 2:] if ":" in line else None
        if property and property != "available":
            if verbose and not value and (property != "detailmat" or
                              (property == 'detailmat' and json_spell['Materiel'] == "true")):
                print(f'WARNING -- spell {s[:-3]} has an empty property : {property}', file=sys.stderr)
            json_spell[property] = value
    available_start = spell.index("available:") + len("available")
    available_end = spell[available_start:].index("level") + available_start
    availables = spell[available_start:available_end].replace("-", "") \
        .replace("\n", ",") \
        .replace(":", "") \
        .replace(" ", "") \
        .replace("[]", "")[1:-1].split(',')
    if '' in availables:
        availables.remove('')
    json_spell["available"] = availables
    if json_spell["level"] in levels:
        levels[json_spell["level"]] += 1
    else:
        levels[json_spell["level"]] = 1
    if verbose and description.startswith('\n'):
        print(f'WARNING -- spell {s[:-3]} has a non-compliant description', file=sys.stderr)
    json_spell['description'] = description
    return json_spell

if __name__ == '__main__':
    os.chdir(spell_dir)
    levels = {}
    spells_json = {}
    spell_dirs = [d for d in os.listdir() if os.path.isdir(d)]
    spell_unsorted = [s for s in os.listdir() if os.path.isfile(s) and not os.path.isdir(s)]
    for s in spell_unsorted:
        to_move = False
        with open(s, encoding="utf8") as f:
            js_spell = read_spell(f.read())
            if js_spell['level'] is not None and js_spell['level'] != '':
                print(f"Moving spell {s}")
                to_move = True
        if to_move:
            os.rename(s, f'{"cantrips" if js_spell["level"] == "0" else "0"+js_spell["level"]}/{s}')
    for d in spell_dirs:
        os.chdir(spell_dir+'/'+d)
        spells = [f for f in os.listdir() if os.path.isfile(f)]
        for s in spells:
            with open(s, encoding="utf8") as f:
                spells_json[s[:-3]] = read_spell(f.read(), verbose=True)
    with open("/home/runner/work/5e.VF/5e.VF/docs/spells.json", "w", encoding="utf8") as f:
        f.write(json.dumps(spells_json, ensure_ascii=False, indent=4))
    if '' in levels:
        levels.pop('')