import _scrape_engl393
import re
import json


class Spell:
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

    def _set_description(self, description_string):
        description_parts = description_string.split('At Higher Levels:')
        self.Description = description_parts[0].strip()
        if (len(description_parts) > 1):
            self.AtHigherLevels = description_parts[1].strip()

    def _parse_info_dict(self, info_dict):
        if 'Casting Time' in info_dict:
            self.CastTime = info_dict['Casting Time']
        if 'Range' in info_dict:
            self.Range = info_dict['Range']
        if 'Components' in info_dict:
            # TODO figure out how to parse components
            self.Components = info_dict['Components']
        if 'Duration' in info_dict:
            self.Duration = info_dict['Duration']

    def print(self):
        print('Name: ' + self.Name)
        print('Level: ' + str(self.Level))
        print('School: ' + self.School)
        print('CastTime: ' + self.CastTime)
        print('Range: ' + self.Range)
        print('Components: ' + self.Components)
        print('Duration: ' + self.Duration)
        print('Description: ' + self.Description)
        print('At Higher Levels: ' + self.AtHigherLevels)

    @staticmethod
    def parse_engl393(spell_name):
        this_spell = Spell(spell_name)
        try:
            soup = _scrape_engl393.get_soup(spell_name)
            this_spell._parse_info_dict(_scrape_engl393.get_info(soup))
            this_spell._set_level_and_school(_scrape_engl393.get_level_and_type(soup))
            this_spell._set_description(_scrape_engl393.get_description(soup))
        except Exception:
            return None
        return this_spell


class SpellEncoder(json.JSONEncoder):
    def default(self, obj):
        # return obj.__dict__
        return {"at_higher_levels": obj.AtHigherLevels,
           "casting_time": obj.CastTime,
           "classes": obj.Classes,
           "components": obj.Components,
           "description": obj.Description,
           "duration": obj.Duration,
           "level": obj.Level,
           "range": obj.Range,
           "school": obj.School,
        }
