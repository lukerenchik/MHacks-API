# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:09:05 2021

@author: Derek Joslin
"""

import NHAPI as nh


engine = nh.NHAPI()

engine.connect("COM12", 1)

engine.rect((0,0),(18,18))

engine.desired()

engine.refresh()

engine.state()

engine.disconnect()