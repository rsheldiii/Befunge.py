BEFUNGE.py

a Python 3 befunge interpreter. just because. Also because I can't find any Funge98 compliant interpreters lying around.

I've currently passed the befunge-93 specification, and I'm working towards getting the interpreter funge-98 compliant, while adding the ability to parse CSV files (which make it a million times easier to edit).

Todo:
	* Lahey-space wraparound
	* a few 3d functions(all noops in arg list)
	* reorder functions to match character map so you dont have to hunt everywhere
	* develop test suite