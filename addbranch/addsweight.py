import argparse, ROOT, time
import array

start = time.time()
print time.asctime(time.localtime()), "Code Started"

parser = argparse.ArgumentParser(description='Fit for B_M from dataset')
parser.add_argument('-s', '--source', default="DATA_Bplus_Kplusmumu_qsq")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-l", "--mlower", default=5175)
parser.add_argument("-u", "--mupper", default=5475)

cfg = parser.parse_args()

if not cfg.debug:
	print time.asctime(time.localtime()), "Supressing Fit Output"
	ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
	ROOT.RooMsgService.instance().setSilentMode(True)

datasource = cfg.source + ".root"
    
tree = "DecayTree"
filename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource
f = ROOT.TFile(filename)
t = f.Get(tree)
t.SetBranchStatus("*",0)
t.SetBranchStatus("B_M", 1)

var = ROOT.RooRealVar("B_M", "m(K^{+}#mu^{+}#mu^{-})",int(cfg.mlower), int(cfg.mupper))

print time.asctime(time.localtime()),"Making Data Set..."

ds = ROOT.RooDataSet("ds", "", t, ROOT.RooArgSet(var))
ds.Print()

print time.asctime(time.localtime()),"Fitting..."

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

r = fullModel.fitTo(ds, ROOT.RooFit.Save(True), ROOT.RooFit.NumCPU(8))
r.Print("v")
print time.asctime(time.localtime()), "Plotting data"
fullModel.plotOn(frame)
fullModel.plotOn(frame, ROOT.RooFit.Components("sigModel"), ROOT.RooFit.LineColor(ROOT.kRed))
fullModel.plotOn(frame, ROOT.RooFit.Components("exp"), ROOT.RooFit.LineColor(ROOT.kGreen))

sigma1.setConstant(True)
sigma2.setConstant(True)
alpha1.setConstant(True)
alpha2.setConstant(True)
n1.setConstant(True)
a.setConstant(True)
frac.setConstant(True)
   
print time.asctime(time.localtime()), "Making S Weights..."

sData = ROOT.RooStats.SPlot("sData","An SPlot", ds, fullModel, ROOT.RooArgList(signalYield, combinatorialYield))

sData.Print("V")
sData.GetYieldFromSWeight("signalYield")
sData.GetYieldFromSWeight("combinatorialYield")

print time.asctime(time.localtime()), "Writing a Tree"

g = ROOT.TFile(filename[:filename.find(".root")] + "_sweight.root", "recreate")
tcount = t.GetEntriesFast()
print time.asctime(time.localtime()),"Contains", tcount, "entries"

print time.asctime(time.localtime()),"Cloning Tree..."
t.SetBranchStatus("*",1)
nt=t.CloneTree(-1, "fast")
print time.asctime(time.localtime()),"Tree Cloned!"

res_tuple = {}
j=0
o = (array.array('f',[0]))
brBranch = nt.Branch('sweight', o, 'sweight/F')

print time.asctime(time.localtime()),"Filling S-Weight Branch"

for i in range(0, tcount):
    nt.GetEntry(i)
    x = nt.B_M
    o[0] = 0
    if (x > cfg.mlower and x < cfg.mupper):
        o[0] = sData.GetSWeight(j, "signalYield")
        j+=1
    brBranch.Fill()
        
print time.asctime(time.localtime()),"Optimising"    
nt.OptimizeBaskets()
print time.asctime(time.localtime()),"Writing"
nt.Write("",ROOT.TObject.kOverwrite)

print time.asctime(time.localtime()),"Closing", g, f
g.Close() 
f.Close()
 
end = time.time()
print "Code completed", time.asctime(time.localtime())
print "time taken", end-start