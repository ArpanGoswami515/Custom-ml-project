import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
# as you can see, i created the classes based on the names of items. i did because it will help store the priorities according to customars.
class SleepingBag:
    def __init__(self, priority):
        self.name = "Sleeping Bag"
        self.priority = int(priority) # like here, when the customar inputs an priority, it will be stored as an object.
        self.weight = 10
# the same happened to each of the items.
class Rope:
    def __init__(self, priority):
        self.name = "Rope"
        self.priority = int(priority)
        self.weight = 3

class PocketKnife:
    def __init__(self, priority):
        self.name = "Pocket Knife"
        self.priority = int(priority)
        self.weight = 2

class Torch:
    def __init__(self, priority):
        self.name = "Torch"
        self.priority = int(priority)
        self.weight = 5

class WaterBottle:
    def __init__(self, priority):
        self.name = "Water Bottle"
        self.priority = int(priority)
        self.weight = 9

class Glucose:
    def __init__(self, priority):
        self.name = "Glucose"
        self.priority = int(priority)
        self.weight = 8

class FirstAidSupplies:
    def __init__(self, priority):
        self.name = "First Aid Supplies"
        self.priority = int(priority)
        self.weight = 6

class RainJacket:
    def __init__(self, priority):
        self.name = "Rain Jacket"
        self.priority = int(priority)
        self.weight = 3

class PersonalLocatorBeacon:
    def __init__(self, priority):
        self.name = "Personal Locator Beacon"
        self.priority = int(priority)
        self.weight = 2

def Sort(sub_li):#here it sorts the backpacks, based on efficeincy. basically just swapping j[i] and j[i+1] if j[i] is smaller
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][-1] < sub_li[j + 1][-1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li

generations = []#holds all generations - it will hold all items in one gen, for all gens
All_Items = []#Holds the objects
best_of_gen = []#holds best from each gen - holds best backpack from each generation, basically a 2d list

userName = input("Welcome to Hiking! What is your name: ")
print("Hi "+userName+"! Please rate the items as your nessecity:-")
SB = SleepingBag(input("Enter the Priority of Sleeping Bag(15 for High priority, 10 for medium priority, 5 for low priority): "))
All_Items.append(SB)
R = Rope(input("Enter the Priority of Rope(15 for High priority, 10 for medium priority, 5 for low priority): "))
All_Items.append(R)
PK = PocketKnife(input("Enter the Priority of Pocket Knife(15 for High priority, 10 for medium priority, 5 for low priority): "))
All_Items.append(PK)
T = Torch(input("Enter the Priority of Torch(15 for High priority, 10 for medium priority, 5 for low priority): "))
All_Items.append(T)
WB = WaterBottle(input("Enter the Priority of Water Bottle(15 for High priority, 10 for medium priority, 5 for low priority): "))
All_Items.append(WB)
G = Glucose(input("Enter the Priority of Glucose(15 for High priority, 10 for medium priority, 5 for low priority): "))
All_Items.append(G)
FAS = FirstAidSupplies(input("Enter the Priority of First Aid Supplies(15 for High priority, 10 for medium priority, 5 for low priority): "))
All_Items.append(FAS)
RJ = RainJacket(input("Enter the Priority of Rain Jacket(15 for High priority, 10 for medium priority, 5 for low priority): "))#taking priority and creating the object
All_Items.append(RJ)#appending objects to the all items, as it will hold the objects
PLB = PersonalLocatorBeacon(input("Enter the Priority of Personal Locator Beacon(15 for High priority, 10 for medium priority, 5 for low priority): "))
All_Items.append(PLB) 

def fitnessFunction(this_generation):

    total_priority = 0
    for o in this_generation:# here is the calculation of priority of backpack
        total_priority = total_priority + o.priority

    return total_priority

def Create_Initial_Population():

    max_weight = 30 # as given in the pdf
    global All_Items

    weight=0
    All_Items_Copy = All_Items.copy()
    this_generation = []

    while(1):
        x = random.choice(All_Items_Copy) # it will take a random item from the list
        All_Items_Copy.pop( All_Items_Copy.index(x)) #and the item will be removed, as duplication cant happen
        if(int(weight+x.weight)<=max_weight): #here it will check if the max weight is crossed
            weight = weight+x.weight
            this_generation.append(x)
        if len(All_Items_Copy)<1: # if all items are removed, or put to backpack, which is nessecery for termination
            break

    this_generation.append(fitnessFunction(this_generation))

    return this_generation

#creating 20 entries first
for i in range(20):
    x = Create_Initial_Population()
    generations.append(x)

#sorting the entries based on fitness values
Sort(generations)

#initializing the key points
no_of_parents = 12
crossover_probability = 0.5
mutation_probability = 0.1
no_of_gen = 40

def crossover(x, y):
    global generations

    father = generations[x].copy()
    mother= generations[y].copy()
    
    child1 = father.copy()#they are copying the parents, later they will crossover
    child2 = mother.copy()
    child1.pop(-1)#poping the part where the efficiency is stored
    child2.pop(-1)
    minimum_length = min(len(child1), len(child2))

    for i in range(minimum_length):#since they can be different length, least is taken
        l= [1, 0]
        x = random.choices(l, weights=(crossover_probability, 1-crossover_probability), k=1)
        if(x==1 and (child1.count(child2[i]==0)) and (child2.count(child1[i]==0))):#here, a coin toss occurs. if it is 1, the feature will be swappend, if 0 then not. and before that, the if statement checks whether it will duplicate the items or not.
            child1[i], child2[i] = child2[i], child1[i]
    
    mutation(child1, child2)

def mutation(child1, child2):
    global All_Items
    global generations

    child1_otherfeatures = set(All_Items)&set(child1)#its for not duplicating the common items
    child1_otherfeatures = sorted(child1_otherfeatures, key = lambda k : child1.index(k))#taking the features child1 dont have
    child2_otherfeatures = list(set(All_Items)&set(child2))
    child2_otherfeatures = sorted(child2_otherfeatures, key = lambda k : child2.index(k))#taking the features child1 dont have

    for i in range(len(child1)):
        l= [1, 0]
        otherfeatures_copy = child1_otherfeatures.copy()
        x = random.choices(l, weights=(mutation_probability, 1-mutation_probability), k=1)#same coin toss, but the chances are 0.01 for mutation now
        if (x==1):
            while(1):
                new_item = random.choice(otherfeatures_copy)
                otherfeatures_copy.pop(otherfeatures_copy.index(new_item))#takes a new item, and checks if the item can be taken without exceeding the limiit
                if(new_item.weight <= child1[i].weight):
                    child1[i] = new_item
                    break
                if(len(otherfeatures_copy) == 0):#if otherfeatures are empty, it will be terminated
                    break
    
    child1.append(fitnessFunction(child1))
    child2.append(fitnessFunction(child2))

    generations.append(child1)
    generations.append(child2)
    
    Sort(generations)

    best_of_gen.append(generations[0])#appending best of the children

def selection():
    global no_of_parents

    #roulette wheel selection
    x = random.randint(0, no_of_parents-1)
    y = random.randint(0, no_of_parents-1)
    while(1):
        if(x==y):
            y= random.randint(0, no_of_parents-1)
        else:
            break

    #sending the index to crossover
    crossover(x, y)

for i in range(no_of_gen):
    selection()

#printing the graph and the optimal backpack
fitness_per_gen = []
for j in best_of_gen:
    fitness_per_gen.append(j[-1])
x = np.arange(0, i+1)
y = np.array(fitness_per_gen)
plt.title("Line graph")#the plotting
plt.ylabel("Fitness")
plt.xlabel("generation")
plt.plot(x, y, color="green")
plt.show()
Sort(generations)
x=generations[0]#prints the info about the best backpack

for i in range(len(x)-1):
    print("Name: %s "% x[i].name + "Weight: %d" % x[i].weight + " Priority: %d" % x[i].priority)
print("The total efficiency is : %d" % x[-1])
