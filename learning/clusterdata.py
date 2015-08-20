import ROOT, time
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
import csv
from sklearn.externals import joblib

def run(source, quick=False):
    print time.asctime(time.localtime()), "Copying datasets"

    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/DATA_Bplus_Kplusmumu_qsqcut_sweight.root")
    t = f.Get("DecayTree")
    
    v = []
    lim = []

    with open(source, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            v.append(row[0])
            lim.append(row[1])
    
    joblib.dump(v, 'pickle/variables.pkl')
    joblib.dump(lim, 'pickle/limits.pkl')

    if quick == True:
        tcount = int(t.GetEntriesFast()*0.015)
    else:
        tcount = t.GetEntriesFast()

    info = []

    frac = 0.5
    ttrain = int(tcount*frac)
    print time.asctime(time.localtime()), "Data contains", tcount, "entries"
    
    for i in range (0, ttrain):
        t.GetEntry(i)
        k = []
        for i in range(len(v)):
            k.append(eval("t."+v[i]))
        info.append(k)
    
    print time.asctime(time.localtime()), "50% copied"
    
    for i in range (ttrain + 1, tcount):
        t.GetEntry(i)
        k = []
        for i in range(len(v)):
            k.append(eval("t."+v[i]))
        info.append(k)

    data = np.array(info)

    if quick == True:
        joblib.dump(data, 'pickle/dataq.pkl')
        
    else:
        joblib.dump(data, 'pickle/data.pkl')
    
    print time.asctime(time.localtime()), "Datasets produced!"