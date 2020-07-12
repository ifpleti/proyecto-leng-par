import tkinter as tk
from tkinter import ttk
from .manage import manage_search
from datetime import date, timedelta

def search_window():

    window = tk.Tk()
    window.title('Buscar alojamiento')
    window.geometry('350x280')
    window.resizable(False, False)

    city_lbl = tk.Label(window, text= 'Lugar')
    city_lbl.grid(column=0, row=1, sticky='E', padx=10, pady=2)
    city_input = tk.Entry(window, justify='center', width=15)
    city_input.grid(column=1, row=1, columnspan=3)

    today = date.today()
    d1 = today.strftime("%d")
    m1 = today.strftime("%m")
    y1 = today.strftime("%Y")

    checkin_lbl = tk.Label(window, text='CheckIn')
    checkin_lbl.grid(column=0, row=2, sticky='E', padx=10, pady=2)
    checkin_input_d = tk.Entry(window, justify='center', width=3)
    checkin_input_d.grid(column=1, row=2, stick='W')
    checkin_input_d.insert(0, d1)
    checkin_input_m = tk.Entry(window, justify='center', width=3)
    checkin_input_m.grid(column=2, row=2)
    checkin_input_m.insert(0, m1)
    checkin_input_y = tk.Entry(window, justify='center', width=5)
    checkin_input_y.grid(column=3, row=2, stick='E')
    checkin_input_y.insert(0, y1)

    tomorrow = date.today() + timedelta(days=1)
    d2 = tomorrow.strftime("%d")
    m2 = tomorrow.strftime("%m")
    y2 = tomorrow.strftime("%Y")

    checkout_lbl = tk.Label(window, text='CheckOut')
    checkout_lbl.grid(column=0, row=3, sticky='E', padx=10, pady=2)
    checkout_input_d = tk.Entry(window, justify='center', width=3)
    checkout_input_d.grid(column=1, row=3, stick='W')
    checkout_input_d.insert(0, d2)
    checkout_input_m = tk.Entry(window, justify='center', width=3)
    checkout_input_m.grid(column=2, row=3)
    checkout_input_m.insert(0, m2)
    checkout_input_y = tk.Entry(window, justify='center', width=5)
    checkout_input_y.grid(column=3, row=3, stick='E')
    checkout_input_y.insert(0, y2)

    rooms_lbl = tk.Label(window, text='Dormitorios')
    rooms_lbl.grid(column=0, row=4, sticky='E', padx=10, pady=2)
    rooms_input = tk.Entry(window, justify='center', width=15)
    rooms_input.grid(column=1, row=4, columnspan=3)

    adults_lbl = tk.Label(window, text='Adultos')
    adults_lbl.grid(column=0, row=5, sticky='E', padx=10, pady=2)
    adults_input = tk.Entry(window, justify='center', width=15)
    adults_input.grid(column=1, row=5, columnspan=3)

    children_lbl = tk.Label(window, text='Niños')
    children_lbl.grid(column=0, row=6, sticky='E', padx=10, pady=2)
    children_input = tk.Entry(window, justify='center', width=15)
    children_input.grid(column=1, row=6, columnspan=3)

    babies_lbl = tk.Label(window, text='Bebés')
    babies_lbl.grid(column=0, row=7, sticky='E', padx=10, pady=2)
    babies_input = tk.Entry(window, justify='center', width=15)
    babies_input.grid(column=1, row=7, columnspan=3)

    search_btn = tk.Button(
        window,
        width=10,
        text='Buscar',
        command= lambda: check_input(
            city_input.get(),
            checkin_input_y.get(),
            checkin_input_m.get(),
            checkin_input_d.get(),
            checkout_input_y.get(),
            checkout_input_m.get(),
            checkout_input_d.get(),
            rooms_input.get(),
            adults_input.get(),
            children_input.get(),
            babies_input.get(),
            window,
            today
            )
        )
    search_btn.grid(column=1, columnspan=3, row=9, pady=4, padx=4)
        
    window.mainloop()

def check_input(city, checkin_y, checkin_m, checkin_d,
checkout_y, checkout_m, checkout_d, rooms, adults, children, babies, window, today):

    valid = True

    if all(x.isalpha() or x.isspace() for x in city) and len(city) > 3:
        city_input = tk.Label(window, text= 'check!', fg="green")
        city_input.grid(column=4, row=1, sticky='W', padx=10, pady=2)
    else:
        city_input = tk.Label(window, text= 'mínimo 4 letras o espacios', fg="red")
        city_input.grid(column=4, row=1, sticky='W', padx=10, pady=2)
        valid = False

    today = today.strftime("%Y-%m-%d")
    try:
        checkin = str(checkin_y)+'-'+str(checkin_m)+'-'+str(checkin_d)
        checkout = str(checkout_y)+'-'+str(checkout_m)+'-'+str(checkout_d)
        if today <= checkin and checkin < checkout:
            try:
                int(checkin_y)
                int(checkin_m)
                int(checkin_d)
                checkin_input = tk.Label(window, text= 'check!', fg="green")
                checkin_input.grid(column=4, row=2, sticky='W', padx=10, pady=2)
            except:
                checkin_input = tk.Label(window, text= 'fecha inválida', fg="red")
                checkin_input.grid(column=4, row=2, sticky='W', padx=10, pady=2)
                valid = False
            try:
                int(checkout_y)
                int(checkout_m)
                int(checkout_d)
                checkout_input = tk.Label(window, text= 'check!', fg="green")
                checkout_input.grid(column=4, row=3, sticky='W', padx=10, pady=2)
            except:
                checkout_input = tk.Label(window, text= 'fecha inválida', fg="red")
                checkout_input.grid(column=4, row=3, sticky='W', padx=10, pady=2)
                valid = False
            
        else:
            checkout_input = tk.Label(window, text= 'fecha inválida', fg="red")
            checkout_input.grid(column=4, row=3, sticky='W', padx=10, pady=2)
            checkin_input = tk.Label(window, text= 'fecha inválida', fg="red")
            checkin_input.grid(column=4, row=2, sticky='W', padx=10, pady=2)
            valid = False
    except:
        checkout_input = tk.Label(window, text= 'fecha inválida', fg="red")
        checkout_input.grid(column=4, row=3, sticky='W', padx=10, pady=2)
        checkin_input = tk.Label(window, text= 'fecha inválida', fg="red")
        checkin_input.grid(column=4, row=2, sticky='W', padx=10, pady=2)
        valid = False
        

    
            

    try:
        int(rooms)
        rooms_input = tk.Label(window, text= 'check!', fg="green")
        rooms_input.grid(column=4, row=4, sticky='W', padx=10, pady=2)
    except:
        rooms_input = tk.Label(window, text= 'Solo números', fg="red")
        rooms_input.grid(column=4, row=4, sticky='W', padx=10, pady=2)
        valid = False

    try:
        int(adults)
        adults_input = tk.Label(window, text= 'check!', fg="green")
        adults_input.grid(column=4, row=5, sticky='W', padx=10, pady=2)
    except:
        adults_input = tk.Label(window, text= 'Solo números', fg="red")
        adults_input.grid(column=4, row=5, sticky='W', padx=10, pady=2)
        valid = False

    try:
        int(children)
        children_input = tk.Label(window, text= 'check!', fg="green")
        children_input.grid(column=4, row=6, sticky='W', padx=10, pady=2)
    except:
        children_input = tk.Label(window, text= 'Solo números', fg="red")
        children_input.grid(column=4, row=6, sticky='W', padx=10, pady=2)
        valid = False

    try:
        int(babies)
        babies_input = tk.Label(window, text= 'check!', fg="green")
        babies_input.grid(column=4, row=7, sticky='W', padx=10, pady=2)
    except:
        babies_input = tk.Label(window, text= 'Solo números', fg="red")
        babies_input.grid(column=4, row=7, sticky='W', padx=10, pady=2)
        valid = False


    if valid == True:
        results = manage_search(city, checkin, checkout, int(rooms), int(adults), int(children), int(babies))
        show_results1 = tk.Label(window, text=results)
        show_results1.grid(column=0, row=10, columnspan=6, padx=10, pady=2)
        show_results2 = tk.Label(window, text='Resultados guardados en generated.txt', fg="green")
        show_results2.grid(column=0, row=11, columnspan=6, padx=10, pady=2)


