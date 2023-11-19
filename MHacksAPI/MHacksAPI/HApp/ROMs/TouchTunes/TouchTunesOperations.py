# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:27:39 2023

@author: Derek Joslin

"""

import RomAPI as rs

class TunesGraphicsRender(rs.RomOperation):
    
    def __init__(self, name, TactileDisplay, TunesFlag, TouchTunesModel):
        
        super().__init__(name)
        
        # inputs to the operation
        self.TunesFlag = TunesFlag
        self.inputDictionary["Tunes Flag"] = self.TunesFlag
        
        self.TouchTunesModel = TouchTunesModel
        self.inputDictionary["Tunes Model"] = self.TouchTunesModel
        
        # outputs to the operation
        self.TactileDisplay = TactileDisplay
        self.outputDictionary[self.TactileDisplay.name] = self.TactileDisplay
        
        executionParameters = {
            "executeOnFlags": [self.TunesFlag], # a set of flag dependencies that when met start executing the Operation
            "executeDelay": 0, # a delay in milliseconds that starts the execution of the Operation after the flag dependencies have been met
        }
        
        self.setExecutionParameters(executionParameters)
        
        # provide a description
        self.description = "This operation refreshs the display when physics are updated. It's execution is interuppt based."
        
        self.executable = self.execute
        
        self.createDebugString()
        
    def checkFlagConditions(self):
        # grab the state of ToolFlag
        updateState = self.TunesFlag.state
        
        # get the current state of the tactile display
        #currentState = self.TactileDisplay.return_currentState()
        if updateState:
            # compare the flag matrix to the current state of the Tactile Display
            self.TunesFlag.setState(0)
            return True
        else:
            # if they are not the same then return false
            return False
        
    def execute(self):
        
        try:
            
            
            if self.TunesFlag.gameState == "Start Menu":
                self.renderBars()        
                self.updateDisplay()
            else:
                self.renderExitScreen()
        
        
        except Exception as e:
            print(e)
        
    def renderBars(self):
        self.TactileDisplay.clear()
        brailleCellHeight = 4
        brailleCellWidth = 3
        
        xStartPosition = 0
        yPosition = 1 + brailleCellHeight*0
        xEndPosition = 14 * brailleCellWidth
        
        self.TactileDisplay.stroke(3)
        for index,barLength in enumerate(self.TouchTunesModel.bars):
            xStartPosition = 0
            yPosition = 1 + brailleCellHeight*index
            if barLength > 0:
                xEndPosition = ((barLength)  * brailleCellWidth) - 1
                self.TactileDisplay.line((yPosition, xStartPosition), (yPosition, xEndPosition))
            
    def renderExitScreen(self):
        """ exit screen  """
        print("Bye-Bye")
        self.TactileDisplay.braille((0,0),"Bye-Bye")
        self.TactileDisplay.desired()
        self.TactileDisplay.refresh()
        self.TactileDisplay.state()
        
    def updateDisplay(self):
        """ communicate with peripherals """
        self.TactileDisplay.desired()
        self.TactileDisplay.refresh()
        
        self.TactileDisplay.state()
        
    def stopOperation(self):
        # delete the timer for the operation by running the super class function
        super().stopOperation()
        
        # mark isStopped as false so the function is not killed
        self.isStopped = False
        
class TunesFlag(rs.RomFlag):
    
    def __init__(self, name):
        super().__init__(name)
        self.debugString = "This flag indicates if the state of the bars has changed."
        self.gameState = "Start Menu"
        self.barSelectedIndex = 0
        self.barLength = 0
        
    def createDebugString(self):
        barSelectedString = "current bar selected: {}".format(self.barSelectedIndex)
        barLengthString = "length of bar selected: {}".format(self.barLength)
        
        self.debugString = barSelectedString + "\n" + barLengthString
        
    def setState(self, state):
        super().setState(state)
        self.createDebugString()