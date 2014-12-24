'''
Created on Nov 14, 2013

@author: RSHELDON
'''

import csv
class BefungeConverter:
    def __init__(self):
        pass

    def ASCIIToCSV(self,file):
        with open(file) as f:
            for line in f.readlines():
                print(line.replace('','\t'))

    def stringToCSV(self,string):
        print(string.replace('','\t'))

    def CSVToASCII(self,filePath):
        with open(filePath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            for row in reader:
                continue

