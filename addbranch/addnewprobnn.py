import sys, ROOT, os, math, time
import array

tuplePath = "/net/storage03/data/users/rstein/tuples/qsq/"
tupleName = "MC_Bplus_Kplusmue_resampled"
treeName = "default"

fullName = tuplePath + tupleName + ".root"

f = ROOT.TFile(fullName, "READ")

if not f.IsOpen() :
    print("file " + fullName + " not found")
    exit()

t = f.Get(treeName)

if not t :
    print("tree " + treeName + " not found")
    exit()

nFileName = "/net/storage03/data/users/rstein/tuples/qsq/" + tupleName+ "_newProbNN.root"
print('saving File to ' + nFileName)

nf = ROOT.TFile(nFileName, "RECREATE")
print "cloning tree..."
nt = t.CloneTree(-1, 'fast')

nt.SetBranchStatus("*", 0)
nt.SetBranchStatus("Kplus_PIDK_corrected", 1)
nt.SetBranchStatus("eminus_PIDe_corrected", 1)
nt.SetBranchStatus("muplus_PIDmu_corrected", 1)

Kplus_newProbNNk = (array.array('d',[0]))
Kplus_newProbNNkBranch = nt.Branch("Kplus_newProbNNk", Kplus_newProbNNk, "Kplus_newProbNNk/D")

Kplus_PIDK_corrected = (array.array('d',[0]))
Kplus_PIDK_correctedBranch = nt.GetBranch("Kplus_PIDK_corrected")
Kplus_PIDK_correctedBranch.SetAddress(Kplus_PIDK_corrected)

muplus_newProbNNmu = (array.array('d',[0]))
muplus_newProbNNmuBranch = nt.Branch("muplus_newProbNNmu", muplus_newProbNNmu, "muplus_newProbNNmu/D")

muplus_PIDmu_corrected = (array.array('d',[0]))
muplus_PIDmu_correctedBranch = nt.GetBranch("muplus_PIDmu_corrected")
muplus_PIDmu_correctedBranch.SetAddress(muplus_PIDmu_corrected)

eminus_newProbNNe = (array.array('d',[0]))
eminus_newProbNNeBranch = nt.Branch("eminus_newProbNNe", eminus_newProbNNe, "eminus_newProbNNe/D")

eminus_PIDe_corrected = (array.array('d',[0]))
eminus_PIDe_correctedBranch = nt.GetBranch("eminus_PIDe_corrected")
eminus_PIDe_correctedBranch.SetAddress(eminus_PIDe_corrected)

print "itterating over", nt.GetEntries() , "events"
for i in range(nt.GetEntries()):
    Kplus_PIDK_correctedBranch.GetEntry(i)
    kval = Kplus_PIDK_corrected[0]/(1-Kplus_PIDK_corrected[0])
    if Kplus_PIDK_corrected[0] > 0.0:
        Kplus_newProbNNk[0] = math.log(kval)
    else:
        Kplus_newProbNNk[0] = -1000
    Kplus_newProbNNkBranch.Fill()
    
    muplus_PIDmu_correctedBranch.GetEntry(i)
    muval = muplus_PIDmu_corrected[0]/(1-muplus_PIDmu_corrected[0])
    if muplus_PIDmu_corrected[0] > 0.0:
        muplus_newProbNNmu[0] = math.log(muval)
    else:
        muplus_newProbNNmu[0] = -1000
    muplus_newProbNNmuBranch.Fill()
    
    eminus_PIDe_correctedBranch.GetEntry(i)
    eminusval = eminus_PIDe_corrected[0]/(1-eminus_PIDe_corrected[0])
    if eminus_PIDe_corrected[0] > 0.0:
        eminus_newProbNNe[0] = math.log(eminusval)
    else:
        eminus_newProbNNe[0] = -1000
    eminus_newProbNNeBranch.Fill()

nt.SetBranchStatus("*", 1)
nt.Write("DecayTree")
nf.Close()

message = str(time.asctime(time.localtime())) + " Created new tree at /net/storage03/data/users/rstein/tuples/qsq/" + tupleName+ "_newProbNN.root"
print message

import os, sys
sys.path.append('/home/rstein/pythonscripts/misc')
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message)