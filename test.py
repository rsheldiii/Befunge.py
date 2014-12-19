from befunge.befunge_interpreter import BefungeInterpreter
import sys

b = BefungeInterpreter()
if (len(sys.argv) <= 2):
    b.program.verbose = False#True TODO make this not like touch things three deep
    b.loadCSVFile('programs/dice.csv')
    #b.loadASCIIFile('befunge.txt')
    b.run()
