# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 11:36:05 2023

@author: Derek Joslin

"""

from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

class DLatchSimulator:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.circuit = Circuit('D Latch Simulation')
        self.libraries = SpiceLibrary('lib')
        # Define subcircuit
        subcircuit = Circuit('DLATCH')
        subcircuit.add_transistor('M1', 'D', 'n1', 'VDD', model='nmos')
        subcircuit.add_transistor('M2', 'n1', 'Q', 'VDD', model='nmos')
        subcircuit.add_transistor('M3', 'D', 'n2', 'GND', model='pmos')
        subcircuit.add_transistor('M4', 'n2', 'Qn', 'GND', model='pmos')
        subcircuit.add_resistor('RD', 'n1', 'GND', 1@megohm)
        subcircuit.add_resistor('RU', 'n2', 'VDD', 1@megohm)
        self.circuit.subcircuit(subcircuit)

        # Create D input and clock signals
        for i in range(self.m):
            for j in range(self.n):
                self.circuit.V(f'D{i}_{j}', f'D{i}_{j}', self.circuit.gnd, 'dc 0V')

        self.circuit.PulseVoltageSource('CLK', 'CLK', self.circuit.gnd, 0@us, 1@us, 10@ns, 10@ns, 100@ns, 1@us)

        # Create D Latches
        for i in range(self.m):
            for j in range(self.n):
                self.circuit.subcircuit(self.latch_model, f'LATCH_{i}_{j}',
                                        D=f'D{i}_{j}', Q=f'Q{i}_{j}', Qn=f'Qn{i}_{j}', CLK='CLK')

        self.simulator = self.circuit.simulator()

    def set_pulsewidth(self, pulsewidth):
        self.circuit['CLK'].rise_time = pulsewidth
        self.circuit['CLK'].fall_time = pulsewidth

    def set_setup_hold_time(self, setup_time, hold_time):
        for i in range(self.m):
            for j in range(self.n):
                self.circuit['LATCH_{}_{}'.format(i, j)].set_parameter('setup_time', setup_time)
                self.circuit['LATCH_{}_{}'.format(i, j)].set_parameter('hold_time', hold_time)

    def run_simulation(self, d_values):
        for i in range(self.m):
            for j in range(self.n):
                self.circuit[f'D{i}_{j}'].dc_value = d_values[i][j]

        self.simulator.reset()
        self.simulator.run()

        results = []
        for i in range(self.m):
            row = []
            for j in range(self.n):
                q_value = self.simulator.evaluate(f'Q{i}_{j}')
                row.append(q_value)
            results.append(row)

        return results

if __name__ == '__main__':
    m = 19
    n = 41
    sim = DLatchSimulator(m, n)
    sim.set_pulsewidth(50@ns)
    sim.set_setup_hold_time(10@ns, 10@ns)

    # Example input matrix with alternating 0s and 1s
    d_values = [[(i+j) % 2 for j in range(n)] for i in range(m)]

    output = sim.run_simulation(d_values)

    print("Output:")
    for row in output:
        print(row)