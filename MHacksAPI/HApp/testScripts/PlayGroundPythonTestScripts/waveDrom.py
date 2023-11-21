# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 14:40:00 2023

@author: derek
"""

import wavedrom

execution_timing = {
    "signal": [
        {"name": "executeOnFlags", "wave": "x01x01x01x01", "data": ["met", "not met"]},
        {"name": "executeDelay", "wave": "0.5ms", "data": ["start"]},
        {"name": "executeContinuously", "wave": "x01x01x01x01", "data": ["True", "False"]},
        {"name": "executeIntervalTime", "wave": "1ms", "data": ["interval"]},
        {"name": "executeTimeLimit", "wave": "10ms", "data": ["limit"]},
        {"name": "stopExecuteOnFlags", "wave": "x01x01x01x01", "data": ["met", "not met"]},
        {"name": "stopExecuteDelay", "wave": "0.5ms", "data": ["stop"]}
    ],
    "foot": {
        "executeOnFlags": "met/not met",
        "executeDelay": "start (0.5ms)",
        "executeContinuously": "True/False",
        "executeIntervalTime": "interval (1ms)",
        "executeTimeLimit": "limit (10ms)",
        "stopExecuteOnFlags": "met/not met",
        "stopExecuteDelay": "stop (0.5ms)"
    }
}

wavedrom.render(execution_timing)
