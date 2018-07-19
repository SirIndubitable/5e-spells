import argparse
import re
import os


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

def parse_file(spell_list, spell_descs):
    spell_list_file = open(spell_list, 'r', encoding="utf8")
    spells = iter(spell_list_file.readlines())
    current_spell, next_spell = get_next_spell(next(spells), spells)
    spellDict = {}
    lines = []
    for spell_description_line in open(spell_descs, 'r', encoding="utf8"):
        if spell_description_line == next_spell:
            spellDict[current_spell.strip()] = '\n'.join(lines)
            lines = []
            current_spell, next_spell = get_next_spell(next_spell, spells)
        lines.append(spell_description_line.strip())

    # add the last spell
    spellDict[current_spell.strip()] = '\n'.join(lines)
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
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
script_dir = os.path.join(script_dir, 'spells')
for key, value in spells_dict.items():
    rel_path = key + ".txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path, 'w', encoding="utf8")
    f.write(value)
    f.close()
