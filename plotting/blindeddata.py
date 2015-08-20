import argparse, ROOT, time
import lhcbStyle as lhcb
import array

start = time.time()

parser = argparse.ArgumentParser(description='Fit for B_M from dataset')
parser.add_argument('-s', '--source', type=str,  choices=['data', 'sim'], default="data")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-l", "--mlower", default=4500)
parser.add_argument("-u", "--mupper", default=6250)
parser.add_argument("-c", "--cut", action="store_true")
parser.add_argument("-i", "--interpolate", action="store_true")
parser.add_argument("-f", "--fixed", action="store_true")

cfg = parser.parse_args()
if not cfg.debug:
    print time.asctime(time.localtime()), "supressing fit output"
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
    ROOT.RooMsgService.instance().setSilentMode(True)

lhcb.setLHCbStyle()

if cfg.source == "data":
    datasource = "DATA_Bplus_Kplusmue_qsqcut"

if cfg.source == "sim":
    datasource = "MC_Bplus_Kplusmue_qsqcut"

tree = "DecayTree"
filename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource + ".root"
f = ROOT.TFile(filename)
t = f.Get(tree)

lowercut = 5120
uppercut = 5420

bincount = 100    
mean = ROOT.RooRealVar("mean", "", 5270, int(cfg.mlower), int(cfg.mupper))

var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})", int(cfg.mlower), int(cfg.mupper))

sigma1 = ROOT.RooRealVar("sigma1", "", 49.6, 0, 100)
alpha1 = ROOT.RooRealVar("alpha1", "", -1.14, -20, 0)
n1 = ROOT.RooRealVar("n1", "", 2.54, 0, 100)

sigma2 = ROOT.RooRealVar("sigma2", "", 18.4, 0, 100)
alpha2 = ROOT.RooRealVar("alpha2", "", 0.31, 0, 20)
n2 = ROOT.RooRealVar("n2", "", 2.18, 0, 100)

a = ROOT.RooRealVar("a", "", -0.0017, -1., 1.)
         
frac = ROOT.RooRealVar("frac", "", 0.5, 0, 1)

cb1 = ROOT.RooCBShape("cb1","", var, mean, sigma1, alpha1, n1)
cb2 = ROOT.RooCBShape("cb2","", var, mean, sigma2, alpha2, n2)
exp = ROOT.RooExponential("exp", "", var, a)
sigModel = ROOT.RooAddPdf ("sigModel", "", ROOT.RooArgList(cb1, cb2), ROOT.RooArgList(frac))

signalYield = ROOT.RooRealVar("signalYield", "", 1530000, 0, 2400000)
combinatorialYield = ROOT.RooRealVar("combinatorialYield", "", 870000, 0, 2400000)

fullModel = ROOT.RooAddPdf("fullmodel", "", ROOT.RooArgList(sigModel, exp), ROOT.RooArgList(signalYield, combinatorialYield))

if cfg.fixed == True:
    sigma1.setConstant(True)
    sigma2.setConstant(True)
    alpha1.setConstant(True)
    alpha2.setConstant(True)
    n1.setConstant(True)
    n2.setConstant(True)

if cfg.graph == True:
    t.SetBranchStatus("*",0)
    t.SetBranchStatus("B_M", 1)

    print time.asctime(time.localtime()), "Making Data Set..."

    ds = ROOT.RooDataSet("ds", "", t, ROOT.RooArgSet(var))
    ds.Print()

    print time.asctime(time.localtime()), "Fitting..."

    c=ROOT.TCanvas()
    frame = var.frame()
    ds.plotOn(frame)

    if cfg.source == "data":
        r = fullModel.fitTo(ds, ROOT.RooFit.Save(True), ROOT.RooFit.NumCPU(8))
        r.Print("v")
        print "plotting data"
        fullModel.plotOn(frame)
        fullModel.plotOn(frame, ROOT.RooFit.Components("sigModel"), ROOT.RooFit.LineColor(ROOT.kRed))
        fullModel.plotOn(frame, ROOT.RooFit.Components("exp"), ROOT.RooFit.LineColor(ROOT.kGreen))
    
    if cfg.source == "sim":
        r = sigModel.fitTo(ds, ROOT.RooFit.Save(True), ROOT.RooFit.NumCPU(8))
        r.Print("v")
        sigModel.plotOn(frame)
        sigModel.plotOn(frame, ROOT.RooFit.Components("cb1"), ROOT.RooFit.LineColor(ROOT.kGreen))
        sigModel.plotOn(frame, ROOT.RooFit.Components("cb2"), ROOT.RooFit.LineColor(ROOT.kRed))
        
    print time.asctime(time.localtime()), "Plotting data"
    frame.Draw()
    c.Print("Bmassfit.pdf(")
    frame.Draw()
    c.Print("Bmassfit.pdf)")
    raw_input("prompt")
    
if cfg.cut == True:
    selection = "(B_M <" + str(lowercut) +" || B_M >" + str(uppercut) + ")"

    print time.asctime(time.localtime()), "writing a tree"

    f = ROOT.TFile(filename, "READ")
    t = f.Get(tree)
    g = ROOT.TFile(filename[:filename.find(".root")] + "_nosignal.root", "recreate")

    tcount = t.GetEntriesFast()
    print time.asctime(time.localtime()), "Contains", tcount, "entries"
    print time.asctime(time.localtime()), "Contains", t.GetEntries(selection), "entries to be copied"

    print time.asctime(time.localtime()), "Cloning Tree..."
    nt=t.CopyTree(selection)

    print time.asctime(time.localtime()), "Tree Cloned!"

    g.Close()

    print time.asctime(time.localtime()), "Branch Filled!"
    
if cfg.interpolate == True:
    
    tree = "DecayTree"
    filename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource + "_nosignal.root"
    f = ROOT.TFile(filename)
    t = f.Get(tree)
    t.SetBranchStatus("*",0)
    t.SetBranchStatus("B_M", 1)

    var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}e^{-})",int(cfg.mlower), int(cfg.mupper))

    print time.asctime(time.localtime()), "Making Data Set..."

    ds = ROOT.RooDataSet("ds", "", t, ROOT.RooArgSet(var))
    ds.Print()

    print time.asctime(time.localtime()), "Fitting..."

    bincount = 100    
    mean = ROOT.RooRealVar("mean", "", 5285, int(cfg.mlower), int(cfg.mupper))

    sigma1 = ROOT.RooRealVar("sigma1", "", 18.6, 0, 50)
    alpha1 = ROOT.RooRealVar("alpha1", "", -2.11)
    n1 = ROOT.RooRealVar("n1", "", 2.83)

    sigma2 = ROOT.RooRealVar("sigma2", "", 8.4, 0, 40)
    alpha2 = ROOT.RooRealVar("alpha2", "", 0.375)
    n2 = ROOT.RooRealVar("n2", "", 31.5)

    a = ROOT.RooRealVar("a", "", -0.0017, -1., 1.)
         
    frac = ROOT.RooRealVar("frac", "", 0.5, 0, 1)

    cb1 = ROOT.RooCBShape("cb1","", var, mean, sigma1, alpha1, n1)
    cb2 = ROOT.RooCBShape("cb2","", var, mean, sigma2, alpha2, n2)
    exp = ROOT.RooExponential("exp", "", var, a)
    sigModel = ROOT.RooAddPdf ("sigModel", "", ROOT.RooArgList(cb1, cb2), ROOT.RooArgList(frac))

    signalYield = ROOT.RooRealVar("signalYield", "", 1530000, 0, 2400000)
    combinatorialYield = ROOT.RooRealVar("combinatorialYield", "", 870000, 0, 2400000)

    fullModel = ROOT.RooAddPdf("fullmodel", "", ROOT.RooArgList(sigModel, exp), ROOT.RooArgList(signalYield, combinatorialYield))

    c=ROOT.TCanvas()
    frame = var.frame()
    ds.plotOn(frame)
    
    var.setRange("R1", cfg.mlower, lowercut)
    var.setRange("R2", uppercut, cfg.mupper)

    r = fullModel.fitTo(ds, ROOT.RooFit.Range("R1,R2"), ROOT.RooFit.Save(True), ROOT.RooFit.NumCPU(8))
    r.Print("v")
    fullModel.plotOn(frame)
    fullModel.plotOn(frame, ROOT.RooFit.Components("sigModel"), ROOT.RooFit.LineColor(ROOT.kRed))
    fullModel.plotOn(frame, ROOT.RooFit.Components("exp"), ROOT.RooFit.LineColor(ROOT.kGreen))

    print time.asctime(time.localtime()), "Plotting data"
    frame.Draw()
    c.Print("cutBmassfit.pdf(")
    frame.Draw()
    c.Print("cutBmassfit.pdf)")
    raw_input("prompt")