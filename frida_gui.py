try:
    from Tkinter import *
except ImportError:
    from tkinter import *

frida_gui = Tk()

save_btn = Button(frida_gui, text = 'Guardar')
open_btn = Button(frida_gui, text = 'Abrir')
frida_lbl = Label(frida_gui, text = '-FRIDA-')
frida_lbl.grid(row = 0, column=1, sticky='WENS')
save_btn.grid(row = 0, column = 0, sticky='WENS', padx=15, pady=10)
open_btn.grid(row = 0, column = 2, sticky='WENS')



text_area = Text(frida_gui, width = 90, height = 40, bd = 1, relief= GROOVE)
text_area.grid(row=1, column = 0, columnspan = 3, padx=(15, 0) , pady=5)

canvas = Canvas(frida_gui, width = 750, height = 600, bd = 1, relief = GROOVE)
canvas.grid(row = 1, column = 4, padx=(0, 5) , pady=5)

user_entry = Entry(frida_gui, state=DISABLED)
user_entry.grid(row=3, column=0, rowspan=1, columnspan=2, sticky='WENS', padx= 15)

read_btn = Button(frida_gui, state=DISABLED, text='Lee', padx=15)
read_btn.grid(row=3, column=2, sticky='WENS')

run_btn = Button(frida_gui, text = 'Frida Pinta')
run_btn.grid(row = 2, column=2, sticky='WENS')

output_lbl = Label(frida_gui, text = 'Output:')
output_lbl.grid(row = 3, column = 4, sticky = 'WNS')

output_area = Text(frida_gui, width = 20, height= 6, bd = 1, relief = GROOVE, state = DISABLED)
output_area.grid(row=5, column = 4, sticky = 'WENS', pady=(0,20), padx=(0,5))


mainloop()