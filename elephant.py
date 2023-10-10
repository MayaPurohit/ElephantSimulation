'''Maya Purohit
Project05
CS 152A
elephant.py
10/19/22
The purpose of this code is to create a simualtion to represent elephants and determine how two different controlling methods impact the population size.
To open this file in the Python Terminal, direct the terminal to the Project 05 folder using the cd command
Enter py and elephant.py from the Project05 folder along with a probability of darting parameter'''

import sys
import stats
import random

IDXCalvingInterval = 0 #index values for the parameters of the function 
IDXPercentDarted = 1
IDXJuvenileAge = 2
IDXMaximumAge = 3
IDXProbCalfSurv = 4
IDXProbAdultSurv = 5
IDXProbSeniorSurv = 6
IDXCarryingCapacity = 7
IDXNumYears = 8

IDXGender = 0 #index values for the attributes of an elephant 
IDXAge = 1
IDXMonthsPregnant = 2
IDXMonthsContraceptiveRemaining = 3

def newElephant(parameters, age):
    elephant = [0,0,0,0]
    gender = ["m", "f"]
    elephant[IDXGender] = random.choice(gender) #randomly chooses a gender
    
    elephant[IDXAge] = age #sets the age of the elephant to the parameter

    if (elephant[IDXGender] == "f"): #determines if a female elephant is pregnant and if she is, how far along she is 
        if(elephant[IDXAge] > parameters[IDXJuvenileAge]) and (elephant[IDXAge] <= parameters[IDXMaximumAge]):
            probofPregnancy = 1.0/parameters[IDXCalvingInterval]
            if(random.random() < probofPregnancy): #determines if they are pregnant
                elephant[IDXMonthsPregnant] = random.randint(1,22) #determines how far along they are
    return elephant

def initPopulation(parameters):
    population = [] #new list
    for i in range(parameters[IDXCarryingCapacity]): #adds penguins until it is at the maximum capacity of the ecosystem
        population.append(newElephant(parameters, random.randint(1, parameters[IDXMaximumAge]))) #adds new elephant lists to the population function
    return population

def incrementAge(population):
    for e in population:
        e[IDXAge] +=1 #adds one year to the age of every elephant in the population
    return population

def calcSurvival(parameters, population):
    new_population = []
    for e in population:
        if(e[IDXAge] <= 1): #uses age to determine the probability of survival
            if(random.random() < parameters[IDXProbCalfSurv]):
                new_population.append(e) #if the random value is less than the 
        if(e[IDXAge] <= parameters[IDXMaximumAge]) and (e[IDXAge] > 1):
            if(random.random() < parameters[IDXProbAdultSurv]):
                new_population.append(e)
        if(e[IDXAge] > parameters[IDXMaximumAge]):
            if(random.random() < parameters[IDXProbSeniorSurv]):
                new_population.append(e)
    return new_population

def dartElephants(parameters, population):
    probofDarting = parameters[IDXPercentDarted] #sets the parameters to local variables
    juvenileAge = parameters[IDXJuvenileAge] 
    maximumAge = parameters[IDXMaximumAge]
    for e in population:
        if(e[IDXGender] == "f"): #tests to see if the elephant is female
            if(e[IDXAge] > juvenileAge) and (e[IDXAge] < maximumAge): #tests to see if they are the appropriate age
                if(random.random() < probofDarting): #uses probability to determine if the elephant is darted
                    e[IDXMonthsPregnant] = 0 #if they are darted, they will no longer be pregnant
                    e[IDXMonthsContraceptiveRemaining] = 22
    return population      

def cullElephants(parameters, population):
    carryingCapacity = parameters[IDXCarryingCapacity] #sets the carrying capacity of the population to the parameter value
    culledNumber = len(population) - carryingCapacity #calculates the number of elephants that need to be culled
    if(culledNumber > 0): #if there are elephants that need to be culled
        random.shuffle(population)
        newPopulation = population[0:carryingCapacity] #the population will be shuffled and cut down to a population that is the size of the carrying capacity.
        return (newPopulation, culledNumber) #returns a tuple
    else:
        return(population, culledNumber) #returns the normal population with the number that needed to be culled

def controlPopulation(parameters, population):
    if(parameters[IDXPercentDarted] == 0): #if the percentage of elephants to be darted is 0
        (newPopulation, culledNumber) = cullElephants(parameters, population) #call the cullElephants function
    else:
        newPopulation = dartElephants(parameters, population) #otherwise, call the dartElephant function
        culledNumber = 0
    
    return (newPopulation, culledNumber)

def simulateMonth(parameters, population):
    calvingInterval = parameters[IDXCalvingInterval] #creates local variables for three parameters in the parameters list 
    juvenileAge = parameters[IDXJuvenileAge]
    maximumAge = parameters[IDXMaximumAge]

    for e in population: #for elephants in the population
        gender = e[IDXGender] #assign local variables for the attributes of elephants.
        age = e[IDXAge]
        monthsPregnant = e[IDXMonthsPregnant]
        monthsContraceptive = e[IDXMonthsContraceptiveRemaining]

        if(gender == "f") and (age > juvenileAge) and (age <= maximumAge): #determines if the elephant is an adult female
            if(monthsContraceptive > 0): #if the number of  months of contraceptive left is more than 0
                e[IDXMonthsContraceptiveRemaining] -= 1 #subtract one month
            elif(monthsPregnant > 0): #if the elephant is pregnant
                if(monthsPregnant >= 22): #if they have reached their full-term or more
                    population.append([random.choice(["m", "f"]), 1, 0, 0]) #add one calf to the population that is one year old
                    e[IDXMonthsPregnant] = 0 #set the elephants pregnancy length to 0
                else:
                    e[IDXMonthsPregnant] += 1 #otherwise, add one month to their pregnancy
            else: #if the elephant is not pregnant and is not on contraceptive
                pregProbability = (1) / (calvingInterval * 12 -22)
                if(random.random() < pregProbability): #if they become pregnant
                    e[IDXMonthsPregnant] = 1 #add one to the number of months that they have been pregnant
    return population

def simulateYear(parameters, population):
    population = calcSurvival(parameters, population) #calls the calcSurvival function to determine the number of elephants that survive
    population = incrementAge(population) #increments the age of every elephant in the population
    for i in range(12):
        population = simulateMonth(parameters, population) #reassigns the value of population to the population that was simulated in the month.
    return population

def calcResults(parameters, population, culledNumber):
    juvenileAge = parameters[IDXJuvenileAge] #assigns local variables to the juvenile and maximum age parameters
    maximumAge = parameters[IDXMaximumAge]
    calfNum = 0 #initializes variables that will will count specific members of the population
    juvenileNum = 0
    adultFemaleNum = 0
    adultMaleNum = 0
    seniorNum = 0
    total = 0

    for e in population:
        total += 1
        if(e[IDXAge] == 1): #depending on the age of the elephant, a different variable is incremented
            calfNum += 1
        elif(e[IDXAge]> 1) and (e[IDXAge] < juvenileAge):
            juvenileNum += 1
        elif(e[IDXAge] > juvenileAge) and (e[IDXAge] <= maximumAge):
            if (e[IDXGender] == "f"): #checks the gender of the adults and increments the count based on gender
                adultFemaleNum += 1
            elif(e[IDXGender] == "m"):
                adultMaleNum += 1
        elif(e[IDXAge] > maximumAge):
            seniorNum += 1
    return [total, calfNum, juvenileNum, adultMaleNum, adultFemaleNum, seniorNum, culledNumber] #returns a list containing all of the counts.

def runSimulation(parameters):
    popsize = parameters[IDXCarryingCapacity]

    # init the population
    population = initPopulation( parameters )
    [population,numCulled] = controlPopulation( parameters, 
    population )

    # run the simulation for N years, storing the results
    results = []
    for i in range(parameters[IDXNumYears]):
        population = simulateYear( parameters, population )
        [population,numCulled] = controlPopulation( parameters, 
         population )
        results.append( calcResults( parameters, population, 
        numCulled ) )
        print("The total population size is: " + str(results[i][0]))
        if results[i][0] > 2 * popsize or results[i][0] == 0 : 
            # cancel early, out of control
            print( 'Terminating early' )
            break
    return results

def main(argv):
    if(len(argv) < 2) or (len(argv) > 2): #if the number of parameters isn't correct, then a usage statement will be printed
        print("This program takes two parameters in the command line, one that specifies the name of the Python program and the second gives the probability of darting.")
    else:
        calvingInterval = 3.1 #initializes all of the parameter values
        probDart = float(argv[1]) #probability of darting occuring from the command line
        juvenileAge = 12
        maxAge = 60
        probCalfSurv = 0.85
        probAdultSurv = 0.996
        probSeniorSurv = 0.2
        carryingCapacity = 7000
        numYears = 200

        parameters = [calvingInterval, probDart, juvenileAge, maxAge, probCalfSurv, probAdultSurv, probSeniorSurv, carryingCapacity, numYears] 
        results = runSimulation(parameters)
        print(results[-1])

        averageTotal = 0 #initalizes variables to hold the total and average of each age of elephant
        averageCalfNum = 0
        averageJuvenileNum = 0
        averageadultMaleNum = 0
        averageadultFemaleNum = 0
        averageseniorNum = 0
        numPoints = len(results)

        for result in results: #adds all of the values in the result list to the corresponding totals
            averageTotal += result[0]
            averageCalfNum += result[1]
            averageJuvenileNum += result[2]
            averageadultMaleNum += result[3]
            averageadultFemaleNum += result[4]
            averageseniorNum += result[5]
    
        averageTotal = averageTotal / numPoints #calculates each average by dividing the sum of the totals by the number of totals that were in the list 
        averageCalfNum = averageCalfNum / numPoints
        averageJuvenileNum = averageJuvenileNum / numPoints
        averageadultMaleNum = averageadultMaleNum / numPoints
        averageadultFemaleNum = averageadultFemaleNum / numPoints
        averageseniorNum = averageseniorNum / numPoints

        print("The average total population is: %i"  % (averageTotal)) #prints all of the averages that were calculated as integers
        print("The average number of calves is: %i" % (averageCalfNum))
        print("The average number of juveniles is: %i" % (averageJuvenileNum)) 
        print("The average number of male adults is: %i" % (averageadultMaleNum))
        print("The average number of female adults is: %i" % (averageadultFemaleNum))
        print("The average number of seniors is: %i" % (averageseniorNum))

        #Extension
        numofFemaleAdults = [] #creates empty lists
        numofMaleAdults = []
        numofJuveniles = []

        for result in results:
            numofJuveniles.append(result[2]) #appends the value at the specified index position in the smaller list to the new list
            numofMaleAdults.append(result[3])
            numofFemaleAdults.append(result[4])
        
        medianJuv = stats.median(numofJuveniles) #uses the median function in the stats module to find the median of the lists
        medianMale = stats.median(numofMaleAdults)
        medianFemale = stats.median(numofFemaleAdults)

        print("The median number of juveniles is: %i" % (medianJuv)) #prints all of the medians 
        print("The median number of adult males is: %i" % (medianMale))
        print("The median number of adult females is: %i" % (medianFemale))

        stJuvenile = stats.standardDeviation(numofJuveniles) #finds the standard deviation of the list using the standard deviation function in the stats module
        stMale = stats.standardDeviation(numofMaleAdults)
        stFemale = stats.standardDeviation(numofFemaleAdults)      

        print("The standard deviation of the juvenile population is: %i" % (stJuvenile)) #prints all of the standard deviations for the three types of elephants
        print("The standard deviation of the adult male population is: %i" % (stMale))
        print("The standard deviation of the adult female population is: %i" % (stFemale))

        
        

        


def test():
    '''Tests all of the functions that are created in the module'''

    #Initialize variables for parameters of the functions
    calvingInterval = 3.1
    percentDarted = 0.0
    juvenileAge = 12
    maxAge = 60
    probCalfSurv = 0.85
    probAdultSurv = 0.996
    probSeniorSurv = 0.2
    carryingCapacity = 20
    numYears = 200


    '''Tests the parameters list and the indexes of the parameters'''
    parameters = [calvingInterval, percentDarted, juvenileAge, maxAge, probCalfSurv, probAdultSurv, probSeniorSurv, carryingCapacity, numYears] #creates a list with the parameter variables
    print(parameters) #prints the list
    print(parameters[IDXCalvingInterval]) #checks to make sure that each parameter is correctly assigned
    print(parameters[IDXPercentDarted])
    print(parameters[IDXJuvenileAge])
    print(parameters[IDXMaximumAge])
    print(parameters[IDXProbCalfSurv])
    print(parameters[IDXProbAdultSurv])
    print(parameters[IDXProbSeniorSurv])
    print(parameters[IDXCarryingCapacity])
    print(parameters[IDXNumYears])

    '''Tests the newElephant function'''
    pop = []
    for i in range(15): #will create 15 elephants (lists)
        pop.append(newElephant(parameters, random.randint(1, parameters[IDXMaximumAge])))
    
    for e in pop:
        print (e) #prints the lists 
    
    '''Tests the initPopulation function'''
    print("Population of Elephants")
    population = initPopulation(parameters)
    print(population)

    '''Tests for the incrementAge function'''
    print("Incremented Age")
    print(incrementAge(population))

    main(sys.argv) #runs the main function 






if __name__ == "__main__":
    test()