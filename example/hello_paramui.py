"""
Simple ParamUI example.
Demonstrates hierarchical parameters, flags, selectors, file/folder selection, and a run button.
"""

import time
from paramui import paramui

# Parameter table for ParamUI
ParameterTable = [
    ['Config/Threshold', 'Threshold', 0.7, [0, 1, 0.01]],           # numeric (hierarchical)
    ['Config/MaxCount', 'Max Count', 100, [10, 500, 10]],           # numeric (hierarchical)
    ['Flags/Enable', 'Enable', True, []],                           # flag (hierarchical)
    ['Flags/Debug', 'Debug Mode', False, []],                       # flag (hierarchical)
    ['Options/Mode', 'Mode', 'Auto', ['Auto', 'Manual', 'Test']],   # selector (hierarchical)
    ['Files/Input', 'Input File', '', '*.csv;*.txt'],               # file (hierarchical)
    ['Files/Output', 'Output Folder', '', 'folder'],                # folder (hierarchical)
    ['Run', 'Run!', False, 'button'],                               # run button
]

def UsrFunc(Prm):
    """
    User function called when Run button is pressed.
    Prints the current parameter values.
    """
    if not Prm.Run:
        return
    print(Prm)

pu = paramui(ParameterTable)

# Main loop: update parameters and call user function when Run is pressed
while pu.IsAlive:
    pu.update_prm()
    if pu.Prm.Run:
        UsrFunc(pu.Prm)
        pu.Prm.Run = False
    time.sleep(0.1)
