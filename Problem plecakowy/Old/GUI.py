from tkinter import *

class Przedmiot:
    def __init__(self,nazwa,waga,cena):
        self.nazwa = str(nazwa)
        self.waga = float(waga)
        self.cena = float(cena)
    
    def wypisz(self):
        return "{} (waga:{},cena:{})".format(self.nazwa,self.waga,self.cena)

przedmioty = []

def dodajObiekt():
    przedmioty.append(Przedmiot(nazwaEntry.get(),wagaEntry.get(),cenaEntry.get()))
    lista.insert(END,przedmioty[-1].wypisz())
    return

def wyczysc():
    przedmioty.clear()
    lista.delete(0,END)
    return
    przedmioty.append(Przedmiot())

def start():
    for i in przedmioty:
        wypisz(i.wypisz())

# --------------------- GUI ------------------------

root = Tk()

root.title("Problem plecakowy algorytmem genetycznym - Mateusz Birkholz | Robert Chyrek")
root.configure(bg='#444444')
root.configure(padx=25, pady=25)
root.resizable(False,False)

lista = Listbox(root,width=90,height=20)
lista.grid(row=1,column=1, rowspan=1, columnspan=2)

txInfo = Text(root,state=DISABLED,height=20,width=70)
txInfo.grid(row=1,rowspan=1,column=4, columnspan=2)

def wypisz(text):
    txInfo.configure(state=NORMAL)
    txInfo.insert(index=INSERT ,chars=str(text)+"\n")
    txInfo.configure(state=DISABLED)
    return

breakLabel = Label(root,bg='#444444')
breakLabel.grid(row=1,column=3)

nazwaLabel = Label(text="Nazwa",fg='white',bg='#444444',width=15,font='Helvetica 15 bold')
nazwaLabel.grid(row=2,column=1,pady=15, padx=15)
wagaLabel = Label(text="Waga",fg='white',bg='#444444',width=15,font='Helvetica 15 bold')
wagaLabel.grid(row=3,column=1,pady=15, padx=15)
cenaLabel = Label(text="Cena",fg='white',bg='#444444',width=15,font='Helvetica 15 bold')
cenaLabel.grid(row=4,column=1,pady=15, padx=15)
plecakLabel = Label(text="Pojemność plecaka",fg='white',bg='#444444',width=15,font='Helvetica 15 bold')
plecakLabel.grid(row=2,column=4,pady=15, padx=15)
iteracjeLabel = Label(text="Liczba iteracji",fg='white',bg='#444444',width=15,font='Helvetica 15 bold')
iteracjeLabel.grid(row=3,column=4,pady=15, padx=15)

nazwaEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
nazwaEntry.grid(row=2,column=2,pady=15, padx=15)
wagaEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
wagaEntry.grid(row=3,column=2,pady=15, padx=15)
cenaEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
cenaEntry.grid(row=4,column=2,pady=15, padx=15)
plecakEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
plecakEntry.grid(row=2,column=5,pady=15, padx=15)
iteracjeEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
iteracjeEntry.grid(row=3,column=5,pady=15, padx=15)

addButton = Button(root,command=dodajObiekt,text="Dodaj",width=25,fg='white',bg='#444444',font='Helvetica 12')
addButton.grid(row=5,column=2)
clearButton = Button(root,command=wyczysc,text="Wyczyść",width=25,fg='white',bg='#444444',font='Helvetica 12')
clearButton.grid(row=5,column=1)
startButton = Button(root,command=start,text="START",width=40,fg='white',bg='#444444',font='Helvetica 12')
startButton.grid(row=5,column=4,columnspan=2)


root.mainloop()