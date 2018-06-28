import argparse
import re
import json
import os
import doctest


missing_spells = set()


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


def parse_value(line, valueName):
    """Parses the school and level out of the standard string

    >>> parse_type("Conjuration cantrip")
    0, Conjuration
    >>> parse_type("2nd-level abjuration")
    2, Abjuration
    """
    return line.replace(valueName + ': ', '').strip()


def add_spell(spellDict, spell):
    spell_iter = iter(spell)
    spell_name = next(spell_iter).strip()
    spell_info = dict()
    spell_info["level"], spell_info["school"] = parse_type(next(spell_iter))
    spell_info["casting_time"] = parse_value(next(spell_iter), 'Casting Time')
    spell_info["range"] = parse_value(next(spell_iter), 'Range')
    spell_info["components"] = parse_value(next(spell_iter), 'Components')
    spell_info["duration"] = parse_value(next(spell_iter), 'Duration')
    spell_info["description"] = "".join(spell_iter)
    spell_info['classes'] = list()
    spellDict[spell_name] = spell_info


def add_classes(spellDict):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    classes_dir = os.path.join(script_dir, 'spellListByClass')
    for file in os.listdir(classes_dir):
        filename = os.path.join(classes_dir, file)
        for spell in open(filename, 'r', encoding="utf8"):
            spellName = spell.strip()
            if spellName in spellDict:
                spellDict[spellName]['classes'].append(file.replace('.txt', ''))
            else:
                missing_spells.add(spellName)


def parse_files():
    spellDict = dict()
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    spells_dir = os.path.join(script_dir, 'spells')
    for file in os.listdir(spells_dir):
        filename = os.path.join(spells_dir, os.fsdecode(file))
        spell = open(filename, 'r', encoding="utf8")
        add_spell(spellDict, spell)
        spell.close()
    return spellDict


parser = argparse.ArgumentParser(description='Parses spells into json')
parser.add_argument('-json', dest='json_dest', type=str,
                    help='destination of the spells json file')
parser.add_argument('-list', dest='list_dest', type=str,
                    help='destination of the list of spells file')
parser.add_argument('-class', dest='class_dest', type=str,
                    help='destination of the file with the list of spells and classes')


args = parser.parse_args()
spells_dict = parse_files()
add_classes(spells_dict)
#print("Missing spells: \n")
#print('\n'.join(sorted(missing_spells)))


if args.json_dest is not None:
    f = open(args.json_dest, 'w')
    f.write(json.dumps(spells_dict, indent=3, sort_keys=True))
    f.close()

if args.list_dest is not None:
    f = open(args.list_dest, 'w')
    for spell_name in sorted(spells_dict.keys()):
        f.write(spell_name + '\n')
    f.close()

if args.class_dest is not None:
    f = open(args.class_dest, 'w')
    spells_by_level = {0: [], 1: [], 2: [], 3: [], 4: [],
                       5: [], 6: [], 7: [], 8: [], 9: []}
    for spell_name, spell in spells_dict.items():
        spells_by_level[spell['level']].append(spell_name)
    for spell_level in sorted(spells_by_level.keys()):
        f.write(str(spell_level) + '\n')
        for spell in spells_by_level[spell_level]:
            f.write(spell + ' (' + ', '.join(spells_dict[spell]['classes']) + ')\n')
    f.close()
