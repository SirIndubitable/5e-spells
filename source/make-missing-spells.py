import os
import re
from spell import Spell


def clean_string(string):
    upper_string = string.upper()
    return re.sub('[\W_]', '', upper_string)


def get_folder_path(folder_name):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    dir_path = os.path.join(script_dir, '..\\resources')
    return os.path.join(dir_path, folder_name)


def get_all_spells():
    all_spells = set()
    spell_list_dir = get_folder_path('spellsBySource')
    for file in os.listdir(spell_list_dir):
        filename = os.path.join(spell_list_dir, file)
        for file_line in open(filename, 'r', encoding="utf8"):
            spell_name, spell_page = file_line.split(': ')
            all_spells.add(spell_name.strip())
    return all_spells


def get_all_available_spells():
    spells_dir = get_folder_path('spells')
    all_available_spells = set()
    for file in os.listdir(spells_dir):
        all_available_spells.add(file.replace('.txt', '').replace('_', ' '))
    return all_available_spells


if __name__ == "__main__":
    all_spells = list(get_all_spells())
    all_spells.sort()
    all_available_spells = get_all_available_spells()
    clean_available_spells = list(map(clean_string, all_available_spells))

    for spell_name in all_spells:
        if clean_string(spell_name) in clean_available_spells:
            print('Skipping ' + spell_name)
            continue

        current_spell = Spell.parse_engl393(spell_name)
        if current_spell is None:
            continue

        spells_dir = get_folder_path('spells')
        rel_path = spell_name.replace(' ', '_')
        rel_path = re.sub('[\W]', '', rel_path)
        rel_path += ".txt"
        abs_file_path = os.path.join(spells_dir, rel_path)
        f = open(abs_file_path, 'w', encoding="utf8")
        current_spell.write(f)
        f.close()
