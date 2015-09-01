import ROOT, time, os, csv
import numpy as np
import pylab as pl
import argparse
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

def output(bdt=0.967, probk=-3.5, probmu=0.9, probe=4.525, countoutput=False, text=False, dynamic=False):
    
    #Fit to find expected background count and exponential distribution parameter
    expcount, aval = f.run(lower, upper, lowercut, uppercut, bdt, probk, probmu, probe, text=text)
    count = 10000
    significance = False
    #iteratively add counts to the signal peak until it has a 5 sigma significance
    if expcount != None:
        while significance != True:
            sig, eff, significance, peak, sigma = s.run(lower, upper, lowercut, uppercut, bdt, expcount, aval, count, probk, probmu, probe, text=text)
            if (dynamic == True) & (peak < 3.0):
                if sigma < (expcount * 0.2):
                    count += (int(sigma) +1)
                else:
                    count +=20
            else:
                count += int(sigma*0.01) +1
        ratio, error = br.run(sig, eff)
        #return ratio and error for the purpose of a csv output and graph
        if countoutput == True:
            return ratio, error
        #return just the ratio, for the purpose of minimisation
        else:
            return ratio
    #If the fit has not converged, or expected count is 0, return error
    else:
        return float('nan')