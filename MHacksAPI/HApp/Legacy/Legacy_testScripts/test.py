
"""
Test file for HapticsEngine
- Enter "COM" for connected device below.
"""

import HapticsEngine as he


# Initialize device
engine = he.HapticsEngine("COM3")


# Print true if COM connection is successfully made
print("COM Connection:")
print(engine.comLink_check())

# Get the number of rows and columns of the tactile displah
engine.pull_displaySize()

# print the number of rows and columns
size = engine.return_displaySize()
print("Tactile Display Dimensions:")
print(size)

# return the desiredState matrix, initalized as all 0s
desired = engine.return_desiredState()
print("Desired State Matrix:")
engine.display_matrix(desired)


# Set a new value for the desiredState matrix
engine.set_desiredState([[1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
                         [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
                         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
                         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
                         [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
                         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
                         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
                         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
                         [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, ],
                         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                         [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, ],
                         [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, ],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, ],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]])

# print the new desiredState matrix
desired = engine.return_desiredState()
print("Desired State Matrix:")
engine.display_matrix(desired)

# push the desiredState from above to the tactile display
engine.push_desiredState()

# parse the embedded device for its current state and save to currentState
engine.pull_currentState()

# print the currentState matrix
current = engine.return_currentState()
print("Current State Matrix:")
engine.display_matrix(current)

# turn COM connection off
engine.comLink_off()
print("COM connection:")
print(engine.comLink_check())

