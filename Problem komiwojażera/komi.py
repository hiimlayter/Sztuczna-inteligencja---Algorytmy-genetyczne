from random import sample, choices, randint, randrange, random
from math import sqrt
import time
from tkinter import *

class Miasto:
    def __init__(self,nazwa,x,y):
        self.name = str(nazwa)
        self.x = float(x)
        self.y = float(y)

    def getName(self):
        return self.name
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def wypisz(self):
        return "{} ({},{})".format(self.name,self.x,self.y)

'''
miasta =[
    Miasto('1', -0.0000000400893815, 0.0000000358808126),
    Miasto('2', -28.8732862244731230, -0.0000008724121069),
    Miasto('3', -79.2915791686897506, 21.4033307581457670),
    Miasto('4', -14.6577381710829471, 43.3895496964974043),
    Miasto('5', -64.7472605264735108, -21.8981713360336698),
    Miasto('6', -29.0584693142401171, 43.2167287683090606),
    Miasto('7', -72.0785319657452987, -0.1815834632498404),
    Miasto('8', -36.0366489745023770, 21.6135482886620949),
    Miasto('9', -50.4808382862985496, -7.3744722432402208),
    Miasto('10', -50.5859026832315024, 21.5881966132975371),
    Miasto('11', -0.1358203773809326, 28.7292896751977480),
    Miasto('12', -65.0865638413727368, 36.0624693073746769),
    Miasto('13', -21.4983260706612533, -7.3194159498090388),
    Miasto('14', -57.5687244704708050, 43.2505562436354225),
    Miasto('15', -43.0700258454450875, -14.5548396888330487)
]
'''

miasta = [
    Miasto('1',835,98),
    Miasto('2',930,356),
    Miasto('3',825,805),
    Miasto('4',716,143),
    Miasto('5',396,333),
    Miasto('6',110,348),
    Miasto('7',124,307),
    Miasto('8',405,873),
    Miasto('9',154,529)
]

#Tworzy listę chromosomów i zwraca ją
def generate_genome(length):
    numbers = [i for i in range(length)]
    return sample(numbers,k=length)

#Tworzy liste genotypów
def generate_population(size,genome_length):
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome,things):
    if len(genome) != len(things):
        raise ValueError("Gon musi posiadać tyle chromosomów co obiektów")

    a = things[genome[0]].getX()-things[genome[-1]].getX()
    b = things[genome[0]].getY()-things[genome[-1]].getY()

    value = sqrt((a**2)+(b**2))

    for i in range(len(things)-1):
        a = things[genome[i]].getX()-things[genome[i+1]].getX()
        b = things[genome[i]].getY()-things[genome[i+1]].getY()
        value += sqrt((a**2)+(b**2))

    return value

def selection_pair(population,things):
    return choices(
        population,
        weights=[fitness(genome,things) for genome in population],
        k=2
    )

def crossover(a,b):
    if len(a) != len(b):
        raise ValueError("Geny muszą być tej samej długości")

    length = len(a)
    if length < 2:
        return a,b

    p1 = a[0:int(len(a)/2)+1]
    for i in range(len(a)):
        if b[i] not in p1:
            p1+=[b[i]]
        
    p2 = b[0:int(len(b)/2)+1]
    for i in range(len(b)):
        if a[i] not in p2:
            p2+=[a[i]]

    return p1, p2

def mutation(genome,num=1,probability=0.3):
    for _ in range(num):
        indexy = [i for i in range(len(genome))]
        index = sample(indexy,k=2)

        if random() < probability:
            x1 = genome[index[0]]
            x2 = genome[index[1]]
            genome[index[0]]=x2
            genome[index[1]]=x1

        return genome

def run_evolution(generation_limit,population_size,things):
    population = generate_population(population_size,len(things))

    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness(genome,things)
        )

        next_generation = population[0:2]

        for j in range(int(len(population)/2)-1):
            parents = selection_pair(population,things)
            offspring_a, offspring_b = crossover(parents[0],parents[1])
            offspring_a = mutation(offspring_a)
            offspring_b = mutation(offspring_b)
            next_generation += [offspring_a,offspring_b]

        population = next_generation

    population = sorted(
        population,
        key=lambda genome: fitness(genome,things)
    )
    return population, i

def genome_to_distance(genome,things):
    return fitness(genome,things)

def genome_to_names(genome,things):
    result = []
    for i in genome:
        result += [things[i].getName()]

    result += [things[genome[0]].getName()]

    return result

def start_genetic(iterations,generation_size):
    start = time.time()

    population, generations = run_evolution(iterations,generation_size,miasta)

    end = time.time()

    wypisz(f"Liczba generacji: {generations+1}")
    wypisz(f"Czas wykonywania: {end-start}s")
    wypisz(f"Wartość rozwiązania: {genome_to_distance(population[0], miasta)}")
    wypisz(f"Najlepsze rozwiązanie: {genome_to_names(population[0],miasta)}")

def dodajObiekt():
    try:
        miasta.append(Miasto(nazwaEntry.get(),float(xEntry.get()),float(yEntry.get())))
        lista.insert(END,miasta[-1].wypisz())
    except:
        wypisz("Błąd! Niewłaściwe dane obiektu!")
    return

def wyczysc():
    miasta.clear()
    lista.delete(0,END)
    return

# --------------------- GUI ------------------------

root = Tk()

root.title("Problem komiwojażera algorytmem genetycznym - Mateusz Birkholz | Robert Chyrek")
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
xLabel = Label(text="X",fg='white',bg='#444444',width=15,font='Helvetica 15 bold')
xLabel.grid(row=3,column=1,pady=15, padx=15)
yLabel = Label(text="Y",fg='white',bg='#444444',width=15,font='Helvetica 15 bold')
yLabel.grid(row=4,column=1,pady=15, padx=15)
iteracjeLabel = Label(text="Liczba iteracji",fg='white',bg='#444444',width=15,font='Helvetica 15 bold')
iteracjeLabel.grid(row=3,column=4,pady=15, padx=15)
generacjeLabel = Label(text="Osobników w generacji",fg='white',bg='#444444',width=20,font='Helvetica 15 bold')
generacjeLabel.grid(row=4,column=4,pady=15, padx=15)

nazwaEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
nazwaEntry.grid(row=2,column=2,pady=15, padx=15)
xEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
xEntry.grid(row=3,column=2,pady=15, padx=15)
yEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
yEntry.grid(row=4,column=2,pady=15, padx=15)
iteracjeEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
iteracjeEntry.grid(row=3,column=5,pady=15, padx=15)
generacjeEntry = Entry(root,fg='white',bg='#444444',width=20,font='Helvetica 15')
generacjeEntry.grid(row=4,column=5,pady=15, padx=15)

addButton = Button(root,command=dodajObiekt,text="Dodaj",width=25,fg='white',bg='#444444',font='Helvetica 12')
addButton.grid(row=5,column=2)
clearButton = Button(root,command=wyczysc,text="Wyczyść",width=25,fg='white',bg='#444444',font='Helvetica 12')
clearButton.grid(row=5,column=1)

def start():

    try:
        iteracje = int(iteracjeEntry.get())
        generacje = int(generacjeEntry.get())

        start_genetic(iteracje,generacje)
        wypisz("\n")
    except:
        if len(miasta)<=0:
            wypisz("Brak obiektów!")
        wypisz("Błąd! Niepoprawne dane!\n")

startButton = Button(root,command=start,text="START",width=40,fg='white',bg='#444444',font='Helvetica 12')
startButton.grid(row=5,column=4,columnspan=2)


root.mainloop()


    


    

    