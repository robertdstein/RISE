import argparse, ROOT, time
import math
from sklearn.externals import joblib
from uncertainties import ufloat

def run(lower, upper, lowercut, uppercut, BDTprob, expcount, count, probk =0.0, probe = 0.0, probmu = 0.0, graph = False):
    print time.asctime(time.localtime()),"Supressing Fit Output"
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.RooMsgService.instance().setSilentMode(True)
    
    #Create a Monte Carlo dataset with a selection
    
    datasource = "MC_Bplus_Kplusmue_resampled.root"
    
    tree = "default"
    filename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource
    f = ROOT.TFile(filename)
    t = f.Get(tree)
    t.SetBranchStatus("*",0)
    t.SetBranchStatus("B_M", 1)
    t.SetBranchStatus("BDT", 1)
    t.SetBranchStatus("Kplus_PIDK_corrected", 1)
    t.SetBranchStatus("muplus_PIDmu_corrected", 1)
    t.SetBranchStatus("eminus_PIDe_corrected", 1)
    t.SetBranchStatus("Kplus_isMuonLoose", 1)
    t.SetBranchStatus("Kplus_InAccMuon", 1)
    t.SetBranchStatus("muplus_ProbNNghost", 1)
    t.SetBranchStatus("eminus_ProbNNghost", 1)
    t.SetBranchStatus("Kplus_ProbNNghost", 1)
    t.SetBranchStatus("Psi_M", 1)    
    
    var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})",lowercut, uppercut)
    BDT = ROOT.RooRealVar("BDT", "", float(BDTprob), 1)
    
    kplus = ROOT.RooRealVar("Kplus_PIDK_corrected", "", 0.0, 1)
    muplus = ROOT.RooRealVar("muplus_PIDmu_corrected", "", 0, 1)
    eminus = ROOT.RooRealVar("eminus_PIDe_corrected", "", 0, 1)
    
    kplusmuonloose = ROOT.RooRealVar("Kplus_isMuonLoose", "", 0.0, 1)
    kplusinaccmuon = ROOT.RooRealVar("Kplus_InAccMuon", "", 0, 1)
    muplusghost = ROOT.RooRealVar("muplus_ProbNNghost", "", 0, 1)
    eminusghost = ROOT.RooRealVar("eminus_ProbNNghost", "", 0, 1)
    kplusghost = ROOT.RooRealVar("Kplus_ProbNNghost", "", 0, 1)
    psim = ROOT.RooRealVar("Psi_M", "", 0, 1)    
       
    
    partselection = "(BDT >"  + str(BDTprob) + ") && (Kplus_PIDK_corrected > " + str(probk) + ") && (muplus_PIDmu_corrected > " + str(probmu) + ") && (eminus_PIDe_corrected > " + str(probe) +")&& (Kplus_isMuonLoose == 0) && (Kplus_InAccMuon == 1) && (eminus_PIDe_corrected > 0.05) && (Kplus_PIDK_corrected > 0.05) && (muplus_PIDmu_corrected > 0.05) && (Psi_M < 3000 || Psi_M >3200)"
    
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

    frame = var.frame()
    ds.plotOn(frame)
    
    var.setRange("R1", lowercut, uppercut)
    r = sigModel.fitTo(ds, ROOT.RooFit.Range("R1"), ROOT.RooFit.Save(True), ROOT.RooFit.NumCPU(12))
    sigModel.plotOn(frame)
    sigModel.plotOn(frame, ROOT.RooFit.Components("sigModel"), ROOT.RooFit.LineColor(ROOT.kGreen))

    if graph == True:    
        c=ROOT.TCanvas()
        c.Divide(2,1)
        c.cd(1)
        print time.asctime(time.localtime()), "Plotting data"
        frame.Draw()
    
    print time.asctime(time.localtime()), "Fit Complete"    
           
    sigma1.setConstant(True)
    sigma2.setConstant(True)
    alpha1.setConstant(True)
    alpha2.setConstant(True)
    n1.setConstant(True)
    n2.setConstant(True)
    mean.setConstant(True)
    frac.setConstant(True)
    
    #Generate composite signal/background data
    
    bkg = joblib.load('pickle/background.pkl')
    a = ROOT.RooRealVar("a", "", bkg)
    exp = ROOT.RooExponential("exp", "", var, a)
    
    sigsim =sigModel.generate(ROOT.RooArgSet(var, BDT, kplus, muplus, eminus), float(count))
    sigsim.Print()
    
    bkgsim =exp.generate(ROOT.RooArgSet(var, BDT, kplus, muplus, eminus), float(expcount))
    bkgsim.Print()
    
    frame = var.frame()
    bkgsim.append(sigsim)

    newdata = bkgsim
    newdata.plotOn(frame)

    signalYield = ROOT.RooRealVar("signalYield", "", float(count), 0, 100*float(count))
    combinatorialYield = ROOT.RooRealVar("combinatorialYield", "", expcount, 0, 10*expcount)

    fullModel = ROOT.RooAddPdf("fullmodel", "", ROOT.RooArgList(sigModel, exp), ROOT.RooArgList(signalYield, combinatorialYield))
    
    r = fullModel.fitTo(newdata, ROOT.RooFit.Save(True), ROOT.RooFit.NumCPU(8))
    fullModel.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kOrange))
    fullModel.plotOn(frame, ROOT.RooFit.Components("sigModel"), ROOT.RooFit.LineColor(ROOT.kGreen))
    fullModel.plotOn(frame, ROOT.RooFit.VisualizeError(r,5), ROOT.RooFit.Components("exp"), ROOT.RooFit.FillColor(ROOT.kRed))
    
    signalYield.setConstant(True)
    sig = signalYield.getVal()
    err = signalYield.getError()
    if err != 0:
        peak = sig/err
    else:
        peak = None
    
    #Check whether data has a 5 sigma significant peak
    
    if sig > err*5:
        significance = True
        print time.asctime(time.localtime()), "Signal Peak with", int(sig), "events has a 5 sigma significance. (Sigma =", err, ")"
    elif sig < err*5:
        significance = False
        print time.asctime(time.localtime()), "Signal Peak with", int(sig), "events is not significant. (Sigma =", err, ")"
    
    print time.asctime(time.localtime()), "Peak is", peak, "Sigma"

    if graph == True:
        c.cd(2)
        print time.asctime(time.localtime()), "Plotting data"
        frame.Draw()
        c.Print("newBmassfit.pdf")
        raw_input("prompt")
        
    efficiency = float(t.GetEntries(selection))/float(t.GetEntriesFast())
    print time.asctime(time.localtime()), "Efficiency is", efficiency
    return ufloat(sig,err), efficiency, significance, peak