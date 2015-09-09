import argparse, ROOT, time
import array
from sklearn.externals import joblib

def run(f, t, lower, upper, lowercut, uppercut, BDTprob, probk = 0.0, probe = 0.0, probmu = 0.0, text=False, graph = False):
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.RooMsgService.instance().setSilentMode(True)
    
    #Generate dataset from B to K mu e raw data with selection

        
    var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})",lower, upper)
    BDT = ROOT.RooRealVar("BDT", "", float(BDTprob), 1)
    
    kplus = ROOT.RooRealVar("Kplus_newProbNNk", "", -10, 15)
    muplus = ROOT.RooRealVar("muplus_newProbNNmu", "", -10, 15)
    eminus = ROOT.RooRealVar("eminus_newProbNNe", "", -10, 15)
    
    selection = "(B_M <" + str(lowercut) +" || B_M >" + str(uppercut) + ") && (BDT >"  + str(BDTprob) + ") && (Kplus_newProbNNk > " + str(probk) + ") && (eminus_newProbNNe > " + str(probe) + ") && (muplus_newProbNNmu > " + str(probmu) + ")" 
    
    if text ==True:
        print time.asctime(time.localtime()), "Selection contains", t.GetEntries(selection), "entries, out of a total of", t.GetEntriesFast(), "entries."
        print time.asctime(time.localtime()), "Making Data Set..."

    ds = ROOT.RooDataSet("ds", "", t, ROOT.RooArgSet(var, BDT, kplus, muplus, eminus), selection)
    
    #Fit the data, ignoring the blind region which has no events
    if text ==True:
        ds.Print()
        print time.asctime(time.localtime()), "Fitting..."

    a = ROOT.RooRealVar("a", "", -0.0017, -1., 1.)
    exp = ROOT.RooExponential("exp", "", var, a)
    
    
    if graph == True:
        c=ROOT.TCanvas()
        frame = var.frame()
        ds.plotOn(frame, ROOT.RooFit.Binning(20))
    
    var.setRange("R1", lower, lowercut)
    var.setRange("R2", uppercut, upper)
    var.setRange("R3", lowercut, uppercut)
    var.setRange("R4", lower, upper)

    minu = ROOT.RooMinuit(exp.createNLL(ds, ROOT.RooFit.Range("R1,R2"), ROOT.RooFit.NumCPU(1)))
    minu.setStrategy(2)
    
    migradStatusCode = minu.migrad()
    
    hesseStatusCode = minu.hesse()
    
    result = minu.save()
    
    covarianceQuality = result.covQual()
    minosStatusCode = minu.minos()
    
    if graph == True:
        print time.asctime(time.localtime()), "Plotting data"
        exp.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))
        frame.Draw()
        c.Print("output/Bmassfit.pdf")
    
    if text ==True:
        print time.asctime(time.localtime()), "Fit Complete!"
    
    #Calculate the expected background count in the blind region
    
    a.setConstant(True)
    
    exp.setNormRange(str(lower) + " < B_M < " + str(upper))
    
    fracInt = exp.createIntegral(ROOT.RooArgSet(var), ROOT.RooFit.Range("R3")).getVal()
    fullInt = exp.createIntegral(ROOT.RooArgSet(var), ROOT.RooFit.Range("R4")).getVal()
    if fullInt!=0 & hesseStatusCode==0 & migradStatusCode==0 & covarianceQuality==3 & minosStatusCode==0:
        prob = fracInt/fullInt
        expectedbkg = int(prob*t.GetEntries(selection)/(1-prob))
    #Pass an Error to minimisation Algorithm, if fit does not converge/has 0 counts
    else:
        expectedbkg = None
    
    minu.Delete()
    ds.Delete()
    del migradStatusCode
    del hesseStatusCode
    result.Delete()
    del covarianceQuality
    del minosStatusCode
    
    return expectedbkg, a.getVal()