import pygame
from tkinter import *
import tkinter.ttk as ttk
from subprocess import *
#window initialization
root = Tk()
root.geometry("515x340")
root.title("Setup do najznamienitszej gry")

"""
kolejność zmiennych:
name
level
fps
samolot
shot
background
speed
"""
#load data
plik = open('settings.txt', 'r')
settings = []
for line in plik.readlines():
    line = line.strip()
    settings.append(line)
plik.close()

settings[2] = int(settings[2])
name = settings[0]
level = settings[1]
fps = settings[2]
plane_style = settings[3]
shot_sound = settings[4]
background = settings[5]
player_speed = settings[6]

#functions-and-procedures
def insert_data():
    database = open('settings.txt', 'w')
    name = player_name.get()
    level = difficulty_level.get()
    fps = max_fps.get()
    samolot = styl_samolotu_value.get()
    shot = dzwiek_strzalu_value.get()
    bg = styl_tla.get()
    sp = speed.get()
    lista = [name, level, fps, samolot, shot, bg, sp]
    for zmienna in lista:
        database.write(str(zmienna) + "\n")
    database.close()
    Popen(["python", "main.py"])
    quit()

def scale_changed(ch):
    speed.set(ch)

#variables---------------------------------------------------------------------------
player_name = StringVar()
player_name.set(name)

difficulty_level = StringVar()
difficulty_level.set(level)

max_fps = IntVar()
max_fps.set(fps)

styl_samolotu_value = StringVar()
styl_samolotu_value.set(plane_style)

dzwiek_strzalu_value = StringVar()
dzwiek_strzalu_value.set(shot_sound)

styl_tla = StringVar()
styl_tla.set(background)

speed = IntVar()
speed.set(player_speed)
#variables---------------------------------------------------------------------------


#frames------------------------------------------------------------------------------
ramka_ogolna = LabelFrame(root, text="Opcje ogólne")
ramka_ogolna.grid(row=0, column=0, padx=10, pady=10)

ramka_dodatkowa = LabelFrame(root, text="Opcje dodatkowe")
ramka_dodatkowa.grid(row=1, column=0, padx=10, pady=10)
#frames------------------------------------------------------------------------------


#general-----------------------------------------------------------------------------
label_wyboru_nazwy = Label(ramka_ogolna, text="Wpisz nazwę gracza", width=28)
label_wyboru_nazwy.grid(row=0,column=0)

entry_wyboru_nazwy = Entry(ramka_ogolna, textvariable=player_name)
entry_wyboru_nazwy.grid(row=1, column=0)


label_wybory_poziomu = Label(ramka_ogolna, text="wybierz poziom trudności")
label_wybory_poziomu.grid(row=0, column=1, columnspan=3)

radio_easy = Radiobutton(ramka_ogolna, variable=difficulty_level, value="latwy", text="łatwy")
radio_normal = Radiobutton(ramka_ogolna, variable=difficulty_level, value="normalny", text="normalny")
radio_hard = Radiobutton(ramka_ogolna, variable=difficulty_level, value="trudny", text="trudny")

radio_easy.grid(row=1, column=2)
radio_normal.grid(row=1, column=3)
radio_hard.grid(row=1, column=4)

for widget in ramka_ogolna.winfo_children():
    widget.grid_configure(padx=10, pady=5)
#general-----------------------------------------------------------------------------


#additional--------------------------------------------------------------------------
label_ilosc_fps = Label(ramka_dodatkowa, text="Maksymalny fps")
label_ilosc_fps.grid(row=0, column=0)

fps_scale = Spinbox(ramka_dodatkowa, from_ = 0, to = 2000, textvariable = max_fps)
fps_scale.grid(row=1, column=0)


label_combobox_samolot = Label(ramka_dodatkowa, text="Wybierz styl samolotu")
label_combobox_samolot.grid(row=0, column=1)

combobox_samolot = ttk.Combobox(ramka_dodatkowa, textvariable = styl_samolotu_value)
combobox_samolot.grid(row=1, column=1)
combobox_samolot['values'] = ('bialy', 'brazowy', 'czarny', 'niebieski', 'polska', 'zebra')


label_combobox_strzal = Label(ramka_dodatkowa, text="Wybierz dźwięk strzału")
label_combobox_strzal.grid(row=0, column=2)

combobox_strzal = ttk.Combobox(ramka_dodatkowa, textvariable=dzwiek_strzalu_value)
combobox_strzal.grid(row=1, column=2)
combobox_strzal['values'] = ('zwykly', 'ciezki', 'lekki', 'rewolwer', 'zabka')


label_tla = Label(ramka_dodatkowa, text="Wybierz tło")
label_tla.grid(row=2, column=0)

combobox_tlo = ttk.Combobox(ramka_dodatkowa, textvariable=styl_tla)
combobox_tlo.grid(row=3, column=0)
combobox_tlo['values'] = ('tlo1', 'tlo2', 'tlo3')


label_speed = Label(ramka_dodatkowa, text="Ustaw prędkość")
label_speed.grid(row=2, column=1)

speed_scale = Scale(ramka_dodatkowa, from_=1, to=99, orient=HORIZONTAL)
speed_scale.grid(row=3, column=1)
speed_scale.config(command=scale_changed)
speed_scale.set(speed.get())


for widget in ramka_dodatkowa.winfo_children():
    widget.grid_configure(padx=10, pady=5)
#additional--------------------------------------------------------------------------


#button------------------------------------------------------------------------------
button = Button(root, text="Graj", command=insert_data)
button.grid()

root.mainloop()