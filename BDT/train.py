import ROOT, time
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
import csv
from sklearn.externals import joblib

def run(name, maxdepth = 10, estimators = 50, quick = False):
    print time.asctime(time.localtime()), "Training BDT" 
    
    #Load datasets for training
    
    if quick == True:
        data = joblib.load("pickle/dataq.pkl")
        output = joblib.load("pickle/outputq.pkl")

    else:
        data = joblib.load("pickle/data.pkl")
        output = joblib.load("pickle/output.pkl")
    
    #Train the BDT (Gradient Boosting Classifier)  and save
    
    clf = ensemble.GradientBoostingClassifier(max_depth = maxdepth, n_estimators = estimators)
    clf.fit(data, output)
    
    if quick == True:
        joblib.dump(clf, 'pickle/' + name + str(maxdepth) + 'quick.pkl')
    else:
        joblib.dump(clf, 'pickle/' + name + str(maxdepth) + '.pkl')
    
    print time.asctime(time.localtime()), "BDT Trained"