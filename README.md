# ParamUI

ParamUI is a Python framework for easy parameter management and GUI creation. It automatically generates a Tkinter-based GUI from a ParameterTable and synchronizes values with a nested Prm structure.

## ✨ Features
- Auto-generates GUI from Parameter Table
- Easy generation of the GUI using LLMs such as ChatGPT
- Parameters are mapped to a nested Prm structure
- Tree navigation using path syntax
- Supports slider, selector, button, checkbox, file browser, and textbox widgets
- Scrollable UI for large parameter sets
- Headless mode is supported for testing without a GUI

## 📦 Installation
### Method 1: Install using pip:
```bash
pip install git+https://github.com/covao/ParamUI
```
### Method 2: Download the source code
Download [paramui.py](./paramui/paramui.py) and place it in your project directory

### Uninstall
```bash
pip uninstall paramui
```

## 📋 Example
~~~python
from paramui import paramui
import time
# Example parameter table
ParameterTable = [
    ['A1','Num A1',0.5, [0, 1, 0.1]], # pu.Prm.A1
    ['Options/Flag1','Flag 1',True,[]], # pu.Prm.Options.Flag1
    ['Run','Run!',False,'button'], # pu.Prm.Run
    ['Options/Select1','Select 1','Two',['One','Two','Three']], # pu.Prm.Options.Select1
    ['Name1','Name 1','Taro',[]] # pu.Prm.Name1
]

# Create paramui instance
pu = paramui(ParameterTable)
while pu.IsAlive:
    pu.update_prm()  # Update Prm Variables from UI
    if  pu.Prm.Run:  # If Run button is pressed
        print("Run button pressed!")
        pu.Prm.Run = False  # Reset button state of the Prm Variable
        print(f"Name:", pu.Prm.Name1, ", Options/Flag:", pu.Prm.Options.Flag1, ", Options/Select:", pu.Prm.Options.Select1, ", A1:", pu.Prm.A1)
    time.sleep(0.1) # Prevent busy-waiting
print("paramui finished.")
~~~

![ParamUI Example](./paramui_example.gif)

## Parameter Table Structure
"Parameter Table" is a list that manages parameters to be displayed in the UI.
 - 'Path of parameter', 'Display Name', Default_value, Range or options
- Example:
```python
ParameterTable = [
    ['A1', 'Num 1', 0.5, [0, 1, 0.1]],  # Slider with range [min, max, step]
    ['Run', 'Run!', False, 'button'],  # Button
    ['Flag', 'Flag 1', True, []],  # Checkbox
    ['Text', 'Text Input', 'ABC', []],  # Textbox
    ['Options/File', 'File Path', '*.txt', 'file'],  # File browser
    ['Options/Selector', 'Select Option', 'Option1', ['Option1', 'Option2', 'Option3']],  # Selector with options
    # Add more parameters as needed
]
```
 
## API Reference
- paramui(parameter_table, show_ui=True): Create the parameter UI and structure. If `show_ui` is False, runs in headless mode.
- close_ui(): Close the UI window.
- update_prm(): Synchronize UI values to Prm structure.
- Prm: Nested parameter structure.
- IsAlive: True if the UI is running.

## 🎬 Demonstrations
- [Hello World](./example/hello_world.py)
- [Life game simulation](./example/lifegame_paramui.py)
- [Mandelbrot set generation](./example/mandelbrot_paramui.py)

