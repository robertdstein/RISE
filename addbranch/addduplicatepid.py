import sys, ROOT, math, time
import array

#Clones ProbNN branches with pid-resamplimg naming conventions, to allow merged datasets 

tuplePath = "/net/storage03/data/users/rstein/tuples/qsq/"
tupleName = "DATA_Bplus_Kplusmue_BDTcut"
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

nFileName = "/net/storage03/data/users/rstein/tuples/qsq/" + tupleName+ "_duplicatedpid.root"
print('saving File to ' + nFileName)

nf = ROOT.TFile(nFileName, "RECREATE")
print "cloning tree..."
nt = t.CloneTree(-1, 'fast')

nt.SetBranchStatus("*", 0)
nt.SetBranchStatus("Kplus_ProbNNk", 1)
nt.SetBranchStatus("eminus_ProbNNe", 1)
nt.SetBranchStatus("muplus_ProbNNmu", 1)

Kplus_PIDk_corrected = (array.array('d',[0]))
Kplus_PIDk_correctedBranch = nt.Branch("Kplus_PIDk_corrected", Kplus_PIDk_corrected, "Kplus_PIDk_corrected/D")

Kplus_ProbNNk = (array.array('d',[0]))
Kplus_ProbNNkBranch = nt.GetBranch("Kplus_ProbNNk")
Kplus_ProbNNkBranch.SetAddress(Kplus_ProbNNk)

muplus_PIDmu_corrected = (array.array('d',[0]))
muplus_PIDmu_correctedBranch = nt.Branch("muplus_PIDmu_corrected", muplus_PIDmu_corrected, "muplus_PIDmu_corrected/D")

muplus_ProbNNmu = (array.array('d',[0]))
muplus_ProbNNmuBranch = nt.GetBranch("muplus_ProbNNmu")
muplus_ProbNNmuBranch.SetAddress(muplus_ProbNNmu)


eminus_PIDe_corrected = (array.array('d',[0]))
eminus_PIDe_correctedBranch = nt.Branch("eminus_PIDe_corrected", eminus_PIDe_corrected, "eminus_PIDe_corrected/D")

eminus_ProbNNe = (array.array('d',[0]))
eminus_ProbNNeBranch = nt.GetBranch("eminus_ProbNNe")
eminus_ProbNNeBranch.SetAddress(eminus_ProbNNe)


print "itterating over", nt.GetEntries() , "events"
for i in range(nt.GetEntries()):
    Kplus_ProbNNkBranch.GetEntry(i)
    Kplus_PIDk_corrected[0] = Kplus_ProbNNk[0]
    Kplus_PIDk_correctedBranch.Fill()
    muplus_ProbNNmuBranch.GetEntry(i)
    muplus_PIDmu_corrected[0] = muplus_ProbNNmu[0]
    muplus_PIDmu_correctedBranch.Fill()
    eminus_ProbNNeBranch.GetEntry(i)
    eminus_PIDe_corrected[0] = eminus_ProbNNe[0]
    eminus_PIDe_correctedBranch.Fill()

nt.SetBranchStatus("*", 1)
nt.Write("DecayTree")
nf.Close()

message = str(time.asctime(time.localtime())) + " Created new tree at /net/storage03/data/users/rstein/tuples/qsq/" + tupleName+ "_duplicatedpid.root"
print message

import os, sys
sys.path.append('/home/rstein/pythonscripts/misc')
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message)