import sys
from enum import Enum, auto
from pathlib import Path

import extract_prop

global spell_name

class School(Enum):
    ABJURATION = auto()
    CONJURATION = auto()
    DIVINATION = auto()
    ENCHANTMENT = auto()
    EVOCATION = auto()
    ILLUSION = auto()
    NECROMANCY = auto()
    TRANSMUTATION = auto()
    BLANK = auto()

class DamageType(Enum):
    ACID = auto()
    BLUDGEONING = auto()
    COLD = auto()
    FIRE = auto()
    FORCE = auto()
    LIGHTNING = auto()
    NECROTIC = auto()
    PIERCING = auto()
    POISON = auto()
    PSYCHIC = auto()
    RADIANT = auto()
    SLASHING = auto()
    THUNDER = auto()
    NONE = auto()

class AreaType(Enum):
    NONE = auto()
    CONE15 = auto()
    CONE30 = auto()
    CONE40 = auto()
    CONE60 = auto()
    CUBE10 = auto()
    CUBE100 = auto()
    CUBE15 = auto()
    CUBE20 = auto()
    CUBE150 = auto()
    CUBE200 = auto()
    CUBE2500 = auto()
    CUBE30 = auto()
    CUBE40 = auto()
    CUBE400000 = auto()
    CUBE5 = auto()
    CUBE5280 = auto()
    CYLINDER10 = auto()
    CYLINDER20 = auto()
    CYLINDER40 = auto()
    CYLINDER5 = auto()
    CYLINDER50 = auto()
    CYLINDER60 = auto()
    LINE100 = auto()
    LINE50 = auto()
    LINE60 = auto()
    LINE90 = auto()
    SPHERE10 = auto()
    SPHERE100 = auto()
    SPHERE15 = auto()
    SPHERE20 = auto()
    SPHERE30 = auto()
    SPHERE360 = auto()
    SPHERE40 = auto()
    SPHERE5 = auto()
    SPHERE60 = auto()

class Range(Enum):
    BLANK = auto()
    MILE = auto()
    KILOMETRE = auto()
    KILOMETRES2 = auto()
    FEET10 = auto()
    FEET15 = auto()
    FEET100 = auto()
    FEET120 = auto()
    FEET150 = auto()
    FEET30 = auto()
    FEET300 = auto()
    FEET5 = auto()
    FEET500 = auto()
    MILES500 = auto()
    FEET60 = auto()
    FEET90 = auto()
    SELF = auto()
    SIGHT = auto()
    SPECIAL = auto()
    TOUCH = auto()
    UNLIMITED = auto()

class Duration(Enum):
    INSTANTANEOUS = auto()
    HOUR = auto()
    MINUTE = auto()
    ROUND = auto()
    DAYS10 = auto()
    DAYS7 = auto()
    DAYS30 = auto()
    MINUTES10 = auto()
    HOURS24 = auto()
    HOURS8 = auto()
    SPECIAL = auto()
    DISPELLED = auto()
    U_HOUR = auto()
    U_MINUTE = auto()
    U_ROUND = auto()
    U_MINUTES10 = auto()
    U_HOURS24 = auto()
    U_HOURS8 = auto()
    U_HOURS2 = auto()

def get_school(school):
    match school:
        case "Abjuration":
            return School.ABJURATION
        case "Conjuration":
            return School.CONJURATION
        case "Divination":
            return School.DIVINATION
        case "Enchantement":
            return School.ENCHANTMENT
        case "Évocation":
            return School.EVOCATION
        case "Illusion":
            return School.ILLUSION
        case "Nécromancie":
            return School.NECROMANCY
        case "Transmutation":
            return School.TRANSMUTATION
        case "":
            return School.BLANK
        case _:
            raise KeyError("Unknown school type :"+school)

def get_damage_type(damage_type):
    match damage_type:
        case "":
            #print("/!\\ WARNING, this damage type should maybe be looked at", file=sys.stderr)
            return DamageType.NONE
        case _:
            raise KeyError("Unknown damage type :"+damage_type)

def get_range(spell_range):
    match spell_range:
        case "Personnelle":
            return Range.SELF, AreaType.NONE
        case "Personnelle (rayon de 10 ft.)":
            return Range.SELF, AreaType.SPHERE10
        case "Personnelle (rayon de 15 ft.)":
            return Range.SELF, AreaType.SPHERE15
        case "Personnelle (rayon de 30 ft.)":
            return Range.SELF, AreaType.SPHERE30
        case "Personnelle (rayon de 60 ft.)":
            return Range.SELF, AreaType.SPHERE60
        case "Personnelle (rayon de 100 ft.)":
            return Range.SELF, AreaType.SPHERE100
        case "Personnelle (cône de 15 ft.)":
            return Range.SELF, AreaType.CONE15
        case "10 ft.":
            return Range.FEET10, AreaType.NONE
        case "15 ft.":
            return Range.FEET15, AreaType.SPHERE30
        case "60 ft.":
            return Range.FEET60, AreaType.NONE
        case "30 ft.":
            return Range.FEET30, AreaType.NONE
        case "120 ft.":
            return Range.FEET120, AreaType.NONE
        case "90 ft.":
            return Range.FEET90, AreaType.NONE
        case "300 ft.":
            return Range.FEET300, AreaType.NONE
        case "90 ft. (cube de 20 ft.)":
            return Range.FEET90, AreaType.CUBE20
        case "90 ft. (rayon de 20 ft.)":
            return Range.FEET90, AreaType.SPHERE20
        case "60 ft. (cube de 10 ft.)":
            return Range.FEET60, AreaType.CUBE10
        case "2 kilomètres":
            return Range.KILOMETRES2, AreaType.NONE
        case "Contact":
            return Range.TOUCH, AreaType.NONE
        case _:
            raise KeyError(f"{spell_name} - Unknown range : {spell_range}")

def get_duration(duration):
    match duration:
        case "Spéciale":
            return Duration.SPECIAL
        case "Jusqu'à dissipation":
            return Duration.DISPELLED
        case "1 Tour":
            return Duration.ROUND
        case "Instantanée":
            return Duration.INSTANTANEOUS
        case "1 Minute":
            return Duration.MINUTE
        case "10 Minutes":
            return Duration.MINUTES10
        case "8 Heures":
            return Duration.HOURS8
        case "24 Heures":
            return Duration.HOURS24
        case "1 Heure":
            return Duration.HOUR

        case _:
            raise KeyError(f"{spell_name} - Unknown duration : {duration}")

class Spell:
    def __init__(self, name, level, school, damage_type, spell_range, duration):
        global spell_name
        spell_name = name
        self.level = level
        self.school = get_school(school)
        self.damage_type = get_damage_type(damage_type)
        (self.range, self.area_type) = get_range(spell_range)
        self.duration = get_duration(duration)


def spell_rep():
    md_files = Path('../../docs/sorts').rglob('*.md')
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        j = extract_prop.extraire_donnees_sort(content)
        if j == {}:
            continue
        level = j["level"]
        school = j["school"]
        damage_type = ""
        spell_range = j["Portee"]
        duration = j["Duree"]
        spell = Spell(file_path, level, school, damage_type, spell_range, duration)
if __name__ == '__main__':
    spell_rep()