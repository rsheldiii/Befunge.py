'''
Stack wrapper around python List class to make it funge compliant.
empty lists error when popped; funge requires a value of 0 to be returned
'''
class BefungeStack:

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
            self.list.pop(n)#will error if you try to pop past the end of the stack. need to check spec on this
    def peek(self):
      return self.list[-1]

    def __getitem__(self,i):
        return self.list[i]

    def __repr__(self):
        return str(self.list)
