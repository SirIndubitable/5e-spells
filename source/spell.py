import _scrape_engl393
import re
import json


class Spell:
    _spell_level_string = {0: 'cantrip', 1: '1st', 2: '2nd', 3: '3rd', 4: '4th',
                           5: '5th', 6: '6th', 7: '7th', 8: '8th', 9: '9th'}

    def __init__(self, name):
        self.Name = name
        self.Level = -1
        self.School = ''
        self.CastTime = ''
        self.Range = ''
        self.Components = list()
        self.Duration = ''
        self.Description = ''
        self.AtHigherLevels = ''
        self.Classes = list()
        self.Sources = list()

    def set_level_and_school(self, level_and_school):
        """
        'Conjuration cantrip' => 0, 'Conjuration'
        '2nd-level abjuration' => 2, 'Abjuration'
        """
        words = level_and_school.split()
        # if the first word doesn't contain a number, it's probably a cantrip
        if re.search(r'\d', words[0]):
            self.Level = int(words[0][0])
            self.School = words[1].capitalize()
        else:
            self.Level = 0
            self.School = words[0].capitalize()

    def get_level_and_school(self):
        """
        'Conjuration cantrip' => 0, 'Conjuration'
        '2nd-level abjuration' => 2, 'Abjuration'
        """
        if self.Level == 0:
            return self.School + ' ' + self._spell_level_string[self.Level]
        else:
            return self._spell_level_string[self.Level] + '-level' + ' ' + self.School

    def set_description(self, description_string):
        description_parts = description_string.split('At Higher Levels:')
        self.Description = description_parts[0].strip()
        if (len(description_parts) > 1):
            self.AtHigherLevels = description_parts[1].strip()

    def _parse_components_string(self, components_string):
        components = list()
        material_components_match = re.search('[Mm]\s*\(.+\)', components_string)
        components_without_material = components_string
        if material_components_match is not None:
            components_without_material = components_string.replace(material_components_match.group(0), '')
            components_without_material = components_without_material.strip()

        components_without_material = components_without_material.upper()
        if 'V' in components_without_material:
            components.append('V')
        if 'S' in components_without_material:
            components.append('S')
        if material_components_match is not None:
            components.append(material_components_match.group(0))
        return components

    def _parse_info_dict(self, info_dict):
        if 'Casting Time' in info_dict:
            self.CastTime = info_dict['Casting Time']
        if 'Range' in info_dict:
            self.Range = info_dict['Range']
        if 'Components' in info_dict:
            self.Components = self._parse_components_string(info_dict['Components'])
        if 'Duration' in info_dict:
            self.Duration = info_dict['Duration'].replace('Conc.', 'Concentration,')

    # print this spell for debugging purposes
    def print(self):
        print('Name: ' + self.Name)
        print('Level: ' + str(self.Level))
        print('School: ' + self.School)
        print('CastTime: ' + self.CastTime)
        print('Range: ' + self.Range)
        print('Components: ' + ', '.join(self.Components))
        print('Duration: ' + self.Duration)
        print('Description: ' + self.Description)
        print('At Higher Levels: ' + self.AtHigherLevels)

    # write the spell to a file in the format we expect to parse it in parse-spells.py
    def write(self, file):
        file.write(self.Name + '\n')
        file.write(self.get_level_and_school() + '\n')
        file.write('Casting Time: ' + self.CastTime + '\n')
        file.write('Range: ' + self.Range + '\n')
        file.write('Components: ' + ', '.join(self.Components) + '\n')
        file.write('Duration: ' + self.Duration + '\n')
        file.write(self.Description)
        if self.AtHigherLevels is not '':
            file.write('\n' + 'At Higher Levels: ' + self.AtHigherLevels)

    @staticmethod
    def parse_engl393(spell_name):
        this_spell = Spell(spell_name)
        try:
            soup = _scrape_engl393.get_soup(spell_name)
            this_spell._parse_info_dict(_scrape_engl393.get_info(soup))
            this_spell.set_level_and_school(_scrape_engl393.get_level_and_type(soup))
            this_spell.set_description(_scrape_engl393.get_description(soup))
        except Exception:
            import traceback
            print('generic exception: ' + traceback.format_exc())
            return None
        return this_spell


# print the spell in json format
class SpellEncoder(json.JSONEncoder):
    def default(self, obj):
        # return obj.__dict__
        return {
            "at_higher_levels": obj.AtHigherLevels,
            "casting_time": obj.CastTime,
            "classes": obj.Classes,
            "components": obj.Components,
            "description": obj.Description,
            "duration": obj.Duration,
            "level": obj.Level,
            "range": obj.Range,
            "school": obj.School,
            "sources": obj.Sources,
        }
