import _scrape_engl393
import re
import json
import logging
from urllib.error import HTTPError

log = logging.getLogger(__name__)

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

    def _set_level_and_school(self, level_and_school):
        """
        'Conjuration cantrip' => 0, 'Conjuration'
        '2nd-level abjuration' => 2, 'Abjuration'
        """
        words = level_and_school.split()
        # if the first word doesn't contain a number, it's probably a cantrip
        if re.search(r'\d', words[0]):
            self.Level = int(words[0][0])
            self.School = words[-1].capitalize()
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

    def _set_description(self, description_string):
        description_parts = description_string.replace('At Higher Levels.', 'At Higher Levels:').split('At Higher Levels:')
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
        if 'cast_time' in info_dict:
            self.CastTime = info_dict['cast_time']
        if 'range' in info_dict:
            self.Range = info_dict['range']
        if 'components' in info_dict:
            self.Components = self._parse_components_string(info_dict['components'])
        if 'duration' in info_dict:
            self.Duration = info_dict['duration'].replace('Conc.', 'duration,')

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


    @staticmethod
    def _parse_value(line, valueName):
        """Parses the value out of the line

        >>> _parse_value("Casting Time: 1 hour", "Casting Time")
        '1 hour'
        >>> _parse_value("Components: V, S, M", "Components")
        'V, S, M'
        """
        return line.replace(valueName + ': ', '').strip()

    # write the spell to a file in the format we expect to parse it in read()
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
    def read(file):
        spell_iter = iter(file)
        spell_name = next(spell_iter).strip()
        spell = Spell(spell_name)
        spell._set_level_and_school(next(spell_iter))
        spell.CastTime = Spell._parse_value(next(spell_iter), 'Casting Time')
        spell.Range = Spell._parse_value(next(spell_iter), 'Range')
        spell.Components = Spell._parse_value(next(spell_iter), 'Components')
        spell.Duration = Spell._parse_value(next(spell_iter), 'Duration')
        spell._set_description("".join(spell_iter))
        return spell

    @staticmethod
    def parse_engl393(spell_name):
        this_spell = Spell(spell_name)
        try:
            soup = _scrape_engl393.get_soup(spell_name)
            info = _scrape_engl393.parse_info(soup)
            this_spell._parse_info_dict(info)
            this_spell._set_level_and_school(info["level_and_type"])
            this_spell._set_description(info["descr_n"])
        except HTTPError:
            log.info(f'"{spell_name}": Page not found')
            return None
        except Exception:
            log.exception(f'"{spell_name}"')
            return None
        return this_spell


# print the spell in json format
class SpellEncoder(json.JSONEncoder):
    def default(self, obj):
        # return obj.__dict__
        return {
            "name": obj.Name,
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
