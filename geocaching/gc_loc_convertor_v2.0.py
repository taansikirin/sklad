#############################################
# name:    gc-loc convertor                 #
# autor:   Petr Douda                       #
# date:    3.5.2010                         #
# version: 2.0                              #
# licence: GNU/GPU                          #
# side:    http://petrdouda.wordpress.com/  #
#############################################
"""
Tento skript prevadi vsechny soubory .gc v zadane slozce na do formatu .loc
opet v zadane slozce.
"""

from Tkinter import *
import os, string, tkFileDialog

def konvertGCloc(GCfolder, LOCfolder):
    files = os.listdir(GCfolder)
    for gc in files:
        gcF = open(GCfolder + "\\" + gc, "r")
        locF = open(LOCfolder + "\\" + os.path.basename(GCfolder + "\\" + gc)[:-3] + ".loc", "w")
        gcRadky = gcF.readlines()
        for gcRadek in gcRadky:
            if gcRadek.find("ORIGMENO") != -1:
                index1 = gcRadek.find("=")+1
                nazev = gcRadek[index1:].rstrip()
            if gcRadek.find("GPS") != -1:
                index2 = gcRadek.find("=")+1
                souradnice = gcRadek[index2:]
                Lat = souradnice.rstrip().split(",")[0]
                Lon = souradnice.rstrip().split(",")[1]
            if gcRadek.find("NAPOVEDA") != -1:
                index3 = gcRadek.find("=")+1
                hint = gcRadek[index3:].rstrip()
            if gcRadek.find("TEREN") != -1:
                index4 = gcRadek.find("=")+1
                teren = gcRadek[index4:].rstrip()
            if gcRadek.find("SIZE") != -1:
                index5 = gcRadek.find("=")+1
                size = gcRadek[index5:].rstrip()
            if gcRadek.find("OBTIAZNOST") != -1:
                index6 = gcRadek.find("=")+1
                obtiznost = gcRadek[index6:].rstrip()
        gcF.close()

        locF.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<loc version="1.0" src="Groundspeak">\n'
                   '<waypoint>\n'
                   '\t<name id="'+nazev+'"><![CDATA['+"velikost: "+size+", obtiznost/teren: "+obtiznost+"/"+teren+", hint: "+hint+']]></name>\n'
                   '\t<coord lat="'+Lat+'" lon="'+Lon+'"/>\n'
                   '\t<type>Geocache</type>\n'
                   '\t<link text="Cache Details">http://www.geocaching.com/seek/cache_details.aspx?wp=GCGG4A</link>\n'
                   '</waypoint></loc>')
        locF.close()

def message(text):
    global m
    m = Message(frame4, text=text, width=500)
    m.pack(side=LEFT)

def vyberGCfolder():
    global GCfolder
    GCfolder = tkFileDialog.askdirectory()
    vstup1.delete(0, END)
    vstup1.insert(0, GCfolder)

def OutputLOCfolder():
    global LOCfolder
    LOCfolder = tkFileDialog.askdirectory()
    vstup2.delete(0, END)
    vstup2.insert(0, LOCfolder)

def GO():
    m.destroy()
    try:
        konvertGCloc(GCfolder, LOCfolder)
        message("Convesion complete.")
    except:
        message("Something went wrong (gc or loc folder is not specified)!")

okno = Tk()
okno.title("Gc-loc konvertor")

frame1 = Frame(okno)
frame1.pack()
v1 = StringVar()
v1.set("Folder with GC-files")
vstup1 = Entry(frame1, textvariable=v1, width=30)
vstup1.pack(side=LEFT)
button1 = Button(frame1, text="GC folder", command=vyberGCfolder, width = 10)
button1.pack(side=RIGHT)

frame2 = Frame(okno)
frame2.pack()
v2 = StringVar()
v2.set("Output LOC folder")
vstup2 = Entry(frame2, textvariable=v2, width=30)
vstup2.pack(side=LEFT)
button2 = Button(frame2, text="LOC folder", command=OutputLOCfolder, width = 10)
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
