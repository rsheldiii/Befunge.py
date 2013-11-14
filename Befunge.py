'''
Created on Jun 13, 2013

@author: RSHELDON

we store the array internally in rows. externally there should be no evidence of this
'''
import sys,random,csv
class BefungeInterpreter:
    def __init__(self):
        self.program = {}
        self.direction = '>';
        self.stack = []
        self.stringMode = False
        self.exitStateFound = False
        self.stringCharacters = ['"','”','�']
        self.functionDictionary = {\
                                   '+' : self.add, '-' : self.subtract, '*' : self.multiply, '/' : self.divide,\
                                   '%' : self.modulus, '!' : self.logicalNot, '`' : self.greaterThan,\
                                   '>' : self.right, '<' : self.left, '^' : self.up, 'V' : self.down, 'v' : self.down, '?' : self.randomDirection,\
                                   '_' : self.rightOrLeft, '|' : self.upOrDown,\
                                   ':' : self.duplicate, '\\' : self.swap, '$' : self.pop, '.' : self.intPrint, ',' : self.strPrint,\
                                   '#' : self.jump, 'p' : self.put, 'g' : self.get,\
                                   '&' : self.inputNumber, '~' : self.inputChar, '@' : self.end, ' ' : self.noop\
                                   }# ” for CSV file
        
        for character in self.stringCharacters:
            self.functionDictionary[character] = self.string
        
        self.stringMode = False;
        
        
        if __name__ == "__main__":
            if '-f' in sys.argv:
                self.loadASCIIFile(sys.argv[sys.argv.index('-f')+1])
            if '-c' in sys.argv:
                self.loadCSVFile(sys.argv[sys.argv.index('-c')+1])
        
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
                if '-v' in sys.argv:
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
            if ('-v' in sys.argv):
                currentCommand = self.getChar()
                print(self.stack)
                print("direction: " +self.direction)
                print("pointer position: " + str(self.pointerPosition))
                print("current command: " + currentCommand)
            self.processCommand()
            
    def getChar(self):
        x,y = self.pointerPosition
        return self.program.get((x,y)," ")#default nonentered value is space
    
    def processCommand(self):
        currentCommand = self.getChar()
        if self.stringMode:
            self.string()    
        elif currentCommand.isdigit():#TODO: figure out if int() returns 0 on failure
            self.stack.append(int(currentCommand))#pretty sure we should do int here
        elif currentCommand in self.functionDictionary:#NO PREMATURE OPTIMIZATION
            #print(self.functionDictionary[currentCommand])
            self.functionDictionary[currentCommand]()
        else:
            print("unexpected character encountered, " + str(currentCommand))
            exit()
        self.advance()
    
    def advance(self):
        def up():
            self.pointerPosition = tuple(map(sum,zip((0,-1),self.pointerPosition)))
        def down():
            self.pointerPosition = tuple(map(sum,zip((0,1),self.pointerPosition)))
        def left():
            self.pointerPosition = tuple(map(sum,zip((-1,0),self.pointerPosition)))
        def right():
            self.pointerPosition = tuple(map(sum,zip((1,0),self.pointerPosition)))
        {'>' : right , 'V' : down , '<' : left, '^' : up }.get(self.direction)()





    #command functions    
    def add(self):
        a,b = self.pop(),self.pop()
        self.stack.append(a+b)
    def subtract(self):
        a,b = self.pop(),self.pop()
        self.stack.append(b-a)
    def multiply(self):
        a,b = self.pop(),self.pop()
        self.stack.append(a*b)
    def divide(self):
        a,b = self.pop(),self.pop()
        self.stack.append(b//a)#will error on 0 currently
    def modulus(self):
        a,b = self.pop(),self.pop()
        self.stack.append(b%a)#will error on 0 currently
    def logicalNot(self):#not is reserved
        a = self.pop()
        if a==0:
            a = 1
        else:
            a = 0
        self.stack.append(a)
    def greaterThan(self):
        a,b = self.pop(),self.pop()
        if b>a:
            self.stack.append(1)
        else:
            self.stack.append(0)
    def left(self):
        self.direction = '<'
    def right(self):
        self.direction = '>'
    def up(self):
        self.direction = '^'
    def down(self):
        self.direction = 'V'
    def randomDirection(self):
        self.direction = random.choice(['>','V','<','^'])
    def rightOrLeft(self):
        a = self.pop()
        if a==0:
            self.direction = '>'
        else:
            self.direction = '<'
    def upOrDown(self):
        a = self.pop()
        if a==0:
            self.direction = 'V'
        else:
            self.direction = '^'
    def string(self):
        if not self.stringMode:
            self.stringMode = True;
        else:
            currentCommand = self.getChar()
            if currentCommand in self.stringCharacters:
                self.stringMode = False;
            else:
                self.stack.append(ord(currentCommand))
    def duplicate(self):
        a = self.pop()
        self.stack.append(a)
        self.stack.append(a)
    def swap(self):
        temp = self.stack[-1]
        self.stack[-1] = self.stack[-2]
        self.stack[-2] = temp
    def pop(self):
        try:
            return self.stack.pop()
        except: return 0
    def intPrint(self):
        print(self.pop())
    def strPrint(self):
        print(chr(self.pop()),end="")
    def jump(self):
        self.advance()
    def put(self):
        y,x,v = self.pop(),self.pop(),self.pop()
        self.program[(x,y)] = chr(v)
    def get(self):
        y,x = self.pop(),self.pop()
        self.stack.append(ord(self.program[(x,y)]))
    def inputNumber(self):
        print("input a number")
        self.stack.append(int(input()))
    def inputChar(self):
        print("input a character")
        self.stack.append(ord(input()))
    def end(self):
        self.exitStateFound = True
    def noop(self):
        ""
    
        
        
b = BefungeInterpreter()

b.loadCSVFile('befunge.csv')
b.run()