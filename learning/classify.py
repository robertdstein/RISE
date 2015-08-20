import ROOT, time
from sklearn import ensemble
import numpy as np
import matplotlib.pyplot as plt
import argparse
import csv
from sklearn.externals import joblib
from sklearn.decomposition import IncrementalPCA, PCA

import itertools
from scipy import linalg
import matplotlib as mpl
from sklearn import mixture    
    
def run(name, fit, quick = False):
    print time.asctime(time.localtime()), "Classifying Data"
    if quick == True:
        gmm = joblib.load('pickle/' + name + 'gmmquick.pkl')
        dpgmm = joblib.load('pickle/' + name + 'dpgmmquick.pkl')
        data = joblib.load("pickle/dataq.pkl")
    else:
        gmm = joblib.load('pickle/' + name + 'gmm.pkl')
        dpgmm = joblib.load('pickle/' + name + 'dpgmm.pkl')
        data = joblib.load('pickle/data.pkl')
    
    v = joblib.load('pickle/variables.pkl')
    
    selection = []
    
    i = 0
    for i in range (0, len(v) -1):
        selection.append(i)
        i+=1

    if fit == "dpgmm":
        dpgmmpredictions = dpgmm.predict(data[:,selection])
    
    elif fit == "gmm":
        gmmpredictions = gmm.predict(data[:,selection])
        
    else:
        raise NameError
    
    print time.asctime(time.localtime()), "Saving Classified Data"
    
    d = []
    
    arg = ""
    for i in range(len(v)):
        arg += str("data[:," + str(i) + "][i], ")
        
    if fit == "dpgmm":
        arg += str("dpgmmpredictions[i]")
    
    elif fit == "gmm":
        arg += str("gmmpredictions[i]")

    for i in range(len(data)):
        d.append(eval(arg))
    
    if quick == True:
        joblib.dump(d, "pickle/data" + name+ "q.pkl")
        
    else:
        joblib.dump(d, "pickle/data" + name + ".pkl")
        
    print time.asctime(time.localtime()), "Classified Data Produced "