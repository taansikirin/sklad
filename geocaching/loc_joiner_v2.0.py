#############################################
# name:    loc joiner                       #
# autor:   Petr Douda                       #
# date:    3.5.2010                         #
# version: 2.0                              #
# licence: GNU/GPU                          #
# site:    http://petrdouda.wordpress.com/  #
#############################################

"""
Tento skript spojuje soubory formatu loc do jednoho. Tim je usnadneno nahrani kesek
napriklad do mobilni navigacni aplikace TerkBuddy.
"""
from Tkinter import *
import os, tkFileDialog

def LOCjoin(locFile, LOCfolder):
    locF = open(locFile + ".loc", "w")
    locF.write('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<loc version="1.0" src="Groundspeak">\n'
               '<waypoint>\n')

    files = os.listdir(LOCfolder)
    pocetSouboru = len(files)
    cisloSouboru = 0
    for loc in files:
        cisloSouboru += 1
        soubor_loc = open(LOCfolder + "\\" + loc, "r")
        seznam = soubor_loc.readlines()
        pocetRadku = len(seznam)
        cisloRadku = 0
        for radek in seznam:
            cisloRadku += 1
            if cisloRadku < 4:
                continue
            elif cisloRadku == pocetRadku and cisloSouboru != pocetSouboru:
                locF.write(radek[:-6]+"<waypoint>\n")
            else:
                locF.write(radek.rstrip()+"\n")
        soubor_loc.close()
    locF.close()

def message(text):
    global m
    m = Message(frame4, text=text, width=500)
    m.pack(side=LEFT)

def vyberLOCfolder():
    global LOCfolder
    LOCfolder = tkFileDialog.askdirectory()
    vstup1.delete(0, END)
    vstup1.insert(0, LOCfolder)

def OutputLOCname():
    global locFile
    locFile = tkFileDialog.asksaveasfilename()
    vstup2.delete(0, END)
    vstup2.insert(0, locFile)
    
def GO():
    m.destroy()
    try:
        LOCjoin(locFile, LOCfolder)
        message("Joining complete.")
    except:
        message("Something went wrong (output file name or loc folder is not specified)!")

okno = Tk()
okno.title("LOC joiner")

frame1 = Frame(okno)
frame1.pack()
v1 = StringVar()
v1.set("Folder with LOC files")
vstup1 = Entry(frame1, textvariable=v1, width=30)
vstup1.pack(side=LEFT)
button1 = Button(frame1, text="LOC folder", command=vyberLOCfolder, width = 10)
button1.pack(side=RIGHT)

frame2 = Frame(okno)
frame2.pack()
v2 = StringVar()
v2.set("Output name of joined LOC")
vstup2 = Entry(frame2, textvariable=v2, width=30)
vstup2.pack(side=LEFT)
button2 = Button(frame2, text="LOC name", command=OutputLOCname, width = 10)
button2.pack(side=RIGHT)

frame3 = Frame(okno)
frame3.pack()
buttonOK = Button(frame3, text="OK", command=GO, widt=10)
buttonOK.pack(side=LEFT)
buttonKill = Button(frame3, text="Quit", command=okno.quit, widt=10)
buttonKill.pack(side=RIGHT)

frame4 = Frame(okno, borderwidth=1, relief=GROOVE)
frame4.pack(fill=X)
message("") #kvuli prvnimu kliknuti na "OK", kde se vola destroy na message

okno.mainloop()
okno.destroy()
