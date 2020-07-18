#dirty hack to import built python module
import sys
sys.path.insert(1, './build')
from spell_5e import Get_Spells

from jsonschema import validate, ValidationError
from json import load, dump

def test_spells_json_schema():
    with open("./build/spells.json", 'r') as json_file:
        with open('./build/spellsSchema.json', 'r') as schema_file:
            schema = load(schema_file)
            spells_json = load(json_file)
            validate(instance=spells_json, schema=schema)

def test_spells_decoder():
    spells = Get_Spells()
    fireballSpell = spells['Fireball']
    assert fireballSpell.AtHigherLevels == ""
    assert fireballSpell.CastTime == "1 action"
    assert fireballSpell.Classes == [ "sorcerer", "wizard" ]
    assert fireballSpell.Components == "V, S, M (a tiny ball of bat guano and sulfur)"
    assert fireballSpell.Description == "A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one.\nThe fire spreads around corners. It ignites flammable objects in the area that aren't being worn or carried.\nAt Higher Levels. When you cast this spell using a spell slot of 4th level or higher, the damage increases by 1d6 for each slot level above 3rd."
    assert fireballSpell.Duration == "Instantaneous"
    assert fireballSpell.Level == 3
    assert fireballSpell.Name == "Fireball"
    assert fireballSpell.Range == "150 feet"
    assert fireballSpell.School == "Evocation"
    assert fireballSpell.Sources == [ "phb 241" ]