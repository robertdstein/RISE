import ROOT, time
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
import csv
from sklearn.externals import joblib

def run(name, quick=False):   
    print time.asctime(time.localtime()), "Making Predictions"
    
    #Load all relevant datasets from Pickle files
    
    if quick == True:
        clf = joblib.load("pickle/" + name +"quick.pkl")
        data = joblib.load("pickle/dataq.pkl")
        output = joblib.load("pickle/outputq.pkl")
        datatest = joblib.load("pickle/datatestq.pkl")
        outputtest = joblib.load("pickle/outputtestq.pkl")
        signal = joblib.load('pickle/signalq.pkl')
        signaltest = joblib.load('pickle/signaltestq.pkl')
        signaloutput = joblib.load('pickle/signaloutputq.pkl')
        signaloutputtest = joblib.load('pickle/signaloutputtestq.pkl')
        background = joblib.load('pickle/backgroundq.pkl')
        backgroundtest = joblib.load('pickle/backgroundtestq.pkl')
        backgroundoutput= joblib.load('pickle/backgroundoutputq.pkl')
        backgroundoutputtest = joblib.load('pickle/backgroundoutputtestq.pkl')
    else:
        clf = joblib.load("pickle/" + name + ".pkl")
        data = joblib.load("pickle/dataq.pkl")
        output = joblib.load("pickle/outputq.pkl")
        datatest = joblib.load("pickle/datatest.pkl")
        outputtest = joblib.load("pickle/outputtest.pkl")
        signal = joblib.load('pickle/signal.pkl')
        signaltest = joblib.load('pickle/signaltest.pkl')
        signaloutput = joblib.load('pickle/signaloutput.pkl')
        signaloutputtest = joblib.load('pickle/signaloutputtest.pkl')
        background = joblib.load('pickle/background.pkl')
        backgroundtest = joblib.load('pickle/backgroundtest.pkl')
        backgroundoutput= joblib.load('pickle/backgroundoutput.pkl')
        backgroundoutputtest = joblib.load('pickle/backgroundoutputtest.pkl')
        
    #Produce scores for each dataset, giving the fraction of correct predictions by the BDT
    
    print "Score on whole training sample is", clf.score(data, output)
    print "Score on whole test sample is", clf.score(datatest, outputtest)
    print "Score on training signal is ", clf.score(signal, signaloutput)
    print "Score on test signal is ", clf.score(signaltest, signaloutputtest)
    print "Score on training background is ", clf.score(background, backgroundoutput)
    print "Score on test background is ", clf.score(backgroundtest, backgroundoutputtest)
    
