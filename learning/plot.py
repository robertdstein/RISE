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
    
def run(name, quick = False):
    print time.asctime(time.localtime()), "Fitting and Plotting Points"
    if quick == True:
        gmm = joblib.load('pickle/' + name + 'gmmquick.pkl')
        dpgmm = joblib.load('pickle/' + name + 'dpgmmquick.pkl')
        data = joblib.load("pickle/dataq.pkl")
    else:
        gmm = joblib.load('pickle/' + name + 'gmm.pkl')
        dpgmm = joblib.load('pickle/' + name + 'dpgmm.pkl')
        data = joblib.load('pickle/data.pkl')
    
    color_iter = itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y', 'k'])
    
    for i, (clf, title) in enumerate([(gmm, 'GMM'),
                                  (dpgmm, 'Dirichlet Process GMM')]):
        splot = plt.subplot(2, 1, 1 + i)
        Y_ = clf.predict(data)
        for i, (mean, covar, color) in enumerate(zip(
                clf.means_, clf._get_covars(), color_iter)):
            v, w = linalg.eigh(covar)
            u = w[0] / linalg.norm(w[0])
            plt.scatter(data[Y_ == i, 0], data[Y_ == i, 1], .8, color=color)
        
        plt.xlim(4500, 6000)
        plt.xticks(())
        plt.yticks(())
        plt.title(title)
        
    print time.asctime(time.localtime()), "Data has been fitted!"
    
    plt.show()