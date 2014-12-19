from befunge.befunge_interpreter import BefungeInterpreter
import sys

b = BefungeInterpreter()
if (len(sys.argv) <= 2):
    b.verbose = False#True
    b.loadCSVFile('dice.csv')
    #b.loadASCIIFile('befunge.txt')
    b.run()
