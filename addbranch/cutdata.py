import ROOT
import argparse

parser = argparse.ArgumentParser(description='Cut Data')
parser.add_argument("-s", "--sim", action="store_true")
cfg = parser.parse_args()

selection = "(B_M < 7000) && (Kplus_isMuonLoose == 0) && (Kplus_InAccMuon == 1) && (muplus_ProbNNghost<0.3) && (eminus_ProbNNghost<0.3) && (Kplus_ProbNNghost < 0.3) && (eminus_ProbNNe > 0.05) && (Kplus_ProbNNk > 0.05) && (muplus_ProbNNmu > 0.05) && (Psi_M < 3000 || Psi_M >3200)"
filename = "/net/storage03/data/users/rstein/tuples/raw/B2Kmue_Data_MergedminPtBranch.root"
treename = "DecayTree"

if cfg.sim == True:
    selection += "(B_BKGCAT == 0)"
    filename = "/net/storage03/data/users/rstein/tuples/raw/B2Kemu_Data_MergedminPTbranch.root"
    treename = "DecayTree"


print "writing a tree"

f = ROOT.TFile(filename, "READ")
t = f.Get(treename)
g = ROOT.TFile(filename[:filename.find(".root")] + "_cut.root", "recreate")

tcount = t.GetEntriesFast()
print "Contains", tcount, "entries"
print "Contains", t.GetEntries(selection), "entries to be copied"


print "Cloning Tree..."
nt=t.CopyTree(selection)

print "Tree Cloned!"

g.Close()

print "Branch Filled!"