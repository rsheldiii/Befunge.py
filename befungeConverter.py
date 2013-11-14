'''
Created on Nov 14, 2013

@author: RSHELDON
'''


class Converter:
    def __init__(self):
        pass
        
    def file(self,file):
        with open(file) as f:
            for line in f.readlines():
                print(line.replace('','\t'))
    def string(self,string):
        print(string.replace('','\t'))
