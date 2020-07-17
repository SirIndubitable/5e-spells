This is a hopefully complete and mostly correct database of D&D 5e spells in a computer
readable format.

It may be a bit off in some places, as it was created by forking https://github.com/tadzik/5e-spells
then parsing https://engl393-dnd5th.wikia.com to get the rest of the spells.

Please report any issues and discrepancies with the list.

`make new-spells` will try to parse spell information from https://engl393-dnd5th.wikia.com 
for any spell that is listed under a source in /resources/spellsBySource and not in /resources/spells

`make export/spells.json` will then take any spells in /resources/spells and make a json file containing the information
contained in the .txt files.  It also will add the book source and supported classes from
/resources/spellListByClass and /resources/spellsBySource

It is set up this way (instead of just always parsing engl393) is so that we can make fixes to the 
spell.txt files if engl393 is not correct.

Enjoy!
