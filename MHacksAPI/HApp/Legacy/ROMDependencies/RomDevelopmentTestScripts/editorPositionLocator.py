# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:53:54 2022

@author: Derek Joslin
"""


xPosition = 0
yPosition = 1
nColumns = 14
nRows = 5




testString = "\nthis\nisateststringtherearealotofwordstnesohusntoahusenthueoasnuteohauosnuhsnauethuesntaohuoe"




def stringPositionLocater():
        #grab the x and y display positions
        
        newLineStringList = testString.split("\n")
        
        cursorStringPosition = 0
        
        virtualXPosition = 0
        virtualYPosition = 0


        if len(newLineStringList) == 1:
            
            for character in newLineStringList[0]:
                if virtualXPosition == xPosition and virtualYPosition == yPosition:
                    break
                virtualXPosition +=1
                cursorStringPosition += 1
                if virtualXPosition > (nColumns - 1):
                    virtualXPosition = 0
                    virtualYPosition += 1
                

        else:
            for stringList in newLineStringList:
                if virtualXPosition == xPosition and virtualYPosition == yPosition:
                    break
                
                if len(stringList) < nColumns:
                    for character in stringList:    
                        if virtualXPosition == xPosition and virtualYPosition == yPosition:
                            break
                        cursorStringPosition += 1
                        virtualXPosition += 1
                    if virtualXPosition == xPosition and virtualYPosition == yPosition:
                        break
                    virtualYPosition += 1
                    cursorStringPosition = cursorStringPosition + 2
                    virtualXPosition = 0
                else:
                    for character in stringList:
                        if virtualXPosition == xPosition and virtualYPosition == yPosition:
                            break
                        if virtualXPosition > (nColumns - 1):
                            virtualXPosition = 0
                            virtualYPosition += 1
                            cursorStringPosition += 1
                        else: 
                            virtualXPosition +=1
                            cursorStringPosition += 1
        
                if virtualXPosition == xPosition and virtualYPosition == yPosition:
                    break
# =============================================================================
#                 virtualXPosition = 0
#                 virtualYPosition += 1
#                 cursorStringPosition = cursorStringPosition + 2
# =============================================================================
        
        #print(self.editor.cursor)
        #print(cursorStringPosition)
        return cursorStringPosition
        

location = stringPositionLocater()


print(location)

print(testString[location])
