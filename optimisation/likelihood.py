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

randomcount =10000

CommonSelection = ("(muplus_ProbNNghost < 0.3) && (eminus_ProbNNghost<0.3) && (Kplus_ProbNNghost < 0.3) && (ElectronKaonMass > 1950) && (MuonKaonMass > 1950)" +
                    "&&(B_L0HadronDecision_TOS==1 || B_L0MuonDecision_TOS==1 || B_L0ElectronDecision_TOS==1 || B_L0HadronDecision_TIS==1 || B_L0MuonDecision_TIS==1 || B_L0ElectronDecision_TIS==1)"  +  
                    "&& (B_Hlt1TrackMuonDecision_TOS == 1 || B_Hlt1TrackAllL0Decision_TOS == 1 || B_Hlt1TrackMuonDecision_TIS == 1 || B_Hlt1TrackAllL0Decision_TIS == 1)" +
                    "&& (B_Hlt2TopoMu3BodyBBDTDecision_TOS==1 || B_Hlt2Topo3BodyBBDTDecision_TOS == 1 || B_Hlt2TopoMu3BodyBBDTDecision_TIS==1 || B_Hlt2Topo3BodyBBDTDecision_TIS == 1) &&")
                    
rand = ROOT.RooRandom.randomGenerator()

def output(bdt=0.97, probk=-2.0, probmu=2.0, probe=2.0, countoutput=False, text=False, graph=False):
    #Fit to find expected background count and exponential distribution parameter
    
    expcount, aval = f.run(file1, t1, CommonSelection, lower, upper, lowercut, uppercut, bdt, probk, probmu, probe, text=text, graph=graph)
    
    if expcount != None:
        
#        ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
#        ROOT.RooMsgService.instance().setSilentMode(True)
#        ROOT.SetMemoryPolicy( ROOT.kMemoryStrict )
#        ROOT.RooAbsData.setDefaultStorageType(ROOT.RooAbsData.Tree) 
#        
#        #Create a Monte Carlo dataset with a selection   
#    
#        BDT = ROOT.RooRealVar("BDT", "", float(bdt), 1)
#    
#        kplus = ROOT.RooRealVar("Kplus_PIDK_corrected", "", -10, 15)
#        muplus = ROOT.RooRealVar("muplus_PIDmu_corrected", "", -10, 15)
#        eminus = ROOT.RooRealVar("eminus_PIDe_corrected", "", -10, 15)
#    
#        kplusmuonloose = ROOT.RooRealVar("Kplus_isMuonLoose", "", 0.0, 1)
#        kplusinaccmuon = ROOT.RooRealVar("Kplus_InAccMuon", "", 0, 1)
#        muplusghost = ROOT.RooRealVar("muplus_ProbNNghost", "", 0, 1)
#        eminusghost = ROOT.RooRealVar("eminus_ProbNNghost", "", 0, 1)
#        kplusghost = ROOT.RooRealVar("Kplus_ProbNNghost", "", 0, 1)
#        psim = ROOT.RooRealVar("Psi_M", "", 0, uppercut)  
#        bkgcat = ROOT.RooRealVar("B_BKGCAT", "", 0, 100)
#        
#        MuonMass =  ROOT.RooRealVar("MuonKaonMass", "", 0, 10000)   
#        ElectronMass =  ROOT.RooRealVar("ElectronKaonMass", "", 0, 10000)
#        
#        Bl0hadronTOS = ROOT.RooRealVar("B_L0HadronDecision_TOS", "", 0, 2)
#        Bl0muonTOS = ROOT.RooRealVar("B_L0MuonDecision_TOS", "", 0, 2)
#        Bl0electronTOS = ROOT.RooRealVar("B_L0ElectronDecision_TOS", "", 0, 2)
#        
#        Bhlt1muonTOS = ROOT.RooRealVar("B_Hlt1TrackMuonDecision_TOS", "", 0, 2)
#        Bhlt1allTOS = ROOT.RooRealVar("B_Hlt1TrackAllL0Decision_TOS", "", 0, 2)
#    
#        Bhltmu3bodyTOS = ROOT.RooRealVar("B_Hlt2TopoMu3BodyBBDTDecision_TOS", "", 0, 2)
#        Bhlt3bodyTOS = ROOT.RooRealVar("B_Hlt2Topo3BodyBBDTDecision_TOS", "", 0, 2)
#    
#        Bl0hadronTIS = ROOT.RooRealVar("B_L0HadronDecision_TIS", "", 0, 2)
#        Bl0muonTIS = ROOT.RooRealVar("B_L0MuonDecision_TIS", "", 0, 2)
#        Bl0electronTIS = ROOT.RooRealVar("B_L0ElectronDecision_TIS", "", 0, 2)
#    
#        Bhlt1muonTIS = ROOT.RooRealVar("B_Hlt1TrackMuonDecision_TIS", "", 0, 2)
#        Bhlt1allTIS = ROOT.RooRealVar("B_Hlt1TrackAllL0Decision_TIS", "", 0, 2)
#    
#        Bhltmu3bodyTIS = ROOT.RooRealVar("B_Hlt2TopoMu3BodyBBDTDecision_TIS", "", 0, 2)
#        Bhlt3bodyTIS = ROOT.RooRealVar("B_Hlt2Topo3BodyBBDTDecision_TIS", "", 0, 2)
#    
        partselection = ("(BDT >"  + str(bdt) + ") && (Kplus_PIDK_corrected > " + str(probk) + ") && (muplus_PIDmu_corrected > " + 
                        str(probmu) + ") && (eminus_PIDe_corrected > " + str(probe) +
                        ")&& (Kplus_isMuonLoose == 0) && (Kplus_InAccMuon==1) && (Psi_M < 3000 || Psi_M >3200) && (B_BKGCAT == 10)")
    
        selection = CommonSelection + "(B_M < " + str(uppercut) + ") && (B_M > " + str(lowercut) + " ) && " + partselection
    
#        args = ROOT.RooArgSet(var, BDT, kplus, muplus, eminus, kplusmuonloose, kplusinaccmuon, psim, bkgcat)
#        args.add(muplusghost)
#        args.add(kplusghost)
#        args.add(eminusghost)
#        
#        args.add(MuonMass)
#        args.add(ElectronMass)
#    
#        args.add(Bl0hadronTOS)
#        args.add(Bl0muonTOS)
#        args.add(Bl0electronTOS)
#    
#        args.add(Bhlt1allTOS)
#        args.add(Bhlt1muonTOS)
#    
#        args.add(Bhltmu3bodyTOS)
#        args.add(Bhlt3bodyTOS)
#    
#        args.add(Bl0hadronTIS)
#        args.add(Bl0muonTIS)
#        args.add(Bl0electronTIS)
#    
#        args.add(Bhlt1allTIS)
#        args.add(Bhlt1muonTIS)
#    
#        args.add(Bhltmu3bodyTIS)
#        args.add(Bhlt3bodyTIS)
#
#        ds = ROOT.RooDataSet("ds", "", t2, args, selection)
#
#        mean = ROOT.RooRealVar("mean", "", 5285, lowercut, uppercut)
#
#        sigma1 = ROOT.RooRealVar("sigma1", "", 49.6, 0, 100)
#        alpha1 = ROOT.RooRealVar("alpha1", "", -1.14, -20, 0)
#        n1 = ROOT.RooRealVar("n1", "", 2.54, 0, 100)
#
#        sigma2 = ROOT.RooRealVar("sigma2", "", 18.4, 0, 100)
#        alpha2 = ROOT.RooRealVar("alpha2", "", 0.31, 0, 20)
#        n2 = ROOT.RooRealVar("n2", "", 2.18, 0, 100)
#         
#        frac = ROOT.RooRealVar("frac", "", 0.5, 0, 1)
#
#        cb1 = ROOT.RooCBShape("cb1","", var, mean, sigma1, alpha1, n1)
#        cb2 = ROOT.RooCBShape("cb2","", var, mean, sigma2, alpha2, n2)
#        sigModel = ROOT.RooAddPdf ("sigModel", "", ROOT.RooArgList(cb1, cb2), ROOT.RooArgList(frac))
#    
#        sigModel.fitTo(ds, ROOT.RooFit.Range("R1"), ROOT.RooFit.NumCPU(1))
#           
#        sigma1.setConstant(True)
#        sigma2.setConstant(True)
#        alpha1.setConstant(True)
#        alpha2.setConstant(True)
#        n1.setConstant(True)
#        n2.setConstant(True)
#        mean.setConstant(True)
#        frac.setConstant(True)
#    
#        #Generate background data
#    
#        a = ROOT.RooRealVar("a", "", aval)
#        exp = ROOT.RooExponential("exp", "", var, a)
#        
#        signalYield = ROOT.RooRealVar("signalYield", "", 5*float(expcount), 0, 10*float(expcount))
#        combinatorialYield = ROOT.RooRealVar("combinatorialYield", "", expcount)
#
#        fullModel = ROOT.RooAddPdf("fullmodel", "", ROOT.RooArgList(sigModel, exp), ROOT.RooArgList(signalYield, combinatorialYield))
#        
#        sigarray = []
#        
#        #Calculate upper limit on branching ratio in a loop, and calculate average
#        
#        print time.asctime(time.localtime()), "Starting Generation"
#        for i in range(randomcount):
#            rand.SetSeed(0)
#
#            bkgsim =exp.generate(ROOT.RooArgSet(var, BDT, kplus, muplus, eminus), int(expcount))
#        
#            plc = ROOT.RooStats.ProfileLikelihoodCalculator(bkgsim, fullModel, ROOT.RooArgSet(signalYield))
#            plc.SetConfidenceLevel(0.999999426697)
#            interval = plc.GetInterval()
#        
#            sig = interval.UpperLimit(signalYield)
#            sigarray.append(sig)
#            
#            bkgsim.Delete()
#            interval.Delete()
#            del interval, bkgsim, sig, plc
#
#        signal = np.mean(sigarray)
#        
#        #Delete Everything!!!!!
#        
#        sigModel.Delete()
#        fullModel.Delete()
#        signalYield.Delete()
#        a.Delete()
#        exp.Delete()
#        combinatorialYield.Delete()
#        args.Delete()
#        BDT.Delete()
#        del sigarray
#        ds.Delete()
#        kplus.Delete()
#        muplus.Delete()
#        eminus.Delete()
#    
#        kplusmuonloose.Delete()
#        kplusinaccmuon.Delete()
#        muplusghost.Delete()
#        eminusghost.Delete()
#        kplusghost.Delete()
#        psim.Delete() 
#        bkgcat.Delete()
#        
#        MuonMass.Delete() 
#        ElectronMass.Delete()
#        
#        Bl0hadronTOS.Delete()
#        Bl0muonTOS.Delete()
#        Bl0electronTOS.Delete()
#        
#        Bhlt1muonTOS.Delete()
#        Bhlt1allTOS.Delete()
#    
#        Bhltmu3bodyTOS.Delete()
#        Bhlt3bodyTOS.Delete()
#    
#        Bl0hadronTIS.Delete()
#        Bl0muonTIS.Delete()
#        Bl0electronTIS.Delete()
#    
#        Bhlt1muonTIS.Delete()
#        Bhlt1allTIS.Delete()
#    
#        Bhltmu3bodyTIS.Delete()
#        Bhlt3bodyTIS.Delete()
#        
#        mean.Delete()
#
#        sigma1.Delete()
#        alpha1.Delete()
#        n1.Delete()
#
#        sigma2.Delete()
#        alpha2.Delete()
#        n2.Delete()
#         
#        frac.Delete()
#
#        cb1.Delete()
#        cb2.Delete()

        signal = p.getExpectedLimit(expcount)
        
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