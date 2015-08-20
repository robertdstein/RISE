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
from iminuit import Minuit

#Fix blinded region and B Mass fit range

lower=4500
upper=6250
lowercut=5100
uppercut=5400

ROOT.gROOT.SetBatch(True)

def output(bdt, probk, probmu, probe):
    expcount = f.run(lower, upper, lowercut, uppercut, bdt, probk, probmu, probe)
    count = 20
    significance = False
    if expcount != None:
        while significance != True:
            sig, eff, significance, peak = s.run(lower, upper, lowercut, uppercut, bdt, expcount, count, probk, probmu, probe)
            count +=20
        ratio = br.run(sig, eff)
        return ratio
    #If the fit has not converged, or expected count is 0, return error
    else:
        return float('nan')

m = Minuit(output, bdt = 0.8, limit_bdt = (0.0, 0.999), error_bdt=0.1, probk = 0.2, limit_probk=(0,1.), error_probk=0.1, probe = 0.2, limit_probe=(0,1.), error_probe = 0.1, probmu = 0.2, limit_probmu=(0,1.), error_probmu=0.1)
m.migrad()

m.print_param()

end = time.time()
print time.asctime(time.localtime()), "Code Ended"

pl.show()