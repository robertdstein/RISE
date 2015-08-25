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

def output(bdt, probk=0.2, probmu=0.2, probe=0.2, countoutput=False):
    expcount = f.run(lower, upper, lowercut, uppercut, bdt, probk, probmu, probe)
    count = 20
    significance = False
    if expcount != None:
        while significance != True:
            sig, eff, significance, peak = s.run(lower, upper, lowercut, uppercut, bdt, expcount, count, probk, probmu, probe)
            count +=20
        ratio, error = br.run(sig, eff)
        if countoutput == True:
            return ratio, error
        else:
            return ratio
    #If the fit has not converged, or expected count is 0, return error
    else:
        return float('nan')