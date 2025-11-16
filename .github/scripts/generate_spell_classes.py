import os
from unidecode import unidecode

spell_dir = "C:\\Users\\frosq\\workspace\\JdR\\5e.VF\\docs\\sorts"

if __name__ == '__main__':
    os.chdir(spell_dir)
    spell_dirs = [d for d in os.listdir() if os.path.isdir(d)]
    for d in spell_dirs:
        os.chdir(spell_dir + '\\' + d)
        spells = [f for f in os.listdir() if os.path.isfile(f)]
        for s in spells:
            with open(s, encoding="utf8") as f:
                spell_str = f.read()
                name = unidecode(s[:-3].title().replace(' ','')).replace("'","")
                first_sep = spell_str.index('---') + 4
                second_sep = spell_str[first_sep:].index("---") + 4
                metadata = spell_str[first_sep:second_sep]
                description = spell_str[second_sep + 4:]
                to_write = f'''from enums.Duration import Duration
from enums.MagicSchool import MagicSchool
from enums.SpellcastingDuration import SpellcastingDuration
from spell.Spell import Spell

class {name}(Spell):
'''
                properties = {}
                for line in metadata.split('\n'):
                    property = line[:line.index(':')] if ":" in line else None
                    value = line[line.index(':') + 2:] if ":" in line else None
                    if property:
                        properties[property] = value
                to_write += f"\tname = '{s[:-3]}'\n"
                to_write += f"\tlevel = {properties['level']}\n"
                to_write += f"\tschool = MagicSchool.{properties['school'].upper()}\n"
                to_write += f"\tverbal = {properties['Verbal'].capitalize()}\n"
                to_write += f"\tsomatic = {properties['Somatique'].capitalize()}\n"
                to_write += f"\tmaterial = {properties['Matériel'].capitalize()}\n"
                to_write += f"\tmaterial_description = '{properties['detailmat']}'\n"
                duree = properties['Durée']
                if ' ' in duree and 'dissipation' not in duree:
                    duration_value, duration_type = properties['Durée'].split()
                    to_write += f"\tduration = {duration_value}\n"
                    match duration_type:
                        case "Minute":
                            duration_type = "MINUTE"
                        case "Minutes":
                            duration_type = "MINUTE"
                        case "Heures":
                            duration_type = "HOUR"
                        case "Heure":
                            duration_type = "HEURES"
                        case "Jour":
                            duration_type = "DAY"
                        case "Jours":
                            duration_type = "DAY"
                        case "jours":
                            duration_type = "DAY"
                        case "Tour":
                            duration_type = "ROUND"
                        case "Tours":
                            duration_type = "ROUND"
                        case "Semaine":
                            duration_type = "WEEK"
                        case "Semaines":
                            duration_type = "WEEKS"
                        case _:
                            raise Exception(f"Duration not handled : {duration_type}")

                    to_write += f"\tduration_type = Duration.{duration_type}\n"
                else:
                    to_write += f"\tduration = 1\n"
                    match duree:
                        case "Spéciale":
                            to_write += f"\tduration_type = Duration.SPECIAL\n"
                        case "Instantanée":
                            to_write += f"\tduration_type = Duration.INSTANTANEOUS\n"
                        case "Jusqu'à dissipation":
                            to_write += f"\tduration_type = Duration.UNTIL_DISPELLED\n"
                        case _:
                            raise Exception(f"Duration not handled : {duree}")
                incantation = properties['Incantation']
                spellcasting, spellcasting_type = incantation.split(maxsplit=1)
                to_write += f"\tspellcasting_duration = {spellcasting}\n"
                match spellcasting_type:
                    case "Action":
                        to_write += f"\tspellcasting_duration_type = SpellcastingDuration.ACTION\n"
                    case "Réaction":
                        to_write += f"\tspellcasting_duration_type = SpellcastingDuration.REACTION\n"
                    case "Action Bonus":
                        to_write += f"\tspellcasting_duration_type = SpellcastingDuration.BONUS_ACTION\n"
                    case "Minute":
                        to_write += f"\tspellcasting_duration_type = SpellcastingDuration.MINUTE\n"
                    case "Minutes":
                        to_write += f"\tspellcasting_duration_type = SpellcastingDuration.MINUTE\n"
                    case "minutes":
                        to_write += f"\tspellcasting_duration_type = SpellcastingDuration.MINUTE\n"
                    case "Heure":
                        to_write += f"\tspellcasting_duration_type = SpellcastingDuration.HOUR\n"
                    case "Heures":
                        to_write += f"\tspellcasting_duration_type = SpellcastingDuration.HOUR\n"
                    case _:
                        raise Exception(f"Duration not handled : {spellcasting_type}")
                if 'Personelle' in properties['Portée']:
                    to_write += f"\tis_range_touch = False\n"
                    to_write += f"\tis_range_self = True\n"
                    if len(properties['Portée']) > 11:
                        to_write += f"\trange_desc = '{properties['Portée'].replace('Personelle','')[1:]}'"
                elif 'Touché' in properties['Portée']:
                    to_write += f"\tis_range_touch = True\n"
                    to_write += f"\tis_range_self = False\n"
                else:
                    to_write += f"\tis_range_touch = False\n"
                    to_write += f"\tis_range_self = False\n"
                    to_write += f"\trange_desc = '{properties['Portée']}'\n"

                to_write += f"\tritual = {properties['Rituel'].capitalize()}\n"
                to_write += f"\tconcentration = {properties['Concentration'].capitalize()}\n"

                to_write += f"\tdescription = '''{description}'''\n"

                with open(f'../../../../SpellsPy/{name}.py', 'w', encoding='utf8') as f:
                    f.write(to_write)