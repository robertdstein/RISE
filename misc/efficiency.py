import argparse, ROOT, time
import lhcbStyle as lhcb
import array
from uncertainties import ufloat
import math

start = time.time()
print time.asctime(time.localtime()), "Calculating Efficiency"

ROOT.gROOT.SetBatch(ROOT.kTRUE)
c=ROOT.TCanvas()

datasource = "DATA_Bplus_Kplusmumu_qsq_sweight"

cutsource = "DATA_Bplus_Kplusmumu_qsqcut_sweight"
    
tree = "DecayTree"
prefilename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource + ".root"
f = ROOT.TFile(prefilename)
t = f.Get(tree)

postfilename = "/net/storage03/data/users/rstein/tuples/qsq/" + cutsource + ".root"
g = ROOT.TFile(postfilename)
u = g.Get(tree)

t.SetBranchStatus("*",0)
t.SetBranchStatus("sweight", 1)
u.SetBranchStatus("*",0)
u.SetBranchStatus("sweight", 1)

PreData = ROOT.TH1D("PreData", "", 100, -5, 5)
PostData= ROOT.TH1D("PostData", "", 100, -5, 5)

t.Draw("sweight>>PreData")
u.Draw("sweight>>PostData")

tcount = t.GetEntriesFast()
ucount = u.GetEntriesFast()

preweight = PreData.GetMean()*tcount
postweight = PostData.GetMean()*ucount

eff = float(postweight/preweight)
err = math.sqrt((eff) * (1-eff))/math.sqrt(tcount)
efficiency = ufloat(eff, err)

print "Sum of weights before is ", preweight
print "Sum of weights after is", postweight
print "Efficiency is", efficiency