import ROOT, time
from sklearn import ensemble
import numpy as np
import matplotlib.pyplot as plt
import argparse
import csv
from sklearn.externals import joblib
from sklearn.decomposition import IncrementalPCA, PCA
import array
import itertools
from scipy import linalg
import matplotlib as mpl
from sklearn import mixture 

name = "ul"   
ncategories = 30
filename = "/net/storage03/data/users/rstein/tuples/qsq/DATA_Bplus_Kplusmumu_qsqcut.root"
accepted_categories = [1, 7]
add_branch = True
cut_tree= True

if add_branch == True:
   
    print time.asctime(time.localtime()), "Creating Tree"

    f = ROOT.TFile(filename)
    t = f.Get("DecayTree")
    
    lim = joblib.load("pickle/limits.pkl")
    data = joblib.load('pickle/' + name + 'data.pkl')
  
    sourcefit = int(len(lim) + 1)
    maxcategory = ncategories +1

    nFileName = "/net/storage03/data/users/rstein/tuples/qsq/" + name+ "_data.root"
    print('saving File to ' + nFileName)

    nf = ROOT.TFile(nFileName, "RECREATE")
    print time.asctime(time.localtime()), "Cloning Tree"
    nt = t.CloneTree(-1, 'fast')

    nt.SetBranchStatus("*", 0)

    group = (array.array('i',[0]))
    groupBranch = nt.Branch("group", group, "group/I")

    print time.asctime(time.localtime()), "Filling Group Branch"

    print "itterating over", nt.GetEntries() , "events"
    for i in range(nt.GetEntries()):
        l=data[i]
        group[0] = l[sourcefit]
        groupBranch.Fill()

    nt.SetBranchStatus("*", 1)
    nt.Write("DecayTree")
    nf.Close()
    f.Close()
    
if cut_tree == True:

    print time.asctime(time.localtime()), "Creating Second Tree"

    h = ROOT.TFile(filename, "READ")
    v = h.Get("DecayTree")
    g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + name+ "_datacut.root", "recreate")

    selection = "(B_M < 7000)"
    for i in accepted_categories:
        selection += " && (group == " + i + ")"

    vcount = v.GetEntriesFast()
    print time.asctime(time.localtime()), "Contains", vcount, "entries"
    print time.asctime(time.localtime()), "Contains", v.GetEntries(selection), "entries to be copied"

    print time.asctime(time.localtime()), "Cloning Tree..."
    nt=v.CopyTree(selection)

    print time.asctime(time.localtime()), "Tree Cloned!"

    g.Close()

    print time.asctime(time.localtime()), "Branch Filled!"