from jsonschema import validate, ValidationError
from json import loads, dumps

def test_spells_json_schema():
    with open("./build/spells.json", 'r') as json_file:
        with open('./build/spellsSchema.json', 'r') as schema_file:
            schema = loads(schema_file.read())
            spells_json = loads(json_file.read())
            validate(instance=spells_json, schema=schema)