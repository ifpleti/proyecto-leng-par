import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

window.title('Proyecto Lenguajes y paradigmas')

window.geometry('600x400')

# --- functions ---

def on_button():
    print('ChecboxBox:')
    for i, var in enumerate(cb_vars):
        if var.get():
            print('option:', OPTIONS[i])

# --- main ---

OPTIONS = ["Apartamento entero","Hostal","Pieza","Hotel"]
category_input = []
choice_title = tk.Label(window, width=15, text='Escoja las categorias que desea en su busqueda:')
choice_title.grid(column=1, row=9)
for i,x in enumerate(OPTIONS):
    var = tk.BooleanVar(value=False)
    category_input.append(var)
    c = tk.Checkbutton(window, text=x, variable=var)
    c.grid(column=1, row =10+i)


# --- others ---

b = tk.Button(root, text='OK', command=on_button)
b.pack(fill='x')

root.mainloop()