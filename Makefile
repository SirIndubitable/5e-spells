 SOURCE	:= source/parse-spells.py \
 		   source/spell.py

all: new-spells parseTest export/spells.json test

export/spells.json: $(SOURCE) $(wildcard resources/*/*.txt) 
	python source/parse-spells.py -json="export/spells.json" -list="export/spelllist.txt" -class="export/List of all 5e spells.txt"

test:
	python -m pytest

parseTest: 
	python source/parse-spells.py --doctest

init:
	pip install -r requirements.txt

new-spells:
	python source/make-missing-spells.py
