'''
# paramui(ParameterTable, UsrFunc, ShowUI)
- Processing: Create UI from ParameterTable, assign UI parts values to Prm structure, call user function
- Input: ParameterTable, UsrFunc
  - ParameterTable: Containing the following columns  
    PrameterVariable, ParameterLabel, InitialValue, Range(Slider:[Min,Max,Step], Selecter:['A','B'...], FileName:'*.txt;*.doc',Button:'button')
  - Example: ParameterTable = [['A1','Num 1',0.5, [0, 1, 0.1]],['F1','Flag 1',True,[]],['Run','Run!',False,'button'],['S1','Select 1','Two',['One','Two','Three']],['Name','Name 1','Taro',[]], ]
    - Prm structure definition Prm.(ParameterVariable)  
      Example: Prm.A1=0.5, Prm.F1=False, Prm.Text='Taro', Prm.S1='Two', Prm.Run=True  
  - UsrFunc: Function handle Example: UsrFunc = lambda Prm:print(Prm)  
  - ShowUI: If ShowUI is False, UI is not created.
- Usage 1: Run on UI event
from paramui import paramui
paramui(ParameterTable, UsrFunc)
- Usage 2: Loop & get UI parameters  
pu = paramui(ParameterTable)
while pu.IsAlive:
    if pu.Prm.Run
       print(pu.Prm)
'''

import threading
import types
import re
import numpy as np
try: # If tkinte is not exist, skip import library
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    pass # no_library
    
class paramui:
    def close_ui(self):
        self.UsrCloseFunc()
        if self.ShowUI:
            self.root.quit()
        if not self.ThreadMode:
            try:
                self.root.destroy()
            except:
                pass
        self.IsAlive = False
# - show_ui: Optional. If False, does not create a GUI with the tkinter library.

    def __init__(self, parameter_table=[], user_func=[], show_ui=True):
        self.parameter_table = parameter_table
        self.IsAlive = False
        self.IsUserFunc = False
        self.UserFunc = user_func
        self.UsrCloseFunc = lambda: True
        self.ThreadMode = False
        self.Prm = types.SimpleNamespace()
        self.UIName = 'ParamUI'
        self.UIWidth = 500
        self.UIMaxHeight = 600
        self.UIYSpace = 45
        self.ShowUI = show_ui
        
        if user_func:
            self.IsUserFunc = True
        if parameter_table and not user_func:
            self.ThreadMode = True
            def user_func(p): return True
        if parameter_table:
            if self.ThreadMode:
                self.Thread = threading.Thread(
                    target=lambda p=parameter_table, u=user_func: self.create_ui(p, u), daemon=True)
                self.Thread.start()
                while not self.IsAlive:
                    pass
            else:
                self.IsAlive = True
                self.create_ui(parameter_table, user_func)

    def __del__(self):
        if self.IsAlive:
            self.close_ui()
        
    def is_numeric(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def update_parameter(self, variable, value):
        setattr(self.Prm, variable, value)
        self.UserFunc(self.Prm)

    def on_slider_change(self, variable, value, spin_var, step):
        v = float(value.get())
        v = round(v / step) * step
        v = round(v,  int(np.floor(-np.log10(step))))
        spin_var.set(v)
        self.update_parameter(variable, v)

    def on_spinbox_change(self, variable, value, slider_var, step):
        if self.is_numeric(value.get()):
            v = float(value.get())
            v = round(v / step) * step
            v = round(v,  int(np.floor(1-np.log10(step))))
            slider_var.set(v)
            value.set(v)
            self.update_parameter(variable, v)

    def on_checkbox_change(self, variable, value):
        self.update_parameter(variable, value)

    def on_button_change(self, variable, value):
        self.update_parameter(variable, True)
        if self.IsUserFunc:
            setattr(self.Prm, variable, [])

    def on_dropdown_change(self, variable, value):
        self.update_parameter(variable, value)

    def on_entry_change_leave(self, variable, value):
        setattr(self.Prm, variable, value)

    def on_entry_change(self, variable, value):
        self.update_parameter(variable, value)

    def browse_file(self, variable, entry_var, str):
        if str =='folder':        
            file_path = filedialog.askdirectory()
        else:
            file_path = filedialog.askopenfilename(
                filetypes=[("File", str.replace(";", " "))])
            
        if file_path:
            entry_var.set(file_path)
            self.update_parameter(variable, file_path)

    def create_ui(self, parameter_table, UserFunc):
        self.parameter_table = parameter_table
        self.UserFunc = UserFunc
        if self.ShowUI:
            self.root = tk.Tk()
            UIHeight = min(self.UIMaxHeight, len(parameter_table)*self.UIYSpace)
            self.root.geometry(str(self.UIWidth)+"x"+str(UIHeight))
            self.root.protocol("WM_DELETE_WINDOW", self.close_ui)
            self.root.title(self.UIName)
            sc = self.UIWidth / 500
    
            canvas = tk.Canvas(self.root)
            scrollbar = tk.Scrollbar(
                self.root, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units"))
            frame = tk.Frame(canvas)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.create_window((0, 0), window=frame, anchor=tk.NW)
            frame.bind("<Configure>", lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))

        for i, param in enumerate(self.parameter_table):
            variable, label, initial_value, step = param
            setattr(self.Prm, variable, initial_value)

            if self.ShowUI:
                row = tk.Frame(frame)
                UIPadY = int(max((self.UIYSpace-35)/2, 0))
                row.pack(side=tk.TOP, fill=tk.X, padx=20, pady=UIPadY, expand=True)
                if not (isinstance(initial_value, list) and not (initial_value)):
                    l = tk.Label(row, text=label, width=int(18*sc), anchor='w')
                    l.pack(side=tk.LEFT, expand=False)
                if isinstance(initial_value, (int, float)) and isinstance(step, list) and len(step)==3 :
                    min_val, max_val, step_val = step
                    var = tk.DoubleVar(self.root)
                    var.set(initial_value)
                    var2 = tk.DoubleVar(self.root)
                    var2.set(initial_value)
                    slider = tk.Scale(row, variable=var, from_=min_val, to=max_val,
                                      resolution=step_val, showvalue=0, orient=tk.HORIZONTAL, length=int(160*sc))
                    slider.bind("<ButtonRelease>", lambda event, v=variable, value=var,
                                spin_var=var2, step=step_val: self.on_slider_change(v, value, spin_var, step))
                    slider.pack(side=tk.LEFT, fill=tk.X)
    
                    spinbox = tk.Spinbox(row, textvariable=var2, from_=min_val,
                                         to=max_val, increment=step_val, width=int(10*sc))
                    spinbox.config(command=lambda v=variable, value=var2, slider_var=var,
                                   step=step_val: self.on_spinbox_change(v, value, slider_var, step))
                    spinbox.bind("<Return>", lambda event, v=variable, value=var2, slider_var=var,
                                 step=step_val: self.on_spinbox_change(v, value, slider_var, step))
                    spinbox.pack(side=tk.RIGHT, fill=tk.X)
    
                elif isinstance(initial_value, bool) and not step:
                    var = tk.BooleanVar(self.root)
                    var.set(initial_value)
                    checkbox = tk.Checkbutton(
                        row, variable=var, command=lambda v=variable, value=var: self.on_checkbox_change(v, value.get()))
                    checkbox.pack(side=tk.LEFT, fill=tk.X, expand=False)
    
                elif isinstance(initial_value, bool) and step=='button':
                    var = tk.BooleanVar(self.root)
                    var.set(initial_value)
                    button = tk.Button(row, text=label, command=lambda v=variable,
                                       value=var: self.on_button_change(v, True))
                    button.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
                elif isinstance(initial_value, str) and not (isinstance(step, list) and len(step) > 1):
                    var = tk.StringVar(self.root)
                    var.set(initial_value)
                    entry = tk.Entry(row, textvariable=var)
                    entry.bind("<Leave>", lambda _, v=variable,
                               value=var: self.on_entry_change_leave(v, value.get()))
                    entry.bind("<Return>", lambda _, v=variable,
                               value=var: self.on_entry_change(v, value.get()))
                    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
                    if isinstance(step, str) and re.match('\*\.|folder', step):
                        browse_button = tk.Button(row, text="Browse",
                                                  command=lambda v=variable, entry_var=var, str=step: self.browse_file(v, entry_var, str))
                        browse_button.pack(side=tk.RIGHT, padx=(0, 10))
    
                elif isinstance(step, list) and step:
                    var = tk.StringVar(self.root)
                    var.set(initial_value)
                    dropdown = tk.OptionMenu(row, var,  *step, command=lambda _,
                                             var=variable, value=var: self.on_dropdown_change(var, value.get()))
                    dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
        self.UserFunc(self.Prm)
        self.IsAlive = True
        if self.ShowUI:
            self.root.mainloop()
    