import sys, ROOT, os, math
import array

tuplePath = "/net/storage03/data/users/rstein/tuples/qsq/"
tupleName = "MC_Bplus_Kplusmue_BDT"
treeName = "DecayTree"

fullName = tuplePath + tupleName + ".root"

f = ROOT.TFile(fullName, "READ")

if not f.IsOpen() :
    print("file " + fullName + " not found")
    exit()

t = f.Get(treeName)

if not t :
    print("tree " + treeName + " not found")
    exit()

nFileName = "/net/storage03/data/users/rstein/tuples/qsq/" + tupleName+ "_eta.root"
print('saving File to ' + nFileName)

nf = ROOT.TFile(nFileName, "RECREATE")
print "cloning tree..."
nt = t.CloneTree(-1, 'fast')

nt.SetBranchStatus("*", 0)
nt.SetBranchStatus("Kplus_ProbNNK", 1)
nt.SetBranchStatus("eminus_ProbNNe", 1)
nt.SetBranchStatus("muplus_ProbNNmu", 1)

Kplus_newProbNNK = (array.array('d',[0]))
Kplus_newProbNNKBranch = nt.Branch("Kplus_newProbNNK", Kplus_newProbNNK, "Kplus_newProbNNK/D")

Kplus_ProbNNK = (array.array('d',[0]))
Kplus_ProbNNKBranch = nt.GetBranch("Kplus_ProbNNK")
Kplus_ProbNNKBranch.SetAddress(Kplus_ProbNNK)

muplus_newProbNNmu = (array.array('d',[0]))
muplus_newProbNNmuBranch = nt.Branch("muplus_newProbNNmu", muplus_newProbNNmu, "muplus_newProbNNmu/D")

muplus_ProbNNmu = (array.array('d',[0]))
muplus_ProbNNmuBranch = nt.GetBranch("muplus_ProbNNmu")
muplus_ProbNNmuBranch.SetAddress(muplus_ProbNNmu)

eminus_newProbNNe = (array.array('d',[0]))
eminus_newProbNNeBranch = nt.Branch("eminus_newProbNNe", eminus_newProbNNe, "eminus_newProbNNe/D")

eminus_ProbNNe = (array.array('d',[0]))
eminus_ProbNNeBranch = nt.GetBranch("eminus_ProbNNe")
eminus_ProbNNeBranch.SetAddress(eminus_ProbNNe)

print "itterating over", nt.GetEntries() , "events"
for i in range(nt.GetEntries()):
    Kplus_ProbNNKBranch.GetEntry(i)
    Kplus_newProbNNK[0] = math.log(Kplus_ProbNNK[0]/(1-Kplus_ProbNNK[0]))
    Kplus_newProbNNKBranch.Fill()
    
    muplus_ProbNNmuBranch.GetEntry(i)
    muplus_newProbNNmu[0] = math.log(muplus_ProbNNmu[0]/(1-muplus_ProbNNmu[0]))
    muplus_newProbNNmuBranch.Fill()
    
    eminus_ProbNNeBranch.GetEntry(i)
    eminus_newProbNNe[0] = math.log(eminus_ProbNNe[0]/(1-eminus_ProbNNe[0]))
    eminus_newProbNNeBranch.Fill()

nt.SetBranchStatus("*", 1)
nt.Write("DecayTree")
nf.Close()