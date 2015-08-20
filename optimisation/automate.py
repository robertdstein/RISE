import ROOT, time, os, csv
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
from subprocess import call
import branchingratio as br
import fit as f
import simulate as s

print time.asctime(time.localtime()), "Starting Code"

#Fix blinded region and B Mass fit range

lower=4500
upper=6250
lowercut=5100
uppercut=5400

with open('results.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['bdt' ,'count', 'peak', 'sig', 'eff', 'significance', 'ratio'])
    
    bdtvals = np.arange(0.95, 0.99, 0.01)
    countvals = np.arange(10, 400, 10)
    
    #Iterate over a range of BDT probabilities and signal counts, exporting results to a csv file
    
    for i in bdtvals:
        bdt = i
        print time.asctime(time.localtime()), "BDT cut is", i
        expcount = f.run(lower, upper, lowercut, uppercut, bdt)
        for i in countvals:
            count = i
            sig, eff, significance, peak = s.run(lower, upper, lowercut, uppercut, bdt, expcount, count)
            if significance == True:
                ratio = br.run(sig, eff)
            else:
                ratio = None
            data = [bdt, count, peak, sig, eff, significance, ratio]
            writer.writerow(data)
end = time.time()
print time.asctime(time.localtime()), "Code Ended"

pl.show()