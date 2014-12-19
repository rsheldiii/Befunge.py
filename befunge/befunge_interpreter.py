'''
Created on Jun 13, 2013

@author: RSHELDON
'''
import csv,sys
from befunge.befunge_program import BefungeProgram

class BefungeInterpreter:
    def __init__(self):
        self.clearProgram() #program loaded into memory, where the key is the hash of the location (eg (1,0) for befunge or (1,3,4) for trefunge etc)
        self.verbose = False

        if __name__ == "__main__":#TODO: move and reimplement these somewhere else, this is now a library for interpreting befunge programs and not a command line tool
            if '-f' in sys.argv:
                self.loadASCIIFile(sys.argv[sys.argv.index('-f')+1])
            if '-c' in sys.argv:
                self.loadCSVFile(sys.argv[sys.argv.index('-c')+1])

            if '-v' in sys.argv:
                self.verbose = True

            if len(self.program):
                self.run()

    def clearProgram(self):
        self.program = BefungeProgram()

    def loadASCIIFile(self,filePath):
        file = open(filePath)
        charinput = file.readlines()
        self.clearProgram()
        for y in range(0,len(charinput)):
            for x in range(0,len(charinput[y])-1):#1 to cut off newlines! check spec on this, we might need to account for /r/n
                self.program[(x,y)] = charinput[y][x]

    def loadCSVFile(self,filePath):
        self.clearProgram()
        y = 0
        width = 0
        with open(filePath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            for row in reader:
                if self.verbose:
                    print(row)
                width = max(len(row),width)
                for x in range(0,len(row)):
                    char = row[x]
                    if char == '':
                        char = ' '
                    self.program[(x,y)] = char
                y += 1


    def run(self):
        self.pointerPosition = (0,0)

        while not self.program.exitStateFound:# and self.tick < 300:
            if self.verbose:
                print(self.program.data)
                #print("pointer position: " + str(self.pointerPosition))
                #print("direction: " +str(self.delta))
                print("current command: " + self.program.getCommand())
                #print('tick: '+ str(self.program.tick))
                print('-'*20)
            self.program.proceed()

        return self.program.exitValue

