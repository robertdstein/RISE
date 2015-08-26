import matplotlib.pyplot as plt
import numpy as np
import csv

x=[]
y=[]
error=[]

def scattergraph(source):
    with open(source + ".csv", 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i=0
        for row in reader:
            if i == 0:
                i+=1
            else:
                x.append(float(row[0]))
                y.append(float(row[1]))   
                error.append(float(row[2]))   
    plt.figure()
    plt.errorbar(x, y, yerr=error, linestyle='_', marker = 'o', color = 'r')
    plt.xlabel("BDT cut")
    plt.ylabel("Expected upper limit on Branching Ratio")
    plt.ylim(0, (10**-8))
    plt.savefig(str(source)+".pdf")
    plt.show()
