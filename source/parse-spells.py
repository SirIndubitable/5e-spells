import argparse
import re
import json
import os
from spell import Spell
from spell import SpellEncoder


missing_spells = set()
created_spells = set()
spells_dict = dict()


def spell_list_parser(dir):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            dir_path = get_dir_path(dir)
            for file in os.listdir(dir_path):
                filename = os.path.join(dir_path, file)
                for file_line in open(filename, 'r', encoding="utf8"):
                    spellName = function(file.replace('.txt', ''), file_line)
                    if spellName not in spells_dict:
                        missing_spells.add(spellName)
        return wrapper
    return real_decorator


def get_alphanumeric_intersection(set1, set2):
    """Returns the the intersection of the sets with the non
       alphanumeric characters removed and ignoring case

    >>> s1 = set(['unique1', 'unique2', 'commons1', 'Common2'])
    >>> s2 = set(['unique3', 'unique4', "common's1", 'common2'])
    >>> sorted(get_alphanumeric_intersection(s1, s2))
    ['COMMON2', 'COMMONS1']
    """
    set1_clean = [x.upper() for x in set1]
    set2_clean = [x.upper() for x in set2]
    set1_clean = set([re.sub('[\W_]', '', x) for x in set1_clean])
    set2_clean = set([re.sub('[\W_]', '', x) for x in set2_clean])
    return set.intersection(set1_clean, set2_clean)


def get_next_spell(next_spell, spell_itr):
    """Returns the new current spell and next spell given
       the old next_spell and the list

    >>> get_next_spell('Alarm', iter(['Finger of Death', 'Catnap']))
    ('Alarm', 'Finger of Death')
    """
    current_spell = next_spell
    try:
        next_spell = next(spell_itr)
    except StopIteration:
        next_spell = None
    return current_spell, next_spell


def add_spell(spellDict, spell_file):
    spell = Spell.read(spell_file)
    spellDict[spell.Name] = spell
    created_spells.add(spell.Name)


@spell_list_parser('spellsBySource')
def add_sources(file_name, file_line):
    spell_name, spell_page = file_line.split(': ')
    if spell_name in spells_dict:
        spell_location = file_name + ' ' + spell_page.strip()
        spells_dict[spell_name].Sources.append(spell_location)
    return spell_name


@spell_list_parser('spellListByClass')
def add_classes(file_name, file_line):
    spell_name = file_line.strip()
    if spell_name in spells_dict:
        spells_dict[spell_name].Classes.append(file_name)
    return spell_name


def parse_spell_files():
    spells_dir = get_dir_path('spells')
    for file in os.listdir(spells_dir):
        filename = os.path.join(spells_dir, os.fsdecode(file))
        spell = open(filename, 'r', encoding="utf8")
        add_spell(spells_dict, spell)
        spell.close()


def get_dir_path(dir):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    dir_path = os.path.join(script_dir, '..\\resources')
    dir_path = os.path.join(dir_path, dir)
    return dir_path


parser = argparse.ArgumentParser(description='Parses spells into json')
parser.add_argument('--doctest', action='store_true',
                    help='run the doctest of the file')
parser.add_argument('-json', dest='json_dest', type=str,
                    help='destination of the spells json file')
parser.add_argument('-list', dest='list_dest', type=str,
                    help='destination of the list of spells file')
parser.add_argument('-class', dest='class_dest', type=str,
                    help='destination of the file with the list of spells and classes')


args = parser.parse_args()
if args.doctest:
    import doctest
    doctest.testmod()
    exit()

parse_spell_files()
add_classes()
add_sources()

error_spells = get_alphanumeric_intersection(missing_spells, created_spells)
if len(error_spells) > 0:
    print("Errors with: \n")
    print('\n'.join(error_spells))

#print("Missing spells: \n")
#print('\n'.join(sorted(missing_spells)))


if args.json_dest is not None:
    f = open(args.json_dest, 'w+')
    f.write(json.dumps(spells_dict, cls=SpellEncoder, indent=3, sort_keys=True))
    f.close()

if args.list_dest is not None:
    f = open(args.list_dest, 'w+')
    for spell_name in sorted(spells_dict.keys()):
        f.write(spell_name + '\n')
    f.close()

if args.class_dest is not None:
    f = open(args.class_dest, 'w+')
    spell_level_string = {0: 'cantrip', 1: '1st', 2: '2nd', 3: '3rd', 4: '4th',
                          5: '5th', 6: '6th', 7: '7th', 8: '8th', 9: '9th'}
    spells_by_level = {0: [], 1: [], 2: [], 3: [], 4: [],
                       5: [], 6: [], 7: [], 8: [], 9: []}
    for spell_name, spell in spells_dict.items():
        spells_by_level[spell.Level].append(spell_name)
    for spell_level in sorted(spells_by_level.keys()):
        f.write(spell_level_string[spell_level] + '\n')
        for spell_name in spells_by_level[spell_level]:
            f.write(spell_name + ' (' + ', '.join(spells_dict[spell_name].Classes) + ')\n')
        f.write('\n')
    f.close()
