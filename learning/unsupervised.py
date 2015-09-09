import ROOT, time, os
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
from subprocess import call

#Hub page for the unsupervised learning scripts

start = time.time()
print time.asctime(time.localtime()), "Starting Code"

parser = argparse.ArgumentParser(description='Unsupervised Learning for grouping of data')
parser.add_argument("-d", "--dataset", action="store_true")
parser.add_argument("-l", "--learn", action="store_true")
parser.add_argument("-q", "--quick", action="store_true")
parser.add_argument("-c", "--classify", action="store_true")
parser.add_argument("-p", "--plot", action="store_true")
parser.add_argument("-o", "--onedhistogram", action="store_true")
parser.add_argument("-n", "--name", default="ul")
parser.add_argument("-f", "--fit", default="dpgmm")
parser.add_argument("-s", "--source", default="clvar.csv")
parser.add_argument("-a", "--alpha", default=200)
parser.add_argument("-g", "--groups", default=30)

cfg = parser.parse_args()

if cfg.source !="clvar.csv":
    raise NameError("Invalid Source Selection!")

#Creates datsets with variables saved in the CSV file cfg.source

if cfg.dataset == True:
    import clusterdata as ds
    if cfg.quick == True:
        ds.run(cfg.source, quick = True)
    else:
        ds.run(cfg.source)

#Applies unsupervised learning to the datasets

if cfg.learn == True:
    import learn as l
    if cfg.quick == True:
        l.run(str(cfg.name + "quick"), cfg.alpha, cfg.groups, quick = True)
    else:
        l.run(cfg.name, cfg.alpha, cfg.groups)

#Does something, probably.    
                        
if cfg.plot == True:
    import plot as p
    if cfg.quick == True:
        p.run(cfg.name + "quick", quick = True)
    else:
        p.run(cfg.name)
        
#Classifies the data into a varying number of categories

if cfg.classify == True:
    import classify as c
    if cfg.quick == True:
        c.run(cfg.name + "quick", cfg.fit, quick = True)
    else:
        c.run(cfg.name, cfg.fit)

#Creates Histograms for each category identied by learning algorithm

if cfg.onedhistogram == True:
    import histogram as h
    if cfg.quick == True:
        h.run(cfg.name + "quick", int(cfg.groups), str(cfg.fit), quick = True)
    else:
        h.run(cfg.name, int(cfg.groups), str(cfg.fit))

end = time.time()
print time.asctime(time.localtime()), "Code Ended"

pl.show()