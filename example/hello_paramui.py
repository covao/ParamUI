# Hello ParamUI
from paramui import paramui

ParameterTable = [
    ['A', 'Parameter A', 0.5, [0, 1, 0.1]],
    ['B', 'Parameter B This is a pen', 200, [100, 500, 10]],
    ['F1', 'Flag 1', True, []],
    ['F2', 'Flag 2', False, []],
    ['S1', 'Select 1', 'Two', ['One', 'Two', 'Three']],
    ['S2', 'Select 2', 'Three', ['One', 'Two', 'Three']],
    ['Name1', 'Name 1', 'Taro', []],
    ['Name2', 'Name 2', 'Jiro', []],
    ['File1', 'File 1', '', '*.py;*.txt'],
    ['Folder1', 'Folder 1', '', 'folder'],
    ['Run', 'Run!', False, 'button'],
]

#Define user function
def UsrFunc(Prm):
  if not Prm.Run:
    return
  print(Prm)

# Parameter display when Run button is clicked
paramui(ParameterTable, UsrFunc)
