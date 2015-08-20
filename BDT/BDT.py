import ROOT, time, os
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
from subprocess import call

start = time.time()
print time.asctime(time.localtime()), "Starting Code"

#Parse Arguments to trigger each BDT module that is needed, as well as additional arguments

parser = argparse.ArgumentParser(description='Train BDT and analyse performance')
parser.add_argument("-d", "--dataset", action="store_true")
parser.add_argument("-t", "--train", action="store_true")
parser.add_argument("-r", "--roc", action="store_true")
parser.add_argument("-f", "--features", action="store_true")
parser.add_argument("-q", "--quick", action="store_true")
parser.add_argument("-c", "--checksignal", action="store_true")
parser.add_argument("-p", "--plot", action="store_true")
parser.add_argument("-fd", "--fulldata", action="store_true")
parser.add_argument("-w", "--write", action="store_true")
parser.add_argument("-cd", "--cutdata", action="store_true")
parser.add_argument("-n", "--name", default="BDT")
parser.add_argument("-m", "--maxdepth", default=6)
parser.add_argument("-s", "--source", default="BDTvar.csv")
parser.add_argument("-b", "--bins", default=30)
parser.add_argument("-e", "--estimators", default=50)

cfg = parser.parse_args()

if cfg.source == "BDTvarJpsi.csv":
    cfg.name += "JPsiK"
elif cfg.source !="BDTvar.csv":
    raise NameError("Invalid Source Selection!")
    
#Generate dataset in a numpy array for later use by SciKit Learn, which is then saved as a pickle file

if cfg.dataset == True:
    import datasets as ds
    if cfg.quick == True:
        ds.run(cfg.source, quick = True)
    else:
        ds.run(cfg.source)

#Loads most recent dataset and trains a BDT on half of the total data

if cfg.train == True:
    import train as tr
    if cfg.quick == True:
        tr.run(cfg.name, int(cfg.maxdepth), int(cfg.estimators), quick = True)
    else:
        tr.run(cfg.name, int(cfg.maxdepth), int(cfg.estimators))

#Generates ROC curves for assesment of efficiency

if cfg.roc == True:
    import roccurves as rc
    if cfg.quick == True:
        rc.run(cfg.name + str(cfg.maxdepth), quick = True)
    else:
        rc.run(cfg.name + str(cfg.maxdepth))
        
#Lists variables used by the BDT, ranked in order of importance
    
if cfg.features == True:
    import features as f
    if cfg.quick == True:
        f.run(cfg.name + str(cfg.maxdepth), quick = True)
    else:
        f.run(cfg.name + str(cfg.maxdepth))
        
#Produces a score for BDT accuracy on subsets of the data, to check for overtraining
        
if cfg.checksignal == True:
    import checksignal as c
    if cfg.quick == True:
        c.run(cfg.name + str(cfg.maxdepth), quick = True)
    else:
        c.run(cfg.name + str(cfg.maxdepth))
        
#Generates a plot to show BDT reponse histograms
        
if cfg.plot == True:
    import plot as p
    if cfg.quick == True:
        p.run(cfg.name + str(cfg.maxdepth), int(cfg.bins), quick = True)
    else:
        p.run(cfg.name + str(cfg.maxdepth), int(cfg.bins))

#Produces an array containing all events from either MC or the real data

if cfg.fulldata == True:
    import fulldata as fd
    if cfg.quick == True:
        raise Exception("Requires full dataset")
    else:
        fd.run()

#Creates a new tree with a BDT branch, giving the probability that each event is a signal event

if cfg.write == True:
    import write as w
    if cfg.quick == True:
        raise Exception("Requires full dataset")
    else:
        w.run(cfg.name + str(cfg.maxdepth),cfg.source)
     
#Produces a new tree by selecting on the basis that BDT>x where x is a given probability

if cfg.cutdata == True:
    import cutdata as cd
    if cfg.quick == True:
        raise Exception("Requires full dataset")
    else:
        cd.run()

end = time.time()
print time.asctime(time.localtime()), "Code Ended"

pl.show()