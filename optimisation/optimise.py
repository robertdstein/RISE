import ROOT, time, os
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
from subprocess import call

#Code hub to run the different modules involved in optimisation

start = time.time()
print time.asctime(time.localtime()), "Starting Code"

parser = argparse.ArgumentParser(description='Beform Datacuts and look for B Mass peaks')
parser.add_argument("-f", "--fit", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-s", "--simulate", action="store_true")
parser.add_argument("-br", "--branchingratio", action="store_true")
parser.add_argument("-l", "--mlower", default=4500)
parser.add_argument("-u", "--mupper", default=6250)
parser.add_argument("-lc", "--lowercut", default=5100)
parser.add_argument("-uc", "--uppercut", default=5400)
parser.add_argument("-c", "--count", default=20)
parser.add_argument("-bkg", "--background", default=200)
parser.add_argument("-b", "--bdt", default=0.6)

cfg = parser.parse_args()

#Produce a dataset from the TTree, remove the BMass range to create a blinded dataset 

if cfg.fit == True:
    import fit as f
    if cfg.graph == True:
        cfg.background = f.run(cfg.mlower, cfg.mupper, cfg.lowercut, cfg.uppercut, cfg.bdt, graph = True)
    else:
        cfg.background = f.run(cfg.mlower, cfg.mupper, cfg.lowercut, cfg.uppercut, cfg.bdt)

#Using a Monte Carlo model and background, simulate K mu e data to place in the cut region 

if cfg.simulate == True:
    import simulate as s
    if cfg.graph == True:
        sig, eff, significance, peak = s.run(cfg.mlower, cfg.mupper, cfg.lowercut, cfg.uppercut, cfg.bdt, cfg.background, cfg.count, graph = True)
    else:
        sig, eff, significance, peak = s.run(cfg.mlower, cfg.mupper, cfg.lowercut, cfg.uppercut, cfg.bdt, cfg.background, cfg.count)
    if significance == True:
        
        #If peak is greater than 5 sigma, calculate the branching ratio
        
        if cfg.branchingratio == True:
            import branchingratio as br
            br.run(sig, eff)
    else:
        print time.asctime(time.localtime()), "Uncertainty is too high to place an upper limit on Branching Ratio"
    
    
end = time.time()
print time.asctime(time.localtime()), "Code Ended"

pl.show()