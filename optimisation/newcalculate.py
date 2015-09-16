import ROOT, time, os, csv, math
import numpy as np
import pylab as pl
import argparse
import branchingratio as br
import fit as f
import poisson as p
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

datasource1 = "DATA_Bplus_Kplusmue_BDTcut_newProbNN_4vectormass.root"
    
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
t1.SetBranchStatus("muplus_ProbNNghost", 1)
t1.SetBranchStatus("eminus_ProbNNghost", 1)
t1.SetBranchStatus("Kplus_ProbNNghost", 1)
t1.SetBranchStatus("B_L0HadronDecision_TOS")
t1.SetBranchStatus("B_L0MuonDecision_TOS")
t1.SetBranchStatus("B_L0ElectronDecision_TOS")
t1.SetBranchStatus("B_Hlt1TrackAllL0Decision_TOS")
t1.SetBranchStatus("B_Hlt1TrackMuonDecision_TOS")
t1.SetBranchStatus("B_Hlt2TopoMu3BodyBBDTDecision_TOS")
t1.SetBranchStatus("B_Hlt2Topo3BodyBBDTDecision_TOS")
t1.SetBranchStatus("B_L0HadronDecision_TIS")
t1.SetBranchStatus("B_L0MuonDecision_TIS")
t1.SetBranchStatus("B_L0ElectronDecision_TIS")
t1.SetBranchStatus("B_Hlt1TrackAllL0Decision_TIS")
t1.SetBranchStatus("B_Hlt1TrackMuonDecision_TIS")
t1.SetBranchStatus("B_Hlt2TopoMu3BodyBBDTDecision_TIS")
t1.SetBranchStatus("B_Hlt2Topo3BodyBBDTDecision_TIS")
t1.SetBranchStatus("ElectronKaonMass")
t1.SetBranchStatus("MuonKaonMass")

datasource2 = "MC_Bplus_Kplusmue_newresampled_Weighted_4vectormass.root"
    
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
t2.SetBranchStatus("B_L0HadronDecision_TOS")
t2.SetBranchStatus("B_L0MuonDecision_TOS")
t2.SetBranchStatus("B_L0ElectronDecision_TOS")
t2.SetBranchStatus("B_Hlt1TrackAllL0Decision_TOS")
t2.SetBranchStatus("B_Hlt1TrackMuonDecision_TOS")
t2.SetBranchStatus("B_Hlt2TopoMu3BodyBBDTDecision_TOS")
t2.SetBranchStatus("B_Hlt2Topo3BodyBBDTDecision_TOS")
t2.SetBranchStatus("B_L0HadronDecision_TIS")
t2.SetBranchStatus("B_L0MuonDecision_TIS")
t2.SetBranchStatus("B_L0ElectronDecision_TIS")
t2.SetBranchStatus("B_Hlt1TrackAllL0Decision_TIS")
t2.SetBranchStatus("B_Hlt1TrackMuonDecision_TIS")
t2.SetBranchStatus("B_Hlt2TopoMu3BodyBBDTDecision_TIS")
t2.SetBranchStatus("B_Hlt2Topo3BodyBBDTDecision_TIS")
t2.SetBranchStatus("ElectronKaonMass")
t2.SetBranchStatus("MuonKaonMass")

var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})",lowercut, uppercut)
var.setRange("R1", lowercut, uppercut)

CommonSelection = ("(muplus_ProbNNghost < 0.3) && (eminus_ProbNNghost<0.3) && (Kplus_ProbNNghost < 0.3) && (ElectronKaonMass > 1950) && (MuonKaonMass > 1950)" +
                    "&&(B_L0HadronDecision_TOS==1 || B_L0MuonDecision_TOS==1 || B_L0ElectronDecision_TOS==1 || B_L0HadronDecision_TIS==1 || B_L0MuonDecision_TIS==1 || B_L0ElectronDecision_TIS==1)"  +  
                    "&& (B_Hlt1TrackMuonDecision_TOS == 1 || B_Hlt1TrackAllL0Decision_TOS == 1 || B_Hlt1TrackMuonDecision_TIS == 1 || B_Hlt1TrackAllL0Decision_TIS == 1)" +
                    "&& (B_Hlt2TopoMu3BodyBBDTDecision_TOS==1 || B_Hlt2Topo3BodyBBDTDecision_TOS == 1 || B_Hlt2TopoMu3BodyBBDTDecision_TIS==1 || B_Hlt2Topo3BodyBBDTDecision_TIS == 1) &&")

def output(bdt=0.976, probk=-1.5, probmu=1.45, probe=0.9, countoutput=False, text=False, graph=False, sigma=5):
    #Fit to find expected background count and exponential distribution parameter
    
    expcount, aval = f.run(file1, t1, CommonSelection, lower, upper, lowercut, uppercut, bdt, probk, probmu, probe, text=text, graph=graph)
    
    if expcount != None:
        partselection = ("(BDT >"  + str(bdt) + ") && (Kplus_PIDK_corrected > " + str(probk) + ") && (muplus_PIDmu_corrected > " + 
                        str(probmu) + ") && (eminus_PIDe_corrected > " + str(probe) +
                        ")&& (Kplus_isMuonLoose == 0) && (Kplus_InAccMuon==1) && (Psi_M < 3000 || Psi_M >3200) && (B_BKGCAT == 10)")
    
        selection = CommonSelection + "(B_M < " + str(uppercut) + ") && (B_M > " + str(lowercut) + " ) && " + partselection
        
        if int(sigma) == 2:
            percentage = 0.95
        
        elif int(sigma) == 5:
            percentage = 0.999999426697        
        
        signal = p.getExpectedLimit(expcount, percentage)
        
        entries = signal + expcount
        
        ratio, error = br.run(signal, entries, file2, t2, selection)     
                    
        #return ratio and error for the purpose of a csv output and graph
        if countoutput == True:
            return ratio, error
        #return just the ratio, for the purpose of minimisation
        else:
            return ratio
    #If the fit has not converged, or expected count is 0, return error
    else:
        return float('nan')