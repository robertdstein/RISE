import argparse, ROOT, time
import array
from sklearn.externals import joblib

def run(lower, upper, lowercut, uppercut, BDTprob, probk = 0.0, probe = 0.0, probmu = 0.0, graph = False, text=False):
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.RooMsgService.instance().setSilentMode(True)
    
    #Generate dataset from B to K mu e raw data with selection
    
    datasource = "DATA_Bplus_Kplusmue_BDTcut_newProbNN.root"
    
    tree = "DecayTree"
    filename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource
    f = ROOT.TFile(filename)
    t = f.Get(tree)
    t.SetBranchStatus("*",0)
    t.SetBranchStatus("B_M", 1)
    t.SetBranchStatus("BDT", 1)
    t.SetBranchStatus("Kplus_newProbNNk", 1)
    t.SetBranchStatus("muplus_newProbNNmu", 1)
    t.SetBranchStatus("eminus_newProbNNe", 1)
        
    var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})",lower, upper)
    BDT = ROOT.RooRealVar("BDT", "", float(BDTprob), 1)
    
    kplus = ROOT.RooRealVar("Kplus_newProbNNk", "", 0, 1)
    muplus = ROOT.RooRealVar("muplus_newProbNNmu", "", 0, 1)
    eminus = ROOT.RooRealVar("eminus_newProbNNe", "", 0, 1)
    
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
        ds.plotOn(frame)
    
    var.setRange("R1", lower, lowercut)
    var.setRange("R2", uppercut, upper)
    var.setRange("R3", lowercut, uppercut)
    var.setRange("R4", lower, upper)

    r = exp.createNLL(ds, ROOT.RooFit.Range("R1,R2"), ROOT.RooFit.NumCPU(8))
    minu = ROOT.RooMinuit(r)
    minu.setStrategy(2)
    
    migradStatusCode = minu.migrad()
    
    hesseStatusCode = minu.hesse();
    
    result = minu.save()
    
    covarianceQuality = result.covQual()
    minosStatusCode = minu.minos()
    
    if graph == True:
        print time.asctime(time.localtime()), "Plotting data"
        exp.plotOn(frame, ROOT.RooFit.LineColor(ROOT.kRed))
        frame.Draw()
        c.Print("Bmassfit.pdf(")
        c.SetLogy()
        frame.Draw()
        c.Print("Bmassfit.pdf)")
        raw_input("prompt")
    
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
    f.Close()
    return expectedbkg, a.getVal()