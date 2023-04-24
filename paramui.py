# ParamUI(ParameterTable, usrFunc)
# - Process: Create UI based on ParameterTable, assign UI parts values to Prm structure by class, call user function with Prm
# - Input: ParameterTable, usrFunc 
#  - ParameterTable: A table containing the following columns: PrameterVariable, ParameterLabel, InitialValue, Min, Max, Step    -Example: ['A', 'Parameter A', 0.5, 0, 1, 0.1;'F1', 'Flag 1', true,[],[],[];'S1', 'Select 1', 'Two',[],[],['One','Two','Three']]
#  - Prm structure definition Prm.(ParameterVariable) Example: Prm.A=12, Prm.F1=false Prm.S1='Two' Member is ParameterVariable only,   
#  - usrFunc: Function handle Example: usrFunc = lambda Prm:print(Prm.A)import tkinter as tk

import tkinter as tk
import types

def ParamUI(parameter_table, user_func):
    Prm = types.SimpleNamespace()

    root = tk.Tk()
    root.title("ParamUI")
    
    def update_parameter(variable, value):
        setattr(Prm, variable, value)
        user_func(Prm)
        
    def on_slider_change(variable, step, event):
        value = round(float(event) / step) * step
        update_parameter(variable, value)

    def on_checkbox_change(variable, value):
        update_parameter(variable, bool(value.get()))

    def on_dropdown_change(variable, value):
        update_parameter(variable, value.get())


    for i, param in enumerate(parameter_table):
        variable, label, initial_value, min_val, max_val, step = param

        setattr(Prm, variable, initial_value)

        row = tk.Frame(root)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        label = tk.Label(row, text=label, width=25)
        label.pack(side=tk.LEFT)

        if isinstance(max_val and initial_value, (int, float)):
            slider = tk.Scale(row, from_=min_val, to=max_val, resolution=step, orient=tk.HORIZONTAL, command=lambda event, var=variable, step=step: on_slider_change(var, step, event))
            slider.set(initial_value)
            slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        elif isinstance(initial_value, bool):
            var = tk.BooleanVar()
            var.set(initial_value)
            checkbox = tk.Checkbutton(row, variable=var, command=lambda var=variable, value=var: on_checkbox_change(var, value))
            checkbox.pack(side=tk.LEFT)

        elif isinstance(step, list):
            var = tk.StringVar()
            var.set(initial_value)
            dropdown = tk.OptionMenu(row, var, *step, command=lambda _, var=variable, value=var: on_dropdown_change(var, value))
            dropdown.pack(side=tk.LEFT)

    root.mainloop()
