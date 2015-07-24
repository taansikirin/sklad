#############################################
# name:    loc-wpt convertor                #
# autor:   Petr Douda                       #
# date:    16.1.2012                        #
# version: 2.1                              #
# licence: GNU/GPU                          #
# site:    http://petrdouda.wordpress.com/  #
#############################################

from Tkinter import *
import os, tkFileDialog

"""
Prevodnik formatu loc na format wpt. Vytvorene wayponty byly odzkouseny v aplikaci
SmartComGPS v 1.5 (1.53b) a OziExplorer (1.11/4b).
Verze 2.1 reaguje na zmenu struktury formatu loc.
"""
def konverze(txt, wpt, cesta, typLoc):
    soubortxt = open(txt, "w")
    souborwpt = open(wpt, "w")

    souborwpt.write("OziExplorer Waypoint File Version 1.1\n"
                    "WGS 84\n"
                    "Reserved 1\n"
                    "\n")

    files = os.listdir(cesta)
    for loc in files:
        if loc[-4:] == ".loc":
            print loc
            soubor_loc = open(cesta + "\\" + loc, "r")
            seznam = soubor_loc.readlines()
            prvniName=True
            for radek in seznam:
                indexR = radek.find("name")
                if indexR != -1 and prvniName:
                    prvniName=False
        #-----------tato cast prevadi locy primo stazene z geocaching.com
                    if typLoc == 1:
                        index1 = radek.find("\"") + 1
                        index2 = radek.rfind("\"")
                        kod = radek[index1:index2]
                        index3 = radek.find("[") + 7
                        index4 = radek.find("by") - 1
                        nazev = radek[index3:index4]
                        soubortxt.write(kod+"\n"+nazev+"\n")
                        souborwpt.write("-1," + nazev + ",")
        #-----------tento blok je upraven pro prevod loc souboru vytvoreneho ze souboru gc (maji nahrazeny kod nazvem kesky a nazev hintem)
                    if typLoc == 2:
                        index1 = radek.find("=") + 2
                        index2 = radek.rfind("CDATA") - 5
                        nazev = radek[index1:index2]
                        index3 = radek.find("[") + 7
                        index4 = radek.rfind("name") - 5
                        hint = radek[index3:index4]
                        soubortxt.write(nazev+"\n"+hint+"\n") 
                        souborwpt.write("-1," + nazev + ",")
        #---------------------------------------------
                if radek[2:7] == "coord" or radek[1:6] == "coord":
                    radek2 = radek.split()
                    lat = radek2[1][5:-1]
                    lon = radek2[2][5:-3]
                    if lat[5] == "-":
                        sirka = "S "
                    else:
                        sirka = "N "
                        
                    if lon[5] == "-":
                        delka = "W "
                    else:
                        delka = "E "
                        
                    soubortxt.write(sirka + lat + "\n" + delka + lon + "\n"
                                    "\n")
                    souborwpt.write(lat + "," + lon + ",\n")
            soubor_loc.close()
        else:
            pass

    soubortxt.close()
    souborwpt.close()

def vyberSlozkyLoc():
    global cesta
    cesta = tkFileDialog.askdirectory()
    vstup1.delete(0, END)
    vstup1.insert(0, cesta)

def outPut():
    global nazevSouboru
    nazevSouboru = tkFileDialog.asksaveasfilename()
    vstup2.delete(0, END)
    vstup2.insert(0, nazevSouboru)

def GO():
    m.destroy()
    try:
        wpt = nazevSouboru + ".wpt"
        txt = nazevSouboru + ".txt"
        konverze(txt, wpt, cesta, typLoc)
        message(wpt + " done!")
    except:
        message("Something went wrong (file name, loc folder or type is not specified!")
    
def radioBut():
    global typLoc
    typLoc = var.get()

def message(text):
    global m
    m = Message(frame5, text=text, width=500)
    m.pack()

okno = Tk()
okno.title("Loc-wpt konvertor")

frame1 = Frame(okno)
frame1.pack()
v1 = StringVar()
v1.set("Input folder")
vstup1 = Entry(frame1, textvariable=v1, width = 30)
vstup1.pack(side=LEFT)
button1 = Button(frame1, text = "loc folder", width = 10, command = vyberSlozkyLoc)
button1.pack(side=RIGHT)

frame2 = Frame(okno, borderwidth=2, relief=GROOVE)
frame2.pack()
var = IntVar()
Radiobutton(frame2, text="Original loc from www.geocaching.com", variable=var, value=1, command=radioBut).pack(anchor=W)
Radiobutton(frame2, text="Changed loc with my scripts", variable=var, value=2, command=radioBut).pack(anchor=W)
Radiobutton.invoke

frame3 = Frame(okno)
frame3.pack()
v2 = StringVar()
v2.set("Output name")
vstup2 = Entry(frame3, textvariable=v2, width = 30)
vstup2.pack(side=LEFT)
button2 = Button(frame3, text = "Output", width = 10, command = outPut)
button2.pack(side=RIGHT)

frame4 = Frame(okno)
frame4.pack()
button3 = Button(frame4, text = "OK", width = 10, command = GO)
button3.pack(side=LEFT)
button4 = Button(frame4, text = "Quit", width = 10, command = okno.quit)
button4.pack(side=RIGHT)

frame5 = Frame(okno, borderwidth=1, relief=GROOVE) #obsahuje message
frame5.pack(fill=X)
message("") #kvuli prvnimu kliknuti na "OK", kde se vola destroy na message

okno.mainloop()
okno.destroy()
