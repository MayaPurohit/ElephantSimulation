'''Maya Purohit
Project03
CS 152A
stats.py
09/28/22
The purpose of this code is to create a module that can be imported into another program to calculate statistics
To open this file in the Python Terminal, direct the terminal to the Project 03 folder using the cd command
Enter py and the file name from the Project03 folder'''

import math #imports the math package
def sum(numbers): #creates a new function that can calculate the sum of all of the numbers in a list
    total = 0.0 #initialized a total variable

    for num in numbers: #for every value in the list, the value will be added to the total variable
        total += num
        
    return total #returns the value


def mean(data):
    '''Calculates the average of the numbers in a list'''
    increment = len(data) #records the number of values in the list 
    average = sum(data)/increment #uses the sum function from above to find the sum
    return average #calculates the average and returns it

def min(data):
    '''Finds the minimum value in the list''' 
    data_min = data[0] #sets the initial value to the first value in the data set
    for num in range(len(data)):
        if(data[num - 1] < data_min): #finds the minimum value in the data set by comparing every value
            data_min = data[num-1] #min value is reassigned
    return data_min

def max(data):
    '''Finds the minimum value in the list'''
    data_max = data[0] #sets the inital number to the first value in the data set
    for num in range(len(data)):
        if(data[num - 1] > data_max): #finds the maximum value in the data set by comparing every value
            data_max = data[num - 1] #max value is reassigned
    return data_max
    

def variance(data):
    '''Finds the variance of the list of values'''
    increment = 0
    average = mean(data) #uses the average function to find the mean of all of the values in data
    increment = len(data) #takes on the value of the number items there are in the list
    numerator = 0
    for value in range (len(data)):
        numerator += ((data[value]-average)**2) #calculates the numerator for the variance formula

    denominator = increment- 1
    variance = numerator/denominator 
    return variance #returns the value of variance to the function

#Extension with more statistics
def standardDeviation(data):
    '''Finds the standard deviation by taking the square root of the variance'''
    standard = math.sqrt(variance(data)) #reused the variance function to find the standard deviation
    return standard #returns the value to the function

def median(data):
    '''Finds the median of the data set'''
    number = 0
    data.sort()
    for i in range(len(data)):
        number += 1 #counts the number of values that are in the list
    if(number % 2 == 0): #if the number is even, the average of the middle two terms should be taken
        firstPosition = int(number/2)
        secondPosition = int(firstPosition + 1)
        median = (data[firstPosition-1] + data[secondPosition-1]) /2 #subtract one from the index position to account for the zero index
            
    if(number % 2 != 0): #if the number is odd, the number at the middle index position should be the median
        value = int(((number-1)/2)+1)
        median = data[value -1]
    return median #returns the median to the function



def test():
    '''Tests the functions from above by calling them'''
    test_list = [1, 2, 3, 4] #creates a list
    sumResult = sum(test_list) #sets the value of the sum function with the list as the parameter to the variable result
    print ("Sum: "+ str(sumResult)) 
    print("Mean: %.2f" % (mean(test_list))) #test for each of the functions to see if they work properly by printing the value
    print("Min: "+ str(min(test_list)))
    print("Max: "+ str(max(test_list)))
    print("Variance: %.2f" % (variance(test_list))) #formats the value to 2 decimal places
    print("Standard Deviation: %.2f" % (standardDeviation(test_list)))
    print("Median: %.2f" % (median(test_list)))


if __name__ == "__main__": #will not execute test function when the file is imported
    test()