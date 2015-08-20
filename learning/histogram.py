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
    
def run(name, ncategories, fit, quick = False):
    print time.asctime(time.localtime()), "Producing histograms"
    
    lim = joblib.load("pickle/limits.pkl")
    v = joblib.load("pickle/variables.pkl")
    
    if quick == True:
        data = joblib.load("pickle/data" + name + "q.pkl")
    else:
        data = joblib.load("pickle/data" + name + ".pkl")
    
    if fit == "dpgmm":
        maxcategory = ncategories +1
        colour ='r' 
    
    elif fit == "gmm":
        maxcategory = 8
        colour = 'b'
    
    from matplotlib.backends.backend_pdf import PdfPages
    pp = PdfPages('output/' + name + '.pdf')
    
    for i in range(0, maxcategory):
        
        d={}
        for k in range(len(lim)):
            d["string{0}".format(k)]=[]
        
        for j in range(len(data)):
            l=data[j]
            if i == int(l[int(len(lim))]):
                m = 0    
                for key in d:
                    a = d.get(key)
                    a.append(l[m])
                    d[key] = a
                    m+=1
        
        print "For Category ", i, " there are ", len(d["string0"]), "events"
        plt.ioff()
        box = dict(facecolor='yellow', pad=5, alpha=0.2)
        fs = (8,18)
        if len(d["string0"]) > 10:       
            k = 0
            j = 0
            plt.figure(figsize = fs)
            for key in d:    
                a = d.get(key)      
                low = lim[k]
                if j == 1:
                    plt.title("Category " + str(i) + " with " +str(len(d["string0"])) + " Events")
                if j == 5:
                    pp.savefig(orientation='portrait')
                    plt.figure(figsize = fs)
                    j = 0
                j+=1
                high = max(np.max(d) for d in a)
                low_high = (low,high)            
                ax = plt.subplot(5, 1, j)
                ax.set_xlabel(v[k], bbox = box)
                plt.hist(a,
                    color=colour, bins=100, 
                    label='S (train)')
                hist, bins = np.histogram(a, bins =100)
                scale = len(a) / sum(hist)
                err = np.sqrt(hist * scale) / scale
                width = (bins[1] - bins[0])
                center = (bins[:-1] + bins[1:]) / 2
                ax.errorbar(center, hist, yerr=err, fmt='o', c=colour, label='S (train)')
                k+=1
            pp.savefig(orientation='portrait')
        
    pp.close()