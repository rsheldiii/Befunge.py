'''
Created on Jun 13, 2013

@author: RSHELDON

NOTE: currently windows only because of the msvcrt module
linux solution for immediate command line interpretation should be implemented

import sys
import tty
tty.setcbreak(sys.stdin)
while True:
    print ord(sys.stdin.read(1))
'''
import sys,random,csv,msvcrt,re
from collections import deque

class Stack:#currently no idea how to do x[3:5]
    def __init__(self,a=[]):
        self.list = a
    def push(self,val):
        self.list.append(val)
    def pop(self,n=""):
        if n == "":
            try:
                return self.list.pop()
            except:
                return 0
        else:
            self.list.pop(n)#will error if you try to pop something that doesnt exist. good idea?
    def __getitem__(self,i):
        return self.list[i]
    def __repr__(self):
        return str(self.list)

class BefungeInterpreter:
    def __init__(self):
        self.program = {}
        self.tick = 0
        self.stack = deque([Stack()])
        self.exitStateFound = False
        self.pointerPosition = (0,0)
        self.exitValue = 0
        self.storageOffset = (0,0)
        self.stringMode = False;
        self.stringCharacter = '"'
        self.jumpOverMode = False;
        self.jumpOverCharacter = ';'
        self.functionDictionary = {\
                                   '+' : self.add, '-' : self.subtract, '*' : self.multiply, '/' : self.divide,\
                                   '%' : self.modulus, '!' : self.logicalNot, '`' : self.greaterThan,\
                                   '>' : self.east, '<' : self.west, '^' : self.north, 'V' : self.south, 'v' : self.south, '?' : self.randomDirection,\
                                   '_' : self.westOrEast, '|' : self.northOrSouth,\
                                   ':' : self.duplicate, '\\' : self.swap, '$' : self.pop, '.' : self.intPrint, ',' : self.strPrint,\
                                   '#' : self.jump, 'p' : self.put, 'g' : self.get,\
                                   '&' : self.inputNumber, '~' : self.inputChar, '@' : self.end, ' ' : self.noop,\
                                   self.stringCharacter : self.string, 'r' : self.reverse, 'x' : self.popVector,\
                                   'j' : self.jumpForward, 'q' : self.quit, 'k' : self.iterate,\
                                   '[' : self.turnLeft, ']' : self.turnRight, 'w' : self.compare,
                                   '{' : self.beginBlock, '}' : self.endBlock, "'" : self.fetchCharacter,
                                   'n' : self.clearStack, 'u' : self.stackUnderStack
                                   }
        self.EAST = (1,0)
        self.WEST = (-1,0)
        self.NORTH = (0,1)
        self.SOUTH = (0,-1)
        
        self.delta = self.EAST
        
        if __name__ == "__main__":
            if '-f' in sys.argv:
                self.loadASCIIFile(sys.argv[sys.argv.index('-f')+1])
            if '-c' in sys.argv:
                self.loadCSVFile(sys.argv[sys.argv.index('-c')+1])
            
            if '-v' in sys.argv:
                self.verbose = True
            
            if len(self.program):
                self.run()
    
    def clearProgram(self):
        self.program = {}
        
    def loadASCIIFile(self,filePath):
        file = open(filePath)
        charinput = file.readlines()
        self.clearProgram()
        for y in range(0,len(charinput)):
            for x in range(0,len(charinput[y])):
                self.program[(x,y)] = charinput[y][x]
    
    def loadCSVFile(self,filePath):
        self.clearProgram()
        y = 0
        width = 0
        with open(filePath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='�')
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
        
        while not self.exitStateFound:
            self.tick +=1
            if self.verbose:
                currentCommand = self.getCommand()
                print(self.stack)
                print("pointer position: " + str(self.pointerPosition))
                print("direction: " +str(self.delta))
                print("current command: " + currentCommand)
                print('tick: '+ str(self.tick))
            self.processCommand()
        
        return self.exitValue
            
    def getCommand(self):
        if self.stringMode:
            if self.program.get(self.pointerPosition," ") == " ":
                #return space and set program counter to place before the next value
                while self.program.get(self.pointerPosition," ") == " ":
                    self.advance()
                self.retreat()
                return " "
            else:
                return self.program[self.pointerPosition]
        else:
            if self.program.get(self.pointerPosition," ") == ";":
                self.advance()
                while self.program.get(self.pointerPosition," ") != ";":
                    self.advance()
                self.advance()
                return self.getCommand()
            elif self.program.get(self.pointerPosition," ") == " ":
                while self.program.get(self.pointerPosition," ") == " ":
                    self.advance()
                return self.getCommand()
            else:
                return self.program[self.pointerPosition]
    
    def processCommand(self):
        currentCommand = self.getCommand()
        if self.stringMode:
            self.string()    
        elif currentCommand in set("1234567890abcdef"):#TODO: make these into functions cuz its faster
            self.push(int(currentCommand,16))#pretty sure we should do int here
        else:
            self.functionDictionary.get(currentCommand,self.error)()     
        self.advance()
        
    def error(self):
        print("unexpected character encountered, " + str(self.getCommand()))
        exit()
    
    def advance(self):#TODO: implement lahey-space wraparound
        screenspaceDelta = (self.delta[0],-self.delta[1])#delta is stored as coordinate delta. in screenspace positive y is flipped. this affects the turning functions
        self.pointerPosition = tuple(map(lambda x,y: x+y,self.pointerPosition,screenspaceDelta))
    
    def retreat(self):#technically I dont have to implement the wraparound for this function because its internal
        self.pointerPosition = tuple(map(lambda x,y: x-y,self.pointerPosition,self.delta))

    def pop(self,n=""):#TODO: figure out how they do default n
        return self.stack[0].pop(n)
    def push(self,value):
        self.stack[0].push(value)

    #command functions    
    def add(self):
        a,b = self.pop(),self.pop()
        self.push(a+b)
    def subtract(self):
        a,b = self.pop(),self.pop()
        self.push(b-a)
    def multiply(self):
        a,b = self.pop(),self.pop()
        self.push(a*b)
    def divide(self):
        a,b = self.pop(),self.pop()
        self.push(b//a)#will error on 0 currently
    def modulus(self):
        a,b = self.pop(),self.pop()
        self.push(b%a)#will error on 0 currently
    def logicalNot(self):#not is reserved lol
        a = self.pop()
        if a==0:
            a = 1
        else:
            a = 0
        self.push(a)
    def greaterThan(self):
        a,b = self.pop(),self.pop()
        if b>a:
            self.push(1)
        else:
            self.push(0)
    def west(self):
        self.delta = self.WEST
    def east(self):
        self.delta = self.EAST
    def north(self):
        self.delta = self.NORTH
    def south(self):
        self.delta = self.SOUTH
    def randomDirection(self):
        self.delta = random.choice([self.WEST,self.EAST,self.NORTH,self.SOUTH])
    def westOrEast(self):
        a = self.pop()
        if a==0:
            self.delta = self.EAST
        else:
            self.delta = self.WEST
    def northOrSouth(self):
        a = self.pop()
        if a==0:
            self.delta = self.SOUTH
        else:
            self.delta = self.NOTH
    def string(self):
        if not self.stringMode:
            self.stringMode = True;
        else:
            currentCommand = self.getCommand()
            if currentCommand == self.stringCharacter:
                self.stringMode = False;
            else:
                self.push(ord(currentCommand))
    def duplicate(self):
        a = self.pop()
        self.push(a)
        self.push(a)
    def swap(self):
        x,y = self.pop(),self.pop()
        self.push(x)
        self.push(y)
    def intPrint(self):
        print(self.pop(),end="")
    def strPrint(self):
        print(chr(self.pop()),end="")
    def jump(self):
        self.advance()
    def put(self):
        y,x,v = self.pop(),self.pop(),self.pop()
        x,y = x+self.storageOffset[0],y+self.storageOffset[1]
        
        self.program[(x,y)] = chr(v)
    def get(self):
        y,x = self.pop(),self.pop()
        x,y = x+self.storageOffset[0],y+self.storageOffset[1]
        
        self.push(ord(self.program[(x,y)]))
    def inputNumber(self):#spec says to extract first contiguous base 10 number from input
        #msvcrt.getch() #wai wont u work
        m = re.search('\d+',input())
        self.push(int(m.group(0)))#currently errors if not found. maybe reflect()?
        
    def inputChar(self):
        #self.push(ord(msvcrt.getch()))
        self.push(ord(input()))
    def end(self):
        self.exitStateFound = True
    def noop(self):
        ""
    
    def turnLeft(self):
        x,y = self.delta
        y *= -1
        self.delta = (y,x)
    def turnRight(self):
        x,y = self.delta
        x *= -1
        self.delta = (y,x)
            
    def reverse(self):#todo: hooray, I can do lambdas. they'll be the first to go when I start optomizing
        self.delta = tuple(map(lambda x: x*-1,self.delta))
    
    def popVector(self):
        y,x = self.pop(),self.pop()
        self.delta = (x,y)
    
    def jumpOver(self):#TODO: incorporate this and space into getCommand. they take 0 ticks, and certain instructions require getCommand to return the next actual valid character
        if not self.jumpOverMode:
            self.jumpOverMode = True
        else:
            if self.getCommand() == self.jumpOverCharacter:
                self.jumpOverMode = False
    
    def jumpForward(self):
        num = self.pop()
        if num > 0:
            for i in range(0,num):
                self.advance()
        else:
            for i in range(0,num*-1):
                self.retreat()
    
    def quit(self):
        self.exitStateFound = True
        self.exitValue = self.pop()
        
    def iterate(self):
        num = self.pop()
        self.advance()
        command = self.getCommand()
        for i in range(0,num):
            self.functionDictionary[command]()
    
    def compare(self):
        b,a = self.pop(),self.pop()
        if a < b:
            self.turnLeft()
        elif a == b:
            self.noop()
        else:
            self.turnRight()
    
    #TODO: do pushthrough functions. 0-9 and a-f
    #TODO: in string mode, spaces are NOT ignored, but are truncated to a single space
    def fetchCharacter(self):
        self.advance()
        self.push(ord(self.getCommand()))
        
    def store(self):
        self.advance()
        self.program[self.pointerPosition] = chr(self.pop())
        
    def clearStack(self):
        self.stack[0]= Stack()
        
    def beginBlock(self):
        n = self.pop()
        if n < 0:
            self.stack.prepend(Stack([0]*n))
        else:
            self.stack.appendleft(Stack(self.stack[0].list[-n:]))#have to use list here for now
        self.stack[1].push(self.storageOffset[0])
        self.stack[1].push(self.storageOffset[1])
        self.storageOffset = tuple(map(lambda x,y: x+y,self.pointerPosition,self.delta))
        
    def endBlock(self):
        if len(self.stack) > 1:
            n = self.pop()
            y,x = self.stack[1].pop(),self.stack[1].pop()
            self.storageOffset = (x,y)
            if n < 0:
                for i in range(0,n):
                    self.stack[1].pop()
            else:
                self.stack[1].list += self.stack[0].list[-n:]#using list here too
            self.stack.popleft()
        else:
            self.reverse();
            
    def stackUnderStack(self):
        if len(self.stack) == 1:
            self.reverse()
        else:
            n = self.pop()
            if n > 0:
                for i in range(0,n):
                    self.push(self.stack[1].pop())
            elif n < 0:
                for i in range(0,-n):
                    self.stack[1].push(self.pop())#TODO: check if push is valid for python lists and get rid of all appends
                    #more TODO: need to create class for stacks. pop() needs to return 0 if nothing is on the stack, which it wont right now
                    
                  
    #TO BE CONTINUED
        
        
b = BefungeInterpreter()
b.verbose = False#True
b.loadASCIIFile('befunge.txt')

b.run()