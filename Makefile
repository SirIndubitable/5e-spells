 SOURCE	:= source/parse-spells.py \
 		   source/spell.py

COPY_RESOURCE_FILES := spellsSchema.json
COPY_DST_FILES := $(addprefix export/, $(COPY_RESOURCE_FILES))

all: parseTest export/spells.json $(COPY_DST_FILES) test

export/spells.json: $(SOURCE) $(wildcard resources/*/*.txt)
	$(info )
	$(info ************   Creating Json   ************)
	mkdir -p export
	python source/parse-spells.py -json="export/spells.json" -list="export/spelllist.txt" -class="export/List of all 5e spells.txt"

$(COPY_DST_FILES): export/% : resources/%
	$(info )
	$(info ************ Copying Resources ************)
	cp -f resources/spellsSchema.json export/spellsSchema.json

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
