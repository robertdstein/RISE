import argparse, ROOT, time
import lhcbStyle as lhcb
import array

start = time.time()
print time.asctime(time.localtime())

parser = argparse.ArgumentParser(description='Fit for B_M from dataset')
parser.add_argument('-s', '--source', type=str,  choices=['data', 'sim'], default="data")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-l", "--mlower", default=5175)
parser.add_argument("-u", "--mupper", default=5475)

cfg = parser.parse_args()

if not cfg.debug:
	print "supressing fit output"
	ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
	ROOT.RooMsgService.instance().setSilentMode(True)

lhcb.setLHCbStyle()

if cfg.source == "data":
    datasource = "DATA_Bplus_Kplusmumu_qsq.root"

if cfg.source == "sim":
    datasource = "MC_Bplus_KplusJpsimumu_qsqcut.root"
    
tree = "DecayTree"
filename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource
f = ROOT.TFile(filename)
t = f.Get(tree)
t.SetBranchStatus("*",0)
t.SetBranchStatus("B_M", 1)

var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}#mu^{-})",int(cfg.mlower), int(cfg.mupper))

print "Making Data Set..."

ds = ROOT.RooDataSet("ds", "", t, ROOT.RooArgSet(var))
ds.Print()

print "Fitting..."

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
    frame.Draw()
    raw_input("prompt")

if cfg.graph:
    print "Plotting data"
    frame.Draw()
    c.Print("Bmassfit.pdf(")
    c.SetLogy()
    frame.Draw()
    c.Print("Bmassfit.pdf)")
    raw_input("prompt")

sigma1.setConstant(True)
sigma2.setConstant(True)
alpha1.setConstant(True)
alpha2.setConstant(True)
n1.setConstant(True)
a.setConstant(True)
frac.setConstant(True)
   
print "Making S Weights..."

if cfg.source == "data":
    sData = ROOT.RooStats.SPlot("sData","An SPlot", ds, fullModel, ROOT.RooArgList(signalYield, combinatorialYield))

if cfg.source == "sim":
    sData = ROOT.RooStats.SPlot("sData","An SPlot", ds, sigModel, ROOT.RooArgList(frac))

sData.Print("V")
sData.GetYieldFromSWeight("signalYield")
sData.GetYieldFromSWeight("combinatorialYield")

print "writing a tree"

g = ROOT.TFile(filename[:filename.find(".root")] + "_sweight.root", "recreate")
tcount = t.GetEntriesFast()
print "Contains", tcount, "entries"

print "Cloning Tree..."
t.SetBranchStatus("*",1)
nt=t.CloneTree(-1, "fast")
print "Tree Cloned!"

res_tuple = {}
j=0
o = (array.array('f',[0]))
brBranch = nt.Branch('sweight', o, 'sweight/F')

print "Filling S-Weight Branch"

for i in range(0, tcount):
    nt.GetEntry(i)
    x = nt.B_M
    o[0] = 0
    if (x > cfg.mlower and x < cfg.mupper):
        o[0] = sData.GetSWeight(j, "signalYield")
        j+=1
    brBranch.Fill()
        
print "Optimising"    
nt.OptimizeBaskets()
print "Writing"
nt.Write("",ROOT.TObject.kOverwrite)

print "closing", g, f
g.Close() 
f.Close()
 
end = time.time()
print time.asctime(time.localtime())
print "time taken", end-start