import platform
from tkinter import *
from tkinter import ttk
import tone_data
from tone_data import fb

import struct

def send_tone():
    print(platform.system())
    print(tone_data.get_system_exclusive().hex())

def update_bo(val):
    #global bo
    b = int(val)
    if(tone_data.bo != b):
        tone_data.bo = b
        send_tone()
    

def update_fb(val):
    b = val
    if(fb[0] != b):
        fb[0] = b
        send_tone()
    

root = Tk()
root.minsize(width=250, height=150)

frame = ttk.Frame(root, padding=1)
frame2 = ttk.Frame(
    frame, width=200, height=100,
    borderwidth=10, relief='sunken')
#スタイル
stl=ttk.Style()
stl.configure('stlSpin.TSpinbox', font=40 , arrowsize = 50)

"""
# スケールの作成
val = DoubleVar()
sc = ttk.Scale(
    frame,
    variable=val,
    orient=VERTICAL,
    #label = 'Basic Octave',
    #showvalue = True,
    length=100,
    from_=0,
    to=3,
    command=lambda e: print('val:%4d' % val.get()))
"""
# スピンボックスbo
#val_bo = StringVar()
#val_bo.set(str(tone_data.bo))
val_bo = IntVar()
b = tone_data.bo[0]
#val_bo.set(tone_data.bo[0])
val_bo.set(b)

sp = ttk.Spinbox(
    frame,
    #format='%d',
    #style= 'stlSpin.TSpinbox',
    width= 10,
    #state= 'readonly',
    textvariable=val_bo,
    from_=0,
    to=3,
    increment=1,
    command=lambda: update_bo(val_bo.get()))

# スピンボックスfb
val_fb = ['']
#val_fb[0] = StringVar()
#val_fb[0].set(str(fb[0]))
val_fb[0] = IntVar()
val_fb[0].set(fb[0])

sp_fb = ttk.Spinbox(
    frame,
    #format='%d',
    #style= 'stlSpin.TSpinbox',
    width= 10,
    #state= 'readonly',
    textvariable=val_fb[0],
    from_=0,
    to=7,
    increment=1,
    command=lambda: update_fb(val_fb[0].get()))


#sc.grid(row=0, column=0, sticky=(N, E, S, W))
sp.grid(row=0, column=1, sticky=(N, E, S, W))
sp_fb.grid(row=0, column=2, sticky=(N, E, S, W))

frame.pack()
#frame2.pack()
root.mainloop()

