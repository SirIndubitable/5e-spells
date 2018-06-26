spells.json: source\parse-spells.pl source\spelllist.txt source\spelldescs.txt
	perl6 source\\parse-spells.pl | json_pp -json_opt pretty,utf8,canonical > spells.json
