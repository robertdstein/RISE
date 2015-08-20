import ROOT
import argparse

selection = "(eminus_P == 40883.7469362)"
filename = "/net/storage03/data/users/dberninghoff/B2Kll/Merged/MC_Bplus_Kplusmue.root"
treename = "Bu2LLK_meLine_TupleMC/DecayTree"

f = ROOT.TFile(filename, "READ")
t = f.Get(treename)

tcount = t.GetEntriesFast()
print "Contains", tcount, "entries"
print "Contains", t.GetEntries(selection), "entries matching selection"