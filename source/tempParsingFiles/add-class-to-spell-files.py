import argparse
import re
import os
from subprocess import call
from pathlib import Path

def parse_file():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    spells_dir = os.path.join(script_dir, 'spells')
    for line in open('List of all 5e spells.txt', 'r', encoding='utf8'):
        if not re.search(r'(.+)\((.+)\)', line):
            continue

        matches = re.match(r'(.+)\((.+)\)', line)
        spell_name = matches.group(1).strip()
        spell_file_path = os.path.join(spells_dir, spell_name + '.txt')
        #f = open(spell_file_path, "r", encoding='utf8')
        #contents = f.readlines()
        #f.close()

        #contents.insert(2, 'Classes: ' + matches.group(2).strip() + '\n')
#
        #f = open(spell_file_path, "w", encoding='utf8')
        #contents = "".join(contents)
        #f.close()
        if not Path(spell_file_path).exists():
            f = open(spell_file_path, "w", encoding='utf8')
            f.write('\n')
            f.close()
            #call(["start", spell_file_path])

parse_file()
