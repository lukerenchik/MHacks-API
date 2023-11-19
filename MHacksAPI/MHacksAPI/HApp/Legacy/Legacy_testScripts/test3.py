
# -*- coding: utf-8 -*
"""
Created on Tue Apr 27 12:56:28 2021

@author: Derek Joslin
"""

import NHAPI as nh



engine = nh.NHAPI()


engine.comLink_on("COM5", 0)


print(engine.comLink_check())

engine.pull_displaySize()


size = engine.return_displaySize()


desired = engine.return_desiredState()


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


engine.push_desiredState()


engine.pull_currentState()


current = engine.return_currentState()


print(engine.comLink_check())


engine.comLink_off()

