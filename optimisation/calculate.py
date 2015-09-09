import ROOT, time, os, csv
import numpy as np
import pylab as pl
import argparse
import branchingratio as br
import fit as f
import simulate as s
from iminuit import Minuit

#Fix blinded region and B Mass fit range

lower=4500
upper=6250
lowercut=5100
uppercut=5400

ROOT.gROOT.SetBatch(True)
ROOT.RooAbsData.setDefaultStorageType(ROOT.RooAbsData.Tree)

#Opens the necessary Trees

datasource1 = "DATA_Bplus_Kplusmue_BDTcut_newProbNN.root"
    
tree1 = "DecayTree"
filename1 = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource1
file1 = ROOT.TFile(filename1)
t1 = file1.Get(tree1)
t1.SetBranchStatus("*",0)
t1.SetBranchStatus("B_M", 1)
t1.SetBranchStatus("BDT", 1)
t1.SetBranchStatus("Kplus_newProbNNk", 1)
t1.SetBranchStatus("muplus_newProbNNmu", 1)
t1.SetBranchStatus("eminus_newProbNNe", 1)

datasource2 = "MC_Bplus_Kplusmue_newresampled_Weighted.root"
    
tree2 = "default"
filename2 = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource2
file2 = ROOT.TFile(filename2)
t2 = file2.Get(tree2)
t2.SetBranchStatus("*",0)
t2.SetBranchStatus("B_M", 1)
t2.SetBranchStatus("BDT", 1)
t2.SetBranchStatus("Kplus_PIDK_corrected", 1)
t2.SetBranchStatus("muplus_PIDmu_corrected", 1)
t2.SetBranchStatus("eminus_PIDe_corrected", 1)
t2.SetBranchStatus("Kplus_isMuonLoose", 1)
t2.SetBranchStatus("Kplus_InAccMuon", 1)
t2.SetBranchStatus("muplus_ProbNNghost", 1)
t2.SetBranchStatus("eminus_ProbNNghost", 1)
t2.SetBranchStatus("Kplus_ProbNNghost", 1)
t2.SetBranchStatus("Psi_M", 1)
t2.SetBranchStatus("B_BKGCAT", 1)


var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})",lowercut, uppercut)
var.setRange("R1", lowercut, uppercut)

c = ROOT.TCanvas()

def output(bdt=0.96, probk=-2.0, probmu=2.0, probe=-10, countoutput=False, text=False, dynamic=False, graph =False):
    #Fit to find expected background count and exponential distribution parameter
    expcount, aval = f.run(file1, t1, lower, upper, lowercut, uppercut, bdt, probk, probmu, probe, text=text, graph=graph)
    count = 17
    significance = False
    #iteratively add counts to the signal peak until it has a 5 sigma significance
    if expcount != None:
        while significance != True:
            sig, entries, significance, peak, sigma, selection = s.run(file2, t2, var, lower, upper, lowercut, uppercut, bdt, expcount, aval, count, probk, probmu, probe, text=text, graph=graph)
            if (dynamic == True) & (peak < 3.0):
                if sigma < (expcount * 0.2):
                    count += (int(sigma) +1)
                else:
                    count +=20
            else:
                count += int(sigma*0.01) +1
        ratio, error = br.run(sig, entries, file2, t2, selection)
        #return ratio and error for the purpose of a csv output and graph
        if countoutput == True:
            return ratio, error
        #return just the ratio, for the purpose of minimisation
        else:
            return ratio
    #If the fit has not converged, or expected count is 0, return error
    else:
        return float('nan')