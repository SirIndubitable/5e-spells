from json import JSONDecoder, load

class Spell:
    _spell_level_string = {0: 'cantrip', 1: '1st', 2: '2nd', 3: '3rd', 4: '4th',
                           5: '5th', 6: '6th', 7: '7th', 8: '8th', 9: '9th'}

    def __init__(self, jobj):
        self._jobj = jobj

    @property
    def Name(self):
        return self._jobj["name"]

    @property
    def Level(self):
        return self._jobj["level"]

    @property
    def Level_str(self):
        return Spell._spell_level_string[self._jobj["level"]]

    @property
    def AtHigherLevels(self):
        return self._jobj["at_higher_levels"]

    @property
    def CastTime(self):
        return self._jobj["casting_time"]

    @property
    def Classes(self):
        return self._jobj["classes"]

    @property
    def Components(self):
        return self._jobj["components"]

    @property
    def Description(self):
        return self._jobj["description"]

    @property
    def Duration(self):
        return self._jobj["duration"]

    @property
    def Range(self):
        return self._jobj["range"]

    @property
    def School(self):
        return self._jobj["school"]

    @property
    def Sources(self):
        return self._jobj["sources"]


# print the spell in json format
class SpellDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "at_higher_levels" in obj:
            return Spell(obj)
        return obj


def Get_Spells():
    from os import path
    basepath = path.dirname(__file__)
    with open(path.join(basepath, "spells.json"), 'r') as json_file:
        return load(json_file, cls=SpellDecoder)