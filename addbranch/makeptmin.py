import ROOT
import array

#Add a branch with the minimum transverse momentum

filename = "/net/storage03/data/users/rstein/tuples/raw/B2Kmue_MC_Merged.root"
treename = "Bu2LLK_meLine/DecayTree"
print "writing a tree"

f = ROOT.TFile(filename, "READ")
t = f.Get(treename)
g = ROOT.TFile(filename[:filename.find(".root")] + "_minPtBranch.root", "recreate")

tcount = t.GetEntriesFast()
print "Contains", tcount, "entries"

print "Cloning Tree..."
nt=t.CloneTree(-1, "fast")

nt.SetBranchStatus("*",0)
nt.SetBranchStatus("eminus_PT", 1)
nt.SetBranchStatus("muplus_PT", 1)

o = (array.array('f',[0]))
brBranch = nt.Branch('PT_Min', o, 'PT_Min/F')

muon = (array.array('d',[0]))
muonBranch = nt.GetBranch("muplus_PT")
muonBranch.SetAddress(muon)

electron = (array.array('d',[0]))
electronBranch = nt.GetBranch("eminus_PT")
electronBranch.SetAddress(electron)

print "Tree Cloned!"

#Fills the branch with the smaller of the electron and muon PT

print "Filling Branch..."

for i in xrange(tcount):
    nt.GetEntry(i)
    if electron[0] < muon[0]:
        o[0] = electron[0]
    else:
        o[0] = muon[0]
    brBranch.Fill()

nt.SetBranchStatus("*", 1)
nt.Write()
g.Close()

print "Branch Filled!"