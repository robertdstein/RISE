import sys, ROOT, os
import array

tuplePath = "/net/storage03/data/users/dberninghoff/B2Kll/Merged/"
tupleName = "DATA_Bplus_Kplusmumu" 
fullName = tuplePath + tupleName + ".root"
treeName = "Bu2LLK_mmLine_TupleMDST/DecayTree"

f = ROOT.TFile(fullName, "READ")

if not f.IsOpen() :
    print("file " + fullName + " not found")
    exit()

t = f.Get(treeName)

if not t :
    print("tree " + treeName + " not found")
    exit()

nFileName = "/net/storage03/data/users/rstein/tuples/qsq/" + tupleName+ "_qsq.root"
print('saving File to ' + nFileName)

nf = ROOT.TFile(nFileName, "RECREATE")
print "cloning tree..."
nt = t.CloneTree(-1, 'fast')

nt.SetBranchStatus("*", 0)
nt.SetBranchStatus("Psi_M", 1)

qsq = (array.array('d',[0]))
qsqBranch = nt.Branch("qsq", qsq, "qsq/D")

Psi_M = (array.array('d',[0]))
Psi_MBranch = nt.GetBranch("Psi_M")
Psi_MBranch.SetAddress(Psi_M)

print "itterating over", nt.GetEntries() , "events"
for i in range(nt.GetEntries()):
    Psi_MBranch.GetEntry(i)
    qsq[0] = Psi_M[0] * Psi_M[0] * 0.000001
    qsqBranch.Fill()

nt.SetBranchStatus("*", 1)
nt.Write("DecayTree")
nf.Close()
