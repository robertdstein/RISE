import argparse, ROOT, time
import array
from sklearn.externals import joblib

def run(f, t, CommonSelection, lower, upper, lowercut, uppercut, BDTprob, probk = 0.0, probe = 0.0, probmu = 0.0, text=False, graph = False):
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.RooMsgService.instance().setSilentMode(True)
    
    #Generate dataset from B to K mu e raw data with selection

        
    var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})",lower, upper)
    BDT = ROOT.RooRealVar("BDT", "", float(BDTprob), 1)
    
    kplus = ROOT.RooRealVar("Kplus_newProbNNk", "", -10, 15)
    muplus = ROOT.RooRealVar("muplus_newProbNNmu", "", -10, 15)
    eminus = ROOT.RooRealVar("eminus_newProbNNe", "", -10, 15)
    
    muplusghost = ROOT.RooRealVar("muplus_ProbNNghost", "", 0, 1)
    eminusghost = ROOT.RooRealVar("eminus_ProbNNghost", "", 0, 1)
    kplusghost = ROOT.RooRealVar("Kplus_ProbNNghost", "", 0, 1)
    
    MuonMass =  ROOT.RooRealVar("MuonKaonMass", "", 0, 10000)   
    ElectronMass =  ROOT.RooRealVar("ElectronKaonMass", "", 0, 10000)
    
    Bl0hadronTOS = ROOT.RooRealVar("B_L0HadronDecision_TOS", "", 0, 2)
    Bl0muonTOS = ROOT.RooRealVar("B_L0MuonDecision_TOS", "", 0, 2)
    Bl0electronTOS = ROOT.RooRealVar("B_L0ElectronDecision_TOS", "", 0, 2)
    
    Bhlt1muonTOS = ROOT.RooRealVar("B_Hlt1TrackMuonDecision_TOS", "", 0, 2)
    Bhlt1allTOS = ROOT.RooRealVar("B_Hlt1TrackAllL0Decision_TOS", "", 0, 2)
    
    Bhltmu3bodyTOS = ROOT.RooRealVar("B_Hlt2TopoMu3BodyBBDTDecision_TOS", "", 0, 2)
    Bhlt3bodyTOS = ROOT.RooRealVar("B_Hlt2Topo3BodyBBDTDecision_TOS", "", 0, 2)
    
    Bl0hadronTIS = ROOT.RooRealVar("B_L0HadronDecision_TIS", "", 0, 2)
    Bl0muonTIS = ROOT.RooRealVar("B_L0MuonDecision_TIS", "", 0, 2)
    Bl0electronTIS = ROOT.RooRealVar("B_L0ElectronDecision_TIS", "", 0, 2)
    
    Bhlt1muonTIS = ROOT.RooRealVar("B_Hlt1TrackMuonDecision_TIS", "", 0, 2)
    Bhlt1allTIS = ROOT.RooRealVar("B_Hlt1TrackAllL0Decision_TIS", "", 0, 2)
    
    Bhltmu3bodyTIS = ROOT.RooRealVar("B_Hlt2TopoMu3BodyBBDTDecision_TIS", "", 0, 2)
    Bhlt3bodyTIS = ROOT.RooRealVar("B_Hlt2Topo3BodyBBDTDecision_TIS", "", 0, 2)
    
    selection = CommonSelection + "(B_M <" + str(lowercut) +" || B_M >" + str(uppercut) + ") && (BDT >"  + str(BDTprob) + ") && (Kplus_newProbNNk > " + str(probk) + ") && (eminus_newProbNNe > " + str(probe) + ") && (muplus_newProbNNmu > " + str(probmu) + ")" 
    
    args = ROOT.RooArgSet(var, BDT, kplus, muplus, eminus, muplusghost, eminusghost, kplusghost, Bl0hadronTOS)
    args.add(Bl0muonTOS)
    args.add(Bl0electronTOS)
    
    args.add(Bhlt1allTOS)
    args.add(Bhlt1muonTOS)
    
    args.add(Bhltmu3bodyTOS)
    args.add(Bhlt3bodyTOS)
    
    args.add(Bl0hadronTIS)
    args.add(Bl0muonTIS)
    args.add(Bl0electronTIS)
    
    args.add(Bhlt1allTIS)
    args.add(Bhlt1muonTIS)
    
    args.add(Bhltmu3bodyTIS)
    args.add(Bhlt3bodyTIS)
    
    args.add(MuonMass)
    args.add(ElectronMass)
    
    
    if text ==True:
        print time.asctime(time.localtime()), "Selection contains", t.GetEntries(selection), "entries, out of a total of", t.GetEntriesFast(), "entries."
        print time.asctime(time.localtime()), "Making Data Set..."

    ds = ROOT.RooDataSet("ds", "", t, args, selection)
    
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