 SOURCE	:= source/parse-spells.py \
 		   source/spell.py

COPY_RESOURCE_FILES := spellsSchema.json
COPY_DST_FILES := $(addprefix build/, $(COPY_RESOURCE_FILES))

all: parseTest build/spells.json $(COPY_DST_FILES) test

build/spells.json: $(SOURCE) $(wildcard resources/*/*.txt)
	$(info )
	$(info ************   Creating Json   ************)
	mkdir -p build
	python source/parse-spells.py -json="build/spells.json" -list="build/spelllist.txt" -class="build/List of all 5e spells.txt"

$(COPY_DST_FILES): build/% : resources/%
	$(info )
	$(info ************ Copying Resources ************)
	cp -f resources/spellsSchema.json build/spellsSchema.json

test:
	$(info )
	$(info ************  Verifying Json   ************)
	python -m pytest

parseTest: 
	$(info )
	$(info ************ Verifying scripts ************)
	python source/parse-spells.py --doctest

init:
	pip install -r requirements.txt

new-spells:
	python source/make-missing-spells.py
