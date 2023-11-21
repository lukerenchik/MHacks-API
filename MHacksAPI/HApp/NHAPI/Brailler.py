# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:04:55 2022

@author: Derek Joslin
"""

import numpy as np


class Brailler():
    
    def __init__(self, data, state):
        #store the outputs for every braille character inside the brailler
        self.data = data
        self.state = state
        
        self.brailleCharacterDictionary = { " "	:	0b000000,
                                            "!"	:	0b011101,
                                            '"'	:	0b000010,
                                            "#"	:	0b001111,
                                            "$"	:	0b110101,
                                            "%"	:	0b100101,
                                            "&"	:	0b111101,
                                            "'"	:	0b001000,
                                            "("	:	0b111011,
                                            ")"	:	0b011111,
                                            "*"	:	0b100001,
                                            "+"	:	0b001101,
                                            ","	:	0b000001,
                                            "-"	:	0b001001,
                                            "."	:	0b000101,
                                            "/"	:	0b001100,
                                            "0"	:	0b001011,
                                            "1"	:	0b010000,
                                            "2"	:	0b011000,
                                            "3"	:	0b010010,
                                            "4"	:	0b010011,
                                            "5"	:	0b010001,
                                            "6"	:	0b011010,
                                            "7"	:	0b011011,
                                            "8"	:	0b011001,
                                            "9"	:	0b001010,
                                            ":"	:	0b100011,
                                            ";"	:	0b000011,
                                            "<"	:	0b110001,
                                            "="	:	0b111111,
                                            ">"	:	0b001110,
                                            "?"	:	0b100111,
                                            "@"	:	0b000100,
                                            "A"	:	0b100000,
                                            "B"	:	0b110000,
                                            "C"	:	0b100100,
                                            "D"	:	0b100110,
                                            "E"	:	0b100010,
                                            "F"	:	0b110100,
                                            "G"	:	0b110110,
                                            "H"	:	0b110010,
                                            "I"	:	0b010100,
                                            "J"	:	0b010110,
                                            "K"	:	0b101000,
                                            "L"	:	0b111000,
                                            "M"	:	0b101100,
                                            "N"	:	0b101110,
                                            "O"	:	0b101010,
                                            "P"	:	0b111100,
                                            "Q"	:	0b111110,
                                            "R"	:	0b111010,
                                            "S"	:	0b011100,
                                            "T"	:	0b011110,
                                            "U"	:	0b101001,
                                            "V"	:	0b111001,
                                            "W"	:	0b010111,
                                            "X"	:	0b101101,
                                            "Y"	:	0b101111,
                                            "Z"	:	0b101011,
                                            "a"	:	0b100000,
                                            "b"	:	0b110000,
                                            "c"	:	0b100100,
                                            "d"	:	0b100110,
                                            "e"	:	0b100010,
                                            "f"	:	0b110100,
                                            "g"	:	0b110110,
                                            "h"	:	0b110010,
                                            "i"	:	0b010100,
                                            "j"	:	0b010110,
                                            "k"	:	0b101000,
                                            "l"	:	0b111000,
                                            "m"	:	0b101100,
                                            "n"	:	0b101110,
                                            "o"	:	0b101010,
                                            "p"	:	0b111100,
                                            "q"	:	0b111110,
                                            "r"	:	0b111010,
                                            "s"	:	0b011100,
                                            "t"	:	0b011110,
                                            "u"	:	0b101001,
                                            "v"	:	0b111001,
                                            "w"	:	0b010111,
                                            "x"	:	0b101101,
                                            "y"	:	0b101111,
                                            "z"	:	0b101011,
                                            "["	:	0b010101,
                                            "\\"	:	0b110011,
                                            "]"	:	0b110111,
                                            "^"	:	0b000110,
                                            "_"	:	0b000111  }

    
    def printCharacter(self, startCoordinate, character):
        #grab the character from the dictionary
        brailleBinary = self.brailleCharacterDictionary[character]
        
        #print the binary charachter to a matrix
        brailleList = self.generateCharacterList(brailleBinary)
        
        #insert that in the state list of the device
        self.insertBrailleCharacter(startCoordinate, brailleList)
        
    def generateCharacterList(self, binaryValue):
        binaryString = bin(binaryValue)
        brailleList = [[0,0],
                       [0,0],
                       [0,0]]
        
        binaryString = binaryString.replace('0b','')
        
        #append zeros until it a binary
        if len(binaryString) < 6:
            while len(binaryString) < 6:
                binaryString = "0" + binaryString
        
        for (stringIndex, stringValue) in enumerate(binaryString):
            binaryDigit = int(stringValue)
            
            if stringIndex < 3:
                brailleList[stringIndex][0] = binaryDigit
            else:
                stringIndex = stringIndex - 3
                brailleList[stringIndex][1] = binaryDigit
        
        

        return brailleList
        
        
    def insertBrailleCharacter(self, startCoordinate, brailleList):
        #first find start coordinate dot

        for xCoordinate in range(0,2):
            for yCoordinate in range(0,3):
                output = brailleList[yCoordinate][xCoordinate]
                if output:
                    self.data[startCoordinate[1] + yCoordinate, startCoordinate[0] + xCoordinate] = 255
                else:
                    self.data[startCoordinate[1] + yCoordinate, startCoordinate[0] + xCoordinate] = 0

                self.state[startCoordinate[1] + yCoordinate][startCoordinate[0] + xCoordinate] = bool(output)



