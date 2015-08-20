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
    
    #Selecting the correct dataset
    
    if source == "BDTvar.csv":
        f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/DATA_Bplus_Kplusmue_qsqcutminPtBranch.root")
        t = f.Get("DecayTree")
    
        g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/MC_Bplus_Kplusmue_qsqcutminPtBranch.root")
        u = g.Get("DecayTree")
        
    elif source == "BDTvarJpsi.csv":
        f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/DATA_Bplus_Kplusmumu_qsqcut.root")
        t = f.Get("DecayTree")
    
        g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/MC_Bplus_KplusJpsimumu_qsqcut.root")
        u = g.Get("DecayTree")       

    info = []
    infotest = []

    emu = []
    emutest =[]
    
    sig= []
    sigtest = []

    bkg = []
    bkgtest = []
    
    #Reading variables from a csv file, and producing an array        
                
    v = []
    
    with open(source, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            v.append(row[0])

    joblib.dump(v, 'pickle/variables.pkl')

    if quick == True:
        tcount = int(t.GetEntriesFast()*0.1)
    else:
        tcount = t.GetEntriesFast()

    frac = 0.5
    ttrain = int(tcount*frac)
    print time.asctime(time.localtime()), "Real Data contains", tcount, "entries. Training on ", ttrain, "Entries"
    ucount = u.GetEntriesFast()
    utrain = int(ucount*frac)
    print time.asctime(time.localtime()), "Monte Carlo contains", ucount, "entries. Training on ", utrain, "Entries"
    
    #Producing arrays of test and train data
    
    for i in range (0, ttrain):
        t.GetEntry(i)
        k = []
        for i in range(len(v)):
            k.append(eval("t."+v[i]))
        info.append(k)
        emu.append(0)
        bkg.append(k)
    
    print time.asctime(time.localtime()), "25% copied"
    
    for i in range (ttrain + 1, tcount):
        t.GetEntry(i)
        k = []
        for i in range(len(v)):
            k.append(eval("t."+v[i]))
        infotest.append(k)
        emutest.append(0)
        bkgtest.append(k)

    print time.asctime(time.localtime()), "50% copied"

    for i in range (0, utrain):
        u.GetEntry(i)
        k = []
        for i in range(len(v)):
            k.append(eval("u."+v[i]))
        info.append(k)
        emu.append(1)
        sig.append(k)
        
    print time.asctime(time.localtime()), "75% copied"
    
    for i in range (utrain + 1, ucount):
        u.GetEntry(i)
        k = []
        for i in range(len(v)):
            k.append(eval("u."+v[i]))
        infotest.append(k)
        emutest.append(1)
        sigtest.append(k)

    data = np.array(info)
    datatest=np.array(infotest)
    
    output = np.array(emu)
    outputtest= np.array(emutest)
    
    background = np.array(bkg)
    backgroundtest = np.array(bkgtest)
    
    backgroundoutput = np.zeros(len(background), dtype=np.int)
    backgroundoutputtest = np.zeros(len(backgroundtest), dtype=np.int)
    
    signal = np.array(sig)
    signaltest = np.array(sigtest)
    
    signaloutput = np.ones(len(signal), dtype=np.int)
    signaloutputtest = np.ones(len(signaltest), dtype=np.int)
    
    #Saving the datasets in the form of Pickle files 
    
    if quick == True:
        joblib.dump(data, 'pickle/dataq.pkl')
        joblib.dump(datatest, 'pickle/datatestq.pkl')
        joblib.dump(output, 'pickle/outputq.pkl')
        joblib.dump(outputtest, 'pickle/outputtestq.pkl')
        joblib.dump(signal, 'pickle/signalq.pkl')
        joblib.dump(signaltest, 'pickle/signaltestq.pkl')
        joblib.dump(signaloutput, 'pickle/signaloutputq.pkl')
        joblib.dump(signaloutputtest, 'pickle/signaloutputtestq.pkl')
        joblib.dump(background, 'pickle/backgroundq.pkl')
        joblib.dump(backgroundtest, 'pickle/backgroundtestq.pkl')
        joblib.dump(backgroundoutput, 'pickle/backgroundoutputq.pkl')
        joblib.dump(backgroundoutputtest, 'pickle/backgroundoutputtestq.pkl')
        
    else:
        joblib.dump(data, 'pickle/data.pkl')
        joblib.dump(datatest, 'pickle/datatest.pkl')
        joblib.dump(output, 'pickle/output.pkl')
        joblib.dump(outputtest, 'pickle/outputtest.pkl')
        joblib.dump(signal, 'pickle/signal.pkl')
        joblib.dump(signaltest, 'pickle/signaltest.pkl')
        joblib.dump(signaloutput, 'pickle/signaloutput.pkl')
        joblib.dump(signaloutputtest, 'pickle/signaloutputtest.pkl')
        joblib.dump(background, 'pickle/background.pkl')
        joblib.dump(backgroundtest, 'pickle/backgroundtest.pkl')
        joblib.dump(backgroundoutput, 'pickle/backgroundoutput.pkl')
        joblib.dump(backgroundoutputtest, 'pickle/backgroundoutputtest.pkl')    
    
    print time.asctime(time.localtime()), "Datasets produced!"