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

defaultbdtcut = 0.95
defaultkcut = -3.0
defaultecut = 4.0
defaultmucut = 1.0

ROOT.gROOT.SetBatch(True)
ROOT.RooAbsData.setDefaultStorageType(ROOT.RooAbsData.Tree)

datasource1 = "DATA_Bplus_Kplusmumu_qsq_sweight_newProbNN.root"
    
tree = "DecayTree"
filename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource1
f = ROOT.TFile(filename)
t = f.Get(tree1)
t.SetBranchStatus("*",0)
t.SetBranchStatus("B_M", 1)
t.SetBranchStatus("BDT", 1)
t.SetBranchStatus("Kplus_newProbNNk", 1)
t.SetBranchStatus("muplus_newProbNNmu", 1)
t.SetBranchStatus("eminus_newProbNNe", 1)

var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})",lowercut, uppercut)
var.setRange("R1", lowercut, uppercut)

BDT = ROOT.RooRealVar("BDT", "", 0, 1)
    
kplus = ROOT.RooRealVar("Kplus_PIDK_corrected", "", -10, 15)
muplus = ROOT.RooRealVar("muplus_PIDmu_corrected", "", -10, 15)
eminus = ROOT.RooRealVar("eminus_PIDe_corrected", "", -10, 15)
    
kplusmuonloose = ROOT.RooRealVar("Kplus_isMuonLoose", "", 0.0, 1)
kplusinaccmuon = ROOT.RooRealVar("Kplus_InAccMuon", "", 0, 1)
muplusghost = ROOT.RooRealVar("muplus_ProbNNghost", "", 0, 1)
eminusghost = ROOT.RooRealVar("eminus_ProbNNghost", "", 0, 1)
kplusghost = ROOT.RooRealVar("Kplus_ProbNNghost", "", 0, 1)
psim = ROOT.RooRealVar("Psi_M", "", 0, uppercut)    
    
partselection = "(BDT >"  + str(BDTprob) + ") && (Kplus_PIDK_corrected > " + str(probk) + ") && (muplus_PIDmu_corrected > " + str(probmu) + ") && (eminus_PIDe_corrected > " + str(probe) +")&& (Kplus_isMuonLoose == 0) && (Kplus_InAccMuon == 1) && (Psi_M < 3000 || Psi_M >3200)"
    
selection = "(B_M < " + str(uppercut) + ") && (B_M > " + str(lowercut) + " ) && " + partselection

print time.asctime(time.localtime()), "Selection contains", t.GetEntries(selection), "entries, out of a total of", t.GetEntriesFast(), "entries."
print time.asctime(time.localtime()), "Making Data Set..."

ds = ROOT.RooDataSet("ds", "", t, ROOT.RooArgSet(var, BDT, kplus, muplus, eminus, kplusmuonloose, kplusinaccmuon, psim), partselection)

ds.Print()
    
#Fit the Monte Carlo signal peak
print time.asctime(time.localtime()), "Fitting..."

mean = ROOT.RooRealVar("mean", "", 5285, lowercut, uppercut)
sigma1 = ROOT.RooRealVar("sigma1", "", 49.6, 0, 100)
alpha1 = ROOT.RooRealVar("alpha1", "", -1.14, -20, 0)
n1 = ROOT.RooRealVar("n1", "", 2.54, 0, 100)
sigma2 = ROOT.RooRealVar("sigma2", "", 18.4, 0, 100)
alpha2 = ROOT.RooRealVar("alpha2", "", 0.31, 0, 20)
n2 = ROOT.RooRealVar("n2", "", 2.18, 0, 100)
         
frac = ROOT.RooRealVar("frac", "", 0.5, 0, 1)

cb1 = ROOT.RooCBShape("cb1","", var, mean, sigma1, alpha1, n1)
cb2 = ROOT.RooCBShape("cb2","", var, mean, sigma2, alpha2, n2)
sigModel = ROOT.RooAddPdf ("sigModel", "", ROOT.RooArgList(cb1, cb2), ROOT.RooArgList(frac))
    
if graph == True:
    frame = var.frame()
    ds.plotOn(frame)
    
sigModel.fitTo(ds, ROOT.RooFit.Range("R1"), ROOT.RooFit.NumCPU(1))

if graph == True:    
    sigModel.plotOn(frame)
    sigModel.plotOn(frame, ROOT.RooFit.Components("sigModel"), ROOT.RooFit.LineColor(ROOT.kGreen))
    c=ROOT.TCanvas()
    c.Divide(2,1)
    c.cd(1)
    print time.asctime(time.localtime()), "Plotting data"
    frame.Draw()
    
if text ==True:
    print time.asctime(time.localtime()), "Fit Complete"
           
sigma1.setConstant(True)
sigma2.setConstant(True)
alpha1.setConstant(True)
alpha2.setConstant(True)
n1.setConstant(True)
n2.setConstant(True)
mean.setConstant(True)
frac.setConstant(True)