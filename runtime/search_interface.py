import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from .manage import manage_search

def search_window():

    window = tk.Tk()
    window.title('Buscar alojamientos')
    window.geometry('310x200')

    city_lbl = tk.Label(window, text= 'Lugar')
    city_lbl.grid(column=0, row=0)
    city_input = tk.Entry(window,width=15, justify='center')
    city_input.grid(column=1, row=0)

    checkin_lbl = tk.Label(window, text='Fecha de ingreso')
    checkin_lbl.grid(column=0, row=1)
    checkin_format_lbl = tk.Label(window, text='YYYY-MM-DD')
    checkin_format_lbl.grid(column=2, row=1)
    checkin_input = tk.Entry(window, width=15, justify='center')
    checkin_input.grid(column=1, row=1)

    checkout_lbl = tk.Label(window, text='Fecha de salida')
    checkout_lbl.grid(column=0, row=2)
    checkout_format_lbl = tk.Label(window, text='YYYY-MM-DD')
    checkout_format_lbl.grid(column=2, row=2)
    checkout_input = tk.Entry(window, width=15, justify='center')
    checkout_input.grid(column=1, row=2)

    rooms_lbl = tk.Label(window, text='n° Dormitorios')
    rooms_lbl.grid(column=0, row=3)
    rooms_input = tk.Entry(window, width=15, justify='center')
    rooms_input.grid(column=1, row=3)

    adults_lbl = tk.Label(window, width=15, text='n° Adultos')
    adults_lbl.grid(column=0, row=4)
    adults_input = tk.Entry(window, width=15, justify='center')
    adults_input.grid(column=1, row=4)

    children_lbl = tk.Label(window, width=15, text='n° Niños')
    children_lbl.grid(column=0, row=5)
    children_input = tk.Entry(window, width=15, justify='center')
    children_input.grid(column=1, row=5)

    babies_lbl = tk.Label(window, width=15, text='n° Bebés')
    babies_lbl.grid(column=0, row=6)
    babies_input = tk.Entry(window, width=15, justify='center')
    babies_input.grid(column=1, row=6)

    void_lbl = tk.Label(window, width=15, text='')
    void_lbl.grid(column=1, row=7)

    search_btn = tk.Button(
        window,
        width=12,
        text='Buscar',
        command= lambda: manage_search(
            str(city_input.get()),
            str(checkin_input.get()),
            str(checkout_input.get()),
            int(rooms_input.get()),
            int(adults_input.get()),
            int(children_input.get()),
            int(babies_input.get()),
            )
        )
    search_btn.grid(column=1, row=8)
        
    window.mainloop()





