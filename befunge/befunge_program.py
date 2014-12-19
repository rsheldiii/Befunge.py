import sys,random,re
from collections import deque
from befunge.befunge_stack import BefungeStack

class BefungeProgram:
    def __init__(self):
        self.stringModeCharacter = '"'
        self.commentModeCharacter = ';'
        self.primitives = set("1234567890abcdef")

        self.setFunctionDictionary()

        self.EAST = (1,0)
        self.WEST = (-1,0)
        self.NORTH = (0,1)
        self.SOUTH = (0,-1)
        self.initProgram()

    def initProgram(self): # deals with the initialization of the program itself and not just state. TODO check if I can put the state somewhere else, like statics, as it will never change
        self.data = {}
        self.tick = 0
        self.stack = deque([BefungeStack()]) #stack of stacks for holding data
        self.delta = self.EAST

        self.exitStateFound = False # tells the program to exit. not sure why I did it this way, i'll have to check
        self.pointerPosition = (0,0) # position of instruction pointer
        self.exitValue = 0 # for errors, returns at program exit
        self.storageOffset = (0,0) # I believe the offset at which put and get commands operate

    def __getitem__(self,index):
      return self.data.get(index," ") # TODO abstracted this out, might not want to

    def __setitem__(self, index, value):
      self.data[index] = value # TODO abstracted this out, might not want to

    def getCommand(self):
      return self[self.pointerPosition]

    def proceed(self):#TODO wanted to name tick
        self.tick +=1
        currentCommand = self.getCommand()

        if currentCommand in self.primitives:#TODO: optimize
            self.stackPush(int(currentCommand,16))
        else:
            self.functionDictionary.get(currentCommand,self.error)()
        self.advance()

    def error(self):
        print("unexpected character encountered, '" + str(self.getCommand()) + "' at " + str(self.pointerPosition))
        exit()

    def advance(self): #TODO: implement lahey-space wraparound
        screenspaceDelta = (self.delta[0],-self.delta[1])#delta is stored as coordinate delta. in screenspace positive y is flipped. this affects the turning functions.
        self.pointerPosition = tuple(map(lambda x,y: x+y,self.pointerPosition,screenspaceDelta))
        return self.getCommand()

    def retreat(self):
        self.pointerPosition = tuple(map(lambda x,y: x-y,self.pointerPosition,self.delta))

    def stackPop(self,n=""): #TODO: figure out how they do default n
        return self.stack[0].pop(n)

    def stackPush(self,value):
        self.stack[0].push(value)

    def stackPeek(self): #not a funge command
        return self.stack[0].peek()

    #command functions
    def add(self):
        a,b = self.stackPop(),self.stackPop()
        self.stackPush(a+b)

    def subtract(self):
        a,b = self.stackPop(),self.stackPop()
        self.stackPush(b-a)

    def multiply(self):
        a,b = self.stackPop(),self.stackPop()
        self.stackPush(a*b)

    def divide(self):
        a,b = self.stackPop(),self.stackPop()
        self.stackPush(b//a)#will error on 0 currently

    def modulus(self):
        a,b = self.stackPop(),self.stackPop()
        self.stackPush(b%a)#will error on 0 currently

    def logicalNot(self):#not is reserved lol
        a = self.stackPop()
        if a==0:
            a = 1
        else:
            a = 0
        self.stackPush(a)

    def greaterThan(self):
        a,b = self.stackPop(),self.stackPop()
        if b>a:
            self.stackPush(1)
        else:
            self.stackPush(0)

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
        a = self.stackPop()
        if a==0:
            self.delta = self.EAST
        else:
            self.delta = self.WEST

    def northOrSouth(self):
        a = self.stackPop()
        if a==0:
            self.delta = self.SOUTH
        else:
            self.delta = self.NORTH

    def stringMode(self):#fast forwards execution to next seen stringMode character, stackPushing all interim characters onto the stack on the way and compressing all spacesw
        currentCommand = self.advance()

        while currentCommand != self.stringModeCharacter:
            if self.stackPeek != " " or currentCommand != " " :
                self.stackPush(ord(currentCommand))

            currentCommand = self.advance()

    def commentMode(self):
        currentCommand = self.advance()
        while currentCommand != self.commentModeCharacter:
            currentCommand = self.advance()

    def duplicate(self):
        a = self.stackPop()
        self.stackPush(a)
        self.stackPush(a)

    def swap(self):
        x,y = self.stackPop(),self.stackPop()
        self.stackPush(x)
        self.stackPush(y)

    def intPrint(self):
        print(self.stackPop(), end="")

    def strPrint(self):
        print(chr(self.stackPop()), end="")

    def jump(self):
        self.advance()

    def put(self):
        y,x,v = self.stackPop(),self.stackPop(),self.stackPop()
        x,y = x+self.storageOffset[0],y+self.storageOffset[1]

        self[(x,y)] = chr(v)

    def get(self):
        y,x = self.stackPop(),self.stackPop()
        x,y = x+self.storageOffset[0],y+self.storageOffset[1]

        self.stackPush(ord(self[(x,y)]))

    def inputNumber(self):#spec says to extract first contiguous base 10 number from input

        m = re.search('\d+',input())
        self.stackPush(int(m.group(0)))#currently errors if not found. maybe reflect()?

    def inputChar(self):
        a = input()#TODO errors on null input
        self.stackPush(ord(a))

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

    def stackPopVector(self):
        y,x = self.stackPop(),self.stackPop()
        self.delta = (x,y)

    def jumpOver(self):#TODO: incorporate this and space into getCommand. they take 0 ticks, and certain instructions require getCommand to return the next actual valid character
        if not self.jumpOverMode:
            self.jumpOverMode = True
        else:
            if self.getCommand() == self.jumpOverCharacter:
                self.jumpOverMode = False

    def jumpForward(self):
        num = self.stackPop()
        if num > 0:
            for i in range(0,num):
                self.advance()
        else:
            for i in range(0,num*-1):
                self.retreat()

    def quit(self):
        self.exitStateFound = True
        self.exitValue = self.stackPop()

    def iterate(self):
        num = self.stackPop()
        self.advance()
        command = self.getCommand()
        for i in range(0,num):
            self.functionDictionary[command]()

    def compare(self):
        b,a = self.stackPop(),self.stackPop()
        if a < b:
            self.turnLeft()
        elif a == b:
            self.noop()
        else:
            self.turnRight()

    #TODO: do stackPushthrough functions? 0-9 and a-f

    def fetchCharacter(self):
        self.advance()
        self.stackPush(ord(self.getCommand()))

    def store(self):
        self.advance()
        self[self.pointerPosition] = chr(self.stackPop())

    def clearStack(self):
        self.stack[0]= Stack()

    def beginBlock(self):
        n = self.stackPop()
        if n < 0:
            self.stack.prepend(Stack([0]*n))
        else:
            self.stack.appendleft(Stack(self.stack[0].list[-n:]))#have to use list here for now
        self.stack[1].stackPush(self.storageOffset[0])
        self.stack[1].stackPush(self.storageOffset[1])
        self.storageOffset = tuple(map(lambda x,y: x+y,self.pointerPosition,self.delta))# I hate python lambda syntax

    def endBlock(self):
        if len(self.stack) > 1:
            n = self.stackPop()
            y,x = self.stack[1].stackPop(),self.stack[1].stackPop()
            self.storageOffset = (x,y)
            if n < 0:
                for i in range(0,n):
                    self.stack[1].stackPop()
            else:
                self.stack[1].list += self.stack[0].list[-n:]#using list here too
            self.stack.stackPopleft()
        else:
            self.reverse();

    def stackUnderStack(self):
        if len(self.stack) == 1:
            self.reverse()
        else:
            n = self.stackPop()
            if n > 0:
                for i in range(0,n):
                    self.stackPush(self.stack[1].stackPop())
            elif n < 0:
                for i in range(0,-n):
                    self.stack[1].stackPush(self.stackPop())

    def setFunctionDictionary(self):
        #down here to make class prettier
        #using sublimes sorting _almost_ works
        self.functionDictionary = {\
              '!' : self.logicalNot,\
              '"' : self.stringMode,\
              '#' : self.jump,\
              '$' : self.stackPop,\
              '%' : self.modulus,\
              '&' : self.inputNumber,\
              '*' : self.multiply,\
              '+' : self.add,\
              ',' : self.strPrint,\
              '-' : self.subtract,\
              '.' : self.intPrint,\
              '/' : self.divide,\
              ':' : self.duplicate,\
              ';' : self.commentMode,\
              '<' : self.west,\
              '=' : self.noop,\
              '>' : self.east,\
              '?' : self.randomDirection,\
              '@' : self.end,\
              '[' : self.turnLeft,\
              '\'': self.fetchCharacter,\
              '\\': self.swap,\
              ']' : self.turnRight,\
              '^' : self.north,\
              '_' : self.westOrEast,\
              '`' : self.greaterThan,\
              'g' : self.get,\
              'h' : self.noop,\
              'i' : self.noop,\
              'j' : self.jumpForward,\
              'k' : self.iterate,\
              'l' : self.noop,\
              'm' : self.noop,\
              'n' : self.clearStack,\
              'o' : self.noop,\
              'p' : self.put,\
              'q' : self.quit,\
              'r' : self.reverse,\
              's' : self.noop,\
              't' : self.noop,\
              'u' : self.stackUnderStack,\
              'V' : self.south,\
              'v' : self.south,\
              'w' : self.compare,\
              'x' : self.stackPopVector,\
              'z' : self.noop,\
              '{' : self.beginBlock,\
              '|' : self.northOrSouth,\
              '}' : self.endBlock,\
              '~' : self.inputChar,\
              ' ' : self.noop\
          }
#TO BE CONTINUED
"""unimplemented functions:
\' fetch character
( load semantics
) unload semantics
= Execute
h go high
i input file
l go low
m high/low if
o output file
s store character
t split
y get sysInfo

unimplemented features:
lahey-space wraparound
3d vectors and similar
concurrent funge
um... other stuff

note that just because it isn't on this list doesn't mean it's completely finished
"""
