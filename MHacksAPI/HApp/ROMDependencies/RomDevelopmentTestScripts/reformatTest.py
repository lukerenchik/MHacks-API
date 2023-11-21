# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 10:55:00 2022

@author: Derek Joslin
"""

nColumns = 14
nRows = 5


editorBox = []#[["" for i in range(0,nColumns)] for j in range(0,nRows)]
boundingBox = [["" for i in range(0,nColumns)] for j in range(0,nRows)]




def editorBoxFormatter(inputString):
    
    
    
    
    


def stringReformatter(testText):
    

    #go through text and add carraige every 13 characters
    newText = ""
    parseText = testText.split("\n")
    nChar = 0
    
    for characterList in parseText:
        #print(characterList)
        nChar = 0
        for character in characterList:
            #if list greater than length of braille display than add \n
            nChar = nChar + 1
            if nChar%14 == 0:
                
                newText = newText + "\n" + character
                nChar = nChar + 1
            else:
                newText = newText + character
        
        newText = newText + "\n"

    newText = newText[0:-1]
    return newText



testText = "hello my name is derek and I like to type really long run on sentences that just seem to go on forever and ever and ever like they just never ever end.\n wow! \n now that\n was a long \n sentence."#"hello world, this was a triumph\nI'm making a note here\nHuge\nSuccess"



print(testText)


print("=============================================================================")


newText = stringReformatter(testText)

print(newText)

print("=============================================================================")

newText = stringReformatter(newText)

print(newText)

print("=============================================================================")

newText = newText[:4] + 'a' + newText[4:]

newText = stringReformatter(newText)

print(newText)






