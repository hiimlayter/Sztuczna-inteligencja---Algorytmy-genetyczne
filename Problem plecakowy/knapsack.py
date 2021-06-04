from random import choices, randint, randrange, random
import time
from tkinter import *

class Thing:
    def __init__(self,nazwa,cena,waga):
        self.name = str(nazwa)
        self.weight = float(waga)
        self.value = float(cena)

    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value

    def getWeight(self):
        return self.weight
    
    def wypisz(self):
        return "{} (waga:{},cena:{})".format(self.name,self.weight,self.value)


things =[
    Thing('Tak1', 92, 23),
    Thing('Tak2', 57, 31),
    Thing('Tak3', 49, 29),
    Thing('Tak4', 68, 44),
    Thing('Nie5', 60, 53),
    Thing('Tak6', 43, 38),
    Thing('Nie7', 67, 63),
    Thing('Nie8', 84, 85),
    Thing('Nie9', 87, 89),
    Thing('Nie10', 72, 82),
]

#things=[]

#Tworzy listę chromosomów i zwraca ją
def generate_genome(length):
    return choices([0,1],k=length)

#Tworzy liste genotypów
def generate_population(size,genome_length):
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome,things,weight_limit):
    if len(genome) != len(things):
        raise ValueError("Gon musi posiadać tyle chromosomów co obiektów")

    weight = 0
    value = 0

    for i,thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.getWeight()
            value += thing.getValue()

            if weight > weight_limit:
                return 0

    return value

def selection_pair(population,things,weight_limit):
    return choices(
        population,
        weights=[fitness(genome,things,weight_limit) for genome in population],
        k=2
    )

def crossover(a,b):
    if len(a) != len(b):
        raise ValueError("Geny muszą być tej samej długości")

    length = len(a)
    if length < 2:
        return a,b

    p = randint(1,length-1)
    return a[0:p]+b[p:], b[0:p]+a[p:]

def mutation(genome,num=1,probability=0.5):
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index]-1)
        return genome

def run_evolution(generation_limit,population_size,things,weight_limit):
    population = generate_population(population_size,len(things))

    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness(genome,things,weight_limit),
            reverse=True
        )

        next_generation = population[0:2]

        for j in range(int(len(population)/2)-1):
            parents = selection_pair(population,things,weight_limit)
            offspring_a, offspring_b = crossover(parents[0],parents[1])
            offspring_a = mutation(offspring_a)
            offspring_b = mutation(offspring_b)
            next_generation += [offspring_a,offspring_b]

        population = next_generation

    population = sorted(
        population,
        key=lambda genome: fitness(genome,things,weight_limit),
        reverse=True
    )
    return population, i

def genome_to_value(genome,things):
    result = 0
    for i,thing in enumerate(things):
        if genome[i] == 1:
            result += thing.value

    return result

def genome_to_things(genome,things):
    result = []
    for i,thing in enumerate(things):
        if genome[i] == 1:
            result += [thing.name]

    return result

def start_genetic(iterations,generation_size,knapsack_weight):
    start = time.time()

    population, generations = run_evolution(iterations,generation_size,things,knapsack_weight)

    end = time.time()

    wypisz(f"Liczba generacji: {generations+1}")
    wypisz(f"Czas wykonywania: {end-start}s")
    wypisz(f"Wartość rozwiązania: {genome_to_value(population[0], things)}")
    wypisz(f"Najlepsze rozwiązanie: {genome_to_things(population[0], things)}")

def dodajObiekt():
    try:
        things.append(Thing(nazwaEntry.get(),int(cenaEntry.get()),int(wagaEntry.get())))
        lista.insert(END,things[-1].wypisz())
    except:
        wypisz("Błąd! Niewłaściwe dane obiektu!")
    return

def wyczysc():
    things.clear()
    lista.delete(0,END)
    return
    przedmioty.append(Przedmiot())

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
generacjeLabel = Label(text="Osobników w generacji",fg='white',bg='#444444',width=20,font='Helvetica 15 bold')
generacjeLabel.grid(row=4,column=4,pady=15, padx=15)

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
        weight = int(plecakEntry.get())

        start_genetic(iteracje,generacje,weight)
        wypisz("\n")
    except:
        if len(things)<=0:
            wypisz("Brak obiektów!")
        wypisz("Błąd! Niepoprawne dane!\n")

startButton = Button(root,command=start,text="START",width=40,fg='white',bg='#444444',font='Helvetica 12')
startButton.grid(row=5,column=4,columnspan=2)


root.mainloop()


    


    

    