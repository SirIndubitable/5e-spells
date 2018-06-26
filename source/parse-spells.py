import argparse
import re
import json
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
    2, abjuration
    """
    words = line.split()
    # if the first word doesn't contain a number, it's probably a cantrip
    if re.search(r'\d', words[0]):
        return int(words[0][0]), words[1].capitalize()
    else:
        return 0, words[0].capitalize()


def parse_spell(spell):
    spell_iter = iter(spell)
    next(spell_iter)  # Throw away the spell name
    spell_info = {}
    spell_info["level"], spell_info["school"] = parse_type(next(spell_iter))
    spell_info["casting_time"] = next(spell_iter).replace('Casting Time: ', '')
    spell_info["range"] = next(spell_iter).replace('Range: ', '').strip()
    spell_info["components"] = next(spell_iter).replace('Components: ', '')
    spell_info["duration"] = next(spell_iter).replace('Duration: ', '')
    spell_info["description"] = " ".join(spell_iter)
    return spell_info


def parse_file(spell_list, spell_descs):
    spell_list_file = open(spell_list, 'r', encoding="utf8")
    spells = iter(spell_list_file.readlines())
    current_spell, next_spell = get_next_spell(next(spells), spells)
    spellDict = {}
    lines = []
    for spell_description_line in open(spell_descs, 'r', encoding="utf8"):
        if spell_description_line == next_spell:
            spellDict[current_spell.strip()] = parse_spell(lines)
            lines = []
            current_spell, next_spell = get_next_spell(next_spell, spells)
        lines.append(spell_description_line.strip())

    # add the last spell
    spellDict[current_spell.strip()] = parse_spell(lines)
    return spellDict


parser = argparse.ArgumentParser(description='Parses spells into json')
parser.add_argument(dest='spell_list', type=str,
                    help='flat list of all spells')
parser.add_argument(dest='spell_desc', type=str,
                    help='description of all the spells')
parser.add_argument(dest='spell_dest', type=str,
                    help='destination of all the spells json file')

args = parser.parse_args()
spells_dict = parse_file(args.spell_list, args.spell_desc)
json.dumps(spells_dict)
f = open(args.spell_dest, 'w')
f.write(json.dumps(spells_dict, indent=3, sort_keys=True))
f.close()
