import random

class BefungePointer:

    DIRECTION = {\
      "East"  : ( 1, 0),\
      "West"  : (-1, 0),\
      "North" : ( 0, 1),\
      "South" : ( 0,-1)\
    }

    def __init__(self, position = (0,0)):
        self.position = position
        self.delta = self.directions()["East"]

    def advance(self):
        screenspaceDelta = (self.delta[0],-self.delta[1])#delta is stored as coordinate delta. in screenspace positive y is flipped. this affects the turning functions.
        self.position = tuple(map(lambda x,y: x+y,self.position,screenspaceDelta))

    def directions(self):
     return BefungePointer.DIRECTION

    def faceEast(self):
      self.delta = self.directions()["East"]

    def faceWest(self):
      self.delta = self.directions()["West"]

    def faceNorth(self):
      self.delta = self.directions()["North"]

    def faceSouth(self):
      self.delta = self.directions()["South"]

    def faceRandom(self):
      self.delta = random.choice(list(self.directions().values()))
