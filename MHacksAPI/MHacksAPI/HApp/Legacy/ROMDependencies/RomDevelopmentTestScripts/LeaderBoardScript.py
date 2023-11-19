# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 10:02:18 2022

@author: Derek Joslin
"""

import operator
import keyboard

LeaderBoardDictionary = {'Derek Joslin': 43, 'James Madison': 45, 'John Quincy Adams': 22, 'Millard Filmore ': 10, 'Harry Truman': 21, 'Warren Harding': 4, 'Martin Van Buren': 100}

while not keyboard.is_pressed('o'):
    
    name = input("Input player name: ")
    
    score = input("Input player score: ")
    
    LeaderBoardDictionary[name] = int(score)
    
    #Print Dictionary Code
    print(LeaderBoardDictionary)
    
    #List top players in order
    sortedLeaderBoard = sorted(LeaderBoardDictionary.items(), key=operator.itemgetter(1),reverse=True)
    
    
    print("\n\n\n\n\n\n\n")
    #print("Player:")
    for player in sortedLeaderBoard:
        print("{0}".format(player[0]))
        
        
    #print("Score:")
    for player in sortedLeaderBoard:
        print("{0}".format(player[1]))
        
else:
    print("\n\n\n\n\n\n\n")
    #print("Player:")
    for player in sortedLeaderBoard:
        print("{0}".format(player[0]))
        
        
    #print("Score:")
    for player in sortedLeaderBoard:
        print("{0}".format(player[1]))
    