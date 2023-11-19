# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:45:18 2023

@author: Derek Joslin

"""

import asyncio
import bleak

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
