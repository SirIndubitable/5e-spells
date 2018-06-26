import argparse
import re
import json
import os
import doctest


def get_next_spell(next_spell, spell_itr):
    current_spell = next_spell
    try:
        next_spell = next(spell_itr)
    except StopIteration:
        next_spell = None
    return current_spell, next_spell


def parse_type(line):
    """Parses the school and level out of the standard string

    >>> parse_type("Conjuration cantrip")
    0, Conjuration
    >>> parse_type("2nd-level abjuration")
    2, Abjuration
    """
    words = line.split()
    # if the first word doesn't contain a number, it's probably a cantrip
    if re.search(r'\d', words[0]):
        return int(words[0][0]), words[1].capitalize()
    else:
        return 0, words[0].capitalize()


def add_spell(spellDict, spell):
    spell_iter = iter(spell)
    spell_name = next(spell_iter).strip()
    spell_info = {}
    spell_info["level"], spell_info["school"] = parse_type(next(spell_iter))
    spell_info["casting_time"] = next(spell_iter).replace('Casting Time: ', '').strip()
    spell_info["range"] = next(spell_iter).replace('Range: ', '').strip()
    spell_info["components"] = next(spell_iter).replace('Components: ', '').strip()
    spell_info["duration"] = next(spell_iter).replace('Duration: ', '').strip()
    spell_info["description"] = " ".join(map(str.strip, spell_iter))
    spellDict[spell_name] = spell_info


def parse_files():
    spellDict = {}
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    spells_dir = os.path.join(script_dir, 'spells')
    for file in os.listdir(spells_dir):
        filename = os.path.join(spells_dir, os.fsdecode(file))
        spell = open(filename, 'r', encoding="utf8")
        add_spell(spellDict, spell)
        spell.close()

    return spellDict


parser = argparse.ArgumentParser(description='Parses spells into json')
parser.add_argument(dest='spell_dest', type=str,
                    help='destination of all the spells json file')

args = parser.parse_args()

spells_dict = parse_files()
json.dumps(spells_dict)
f = open(args.spell_dest, 'w')
f.write(json.dumps(spells_dict, indent=3, sort_keys=True))
f.close()
