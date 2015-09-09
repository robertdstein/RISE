import argparse, ROOT, time
import math
from sklearn.externals import joblib
from uncertainties import ufloat

def run(f, t, var, lower, upper, lowercut, uppercut, BDTprob, expcount, aval, count, probk =0.0, probe = 0.0, probmu = 0.0, text = False, graph = False):
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.RooMsgService.instance().setSilentMode(True)
    
    #Create a Monte Carlo dataset with a selection   
    
    BDT = ROOT.RooRealVar("BDT", "", float(BDTprob), 1)
    
    kplus = ROOT.RooRealVar("Kplus_PIDK_corrected", "", -10, 15)
    muplus = ROOT.RooRealVar("muplus_PIDmu_corrected", "", -10, 15)
    eminus = ROOT.RooRealVar("eminus_PIDe_corrected", "", -10, 15)
    
    kplusmuonloose = ROOT.RooRealVar("Kplus_isMuonLoose", "", 0.0, 1)
    kplusinaccmuon = ROOT.RooRealVar("Kplus_InAccMuon", "", 0, 1)
    muplusghost = ROOT.RooRealVar("muplus_ProbNNghost", "", 0, 1)
    eminusghost = ROOT.RooRealVar("eminus_ProbNNghost", "", 0, 1)
    kplusghost = ROOT.RooRealVar("Kplus_ProbNNghost", "", 0, 1)
    psim = ROOT.RooRealVar("Psi_M", "", 0, uppercut)  
    bkgcat = ROOT.RooRealVar("B_BKGCAT", "", 0, 100)  
    
    partselection = "(BDT >"  + str(BDTprob) + ") && (Kplus_PIDK_corrected > " + str(probk) + ") && (muplus_PIDmu_corrected > " + str(probmu) + ") && (eminus_PIDe_corrected > " + str(probe) +")&& (Kplus_isMuonLoose == 0) && (Kplus_InAccMuon==1) && (Psi_M < 3000 || Psi_M >3200) && (B_BKGCAT == 10)"
    
    selection = "(B_M < " + str(uppercut) + ") && (B_M > " + str(lowercut) + " ) && " + partselection
    
    if text ==True:
        print time.asctime(time.localtime()), "Selection contains", t.GetEntries(selection), "entries, out of a total of", t.GetEntriesFast(), "entries."
        print time.asctime(time.localtime()), "Making Data Set..."

    ds = ROOT.RooDataSet("ds", "", t, ROOT.RooArgSet(var, BDT, kplus, muplus, eminus, kplusmuonloose, kplusinaccmuon, psim, bkgcat), partselection)
    
    if text ==True:
        ds.Print()
    
    #Fit the Monte Carlo signal peak
    if text ==True:
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
    
    #Generate composite signal/background data
    
    a = ROOT.RooRealVar("a", "", aval)
    exp = ROOT.RooExponential("exp", "", var, a)
    
    sigsim =sigModel.generate(ROOT.RooArgSet(var, BDT, kplus, muplus, eminus), float(count))

    bkgsim =exp.generate(ROOT.RooArgSet(var, BDT, kplus, muplus, eminus), float(expcount))
    
    if text == True:
        sigsim.Print()
        bkgsim.Print()
    
    bkgsim.append(sigsim)

    newdata = bkgsim
    
    if graph == True:
        frame = var.frame()
        newdata.plotOn(frame, ROOT.RooFit.Binning(10))

    signalYield = ROOT.RooRealVar("signalYield", "", float(count), 0, 100*float(count))
    combinatorialYield = ROOT.RooRealVar("combinatorialYield", "", expcount, 0, 10*expcount)

    fullModel = ROOT.RooAddPdf("fullmodel", "", ROOT.RooArgList(sigModel, exp), ROOT.RooArgList(signalYield, combinatorialYield))
    
    r = fullModel.fitTo(newdata, ROOT.RooFit.NumCPU(1))
    
    if graph == True:    
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
        if text ==True:
            print time.asctime(time.localtime()), "Signal Peak with", int(sig), "events has a 5 sigma significance. (Sigma =", err, ")"
    elif sig < err*5:
        significance = False
        if text ==True:
            print time.asctime(time.localtime()), "Signal Peak with", int(sig), "events is not significant. (Sigma =", err, ")"
    
    if text ==True:
        print time.asctime(time.localtime()), "Peak is", peak, "Sigma"

    if graph == True:
        c.cd(2)
        print time.asctime(time.localtime()), "Plotting data"
        frame.Draw()
        c.Print("output/newBmassfit.pdf")
           
    sigsim.Delete()
    ds.Delete()
    bkgsim.Delete()
    newdata.Delete()
    sigModel.Delete()
    fullModel.Delete()

    if r:
        del r
        
    return ufloat(sig,err), t.GetEntries(selection), significance, peak, err, selection