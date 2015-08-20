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

def run(name, nalpha, groups, quick = False):
    print time.asctime(time.localtime()), "Learning!" 
    
    v = joblib.load("pickle/variables.pkl")
    
    selection = []
    
    i = 0
    for i in range (0, len(v) -1):
        selection.append(i)
        i+=1
    
    if quick == True:
        data = joblib.load("pickle/dataq.pkl")

    else:
        data = joblib.load("pickle/data.pkl")

    gmm = mixture.GMM(n_components=7, covariance_type='diag')
    gmm.fit(data[:,selection])

    dpgmm = mixture.DPGMM(n_components=int(groups), alpha = float(nalpha), tol=1.0, n_iter=20, covariance_type='diag')
    dpgmm.fit(data[:,selection])

    if quick == True:
        joblib.dump(gmm, 'pickle/' + name + 'gmmquick.pkl')
        joblib.dump(dpgmm, 'pickle/' + name + 'dpgmmquick.pkl')
    else:
        joblib.dump(gmm, 'pickle/' + name + 'gmm.pkl')
        joblib.dump(dpgmm, 'pickle/' + name + 'dpgmm.pkl')
    
    print time.asctime(time.localtime()), "Unsupervised learning complete!"