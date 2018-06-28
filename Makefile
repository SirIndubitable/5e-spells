spells.json: source/parse-spells.py $(wildcard source/spells/*.txt)
	python source/parse-spells.py -json="spells.json" -list="spelllist.txt" -class="List of all 5e spells.txt"