from random import choices, randint, randrange, random
import time

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
        return "{} (waga:{},cena:{})".format(self.nazwa,self.waga,self.cena)

things =[
    Thing('Tak', 92, 23),
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

def run_evolution(generation_limit,fitness_limit,population_size,things,weight_limit):
    population = generate_population(population_size,len(things))

    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness(genome,things,weight_limit),
            reverse=True
        )

        if fitness(population[0],things,weight_limit) >= fitness_limit:
            break

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

start = time.time()

population, generations = run_evolution(1000,740,10,things,165)

def genome_to_things(genome,things):
    result = []
    for i,thing in enumerate(things):
        if genome[i] == 1:
            result += [thing.name]

    return result

end = time.time()

print(f"number of generations: {generations}")
print(f"time: {end-start}s")
print(f"best solution: {genome_to_things(population[0], things)}")
    


    

    