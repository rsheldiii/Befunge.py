from befunge.interpreter import BefungeInterpreter
import sys

b = BefungeInterpreter(False,100)
if (len(sys.argv) <= 2):
    #b.verbose = True# TODO make this not like touch things three deep
    print("beginning totally legit test suite")
    print("hello world")
    b.loadASCIIFile('programs/helloworld.txt')
    b.run()
    print()
    print("dice")
    b.loadCSVFile('programs/dice.csv')
    b.run()
