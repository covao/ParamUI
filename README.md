[Japanese(Google Translate)](https://github-com.translate.goog/covao/ParamUI?_x_tr_sl=en&_x_tr_tl=ja&_x_tr_hl=ja&_x_tr_pto=wapp)

# ParamUI Python  
- Create App with UI from simple parameter table
- Easy code generation using ChatGPT

# Instalation
## Method 1
- Install library in python environment
~~~
pip install git+https://github.com/covao/ParamUI

~~~
## Method 2
- Download [paramui.py](./paramui/paramui.py) and copy to the folder where you run the python script 

# Usage
## Parameter table definition
Parameter table is containing the following columns  
- Prameter Variable
- Parameter Label
- Initial Value
- Range 
 - Slider: <code>[Min, Max, Step]</code>
 - Check Box: <code>[]</code>
 - Selecter: <code>['A','B'...]</code>
 - Edit Box: <code>[]</code>
 - File Selecter: <code> '\*.txt;*.\doc' </code>
 - Folder Selecter: <code>'folder'</code>
 - Button: <code>'button'</code>

~~~ python
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

~~~
## Example 1: Run on UI event
~~~ python
from paramui import paramui
def usrfunc(Prm):
    if not Prm.Run:
        return
    print(Prm)
paramui(ParameterTable, usrfunc)

~~~
## Example 2: Loop & Get Parameters
~~~ python
from paramui import paramui
import time
pu = paramui(ParameterTable)
while pu.IsAlive:
    print(pu.Prm)
    time.sleep(0.5)
    
~~~

## Hello ParamUI
- [hello_paramui.py](./example/hello_paramui.py)  
![Hello ParamUI](./img/hello_paramui.jpg)

# [ParamUI Prompt Designer](https://covao.github.io/ParamUI/html/paramui_prompt_designer.html)
- Generate prompt of UI app using LLM
Try prompt! e.g. ChatGPT, Bing Chat, Bard  
[Start ParamUI Prompt Designer](https://covao.github.io/ParamUI/html/paramui_prompt_designer.html)

# Demo
- [Lifegame](./example/lifegame_paramui.py)
- [Mandelblot](./example/mandelbrot_paramui.py)

# Related Sites
- [ParamUI MATLAB](https://github.com/covao/ParamUI_MATLAB)

