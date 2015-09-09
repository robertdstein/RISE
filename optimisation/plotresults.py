import matplotlib.pyplot as plt
import numpy as np
import csv

x=[]
y=[]
error=[]

def scattergraph(source):
    
    #Reads results from a given CSV file
    
    with open("sources/" + source + ".csv", 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i=0
        for row in reader:
            if i == 0:
                variable = row[0]
                i+=1
            else:
                x.append(float(row[0]))
                y.append(float(row[1]))   
                error.append(float(row[2]))   
    
    #Creates a scatter graph displaying the upper limit on Branching Ratio over a range of variable values
    
    plt.figure()
    plt.errorbar(x, y, yerr=error, linestyle='_', marker = 'o', color = 'r')
    plt.xlabel(str(variable) + " cut")
    plt.ylabel("Expected upper limit on Branching Ratio")
    plt.ylim(0)
    plt.savefig("output/" + str(source)+".pdf")
    plt.show()