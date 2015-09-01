import sys, ROOT, os, math, time
import array

tuplePath = "/net/storage03/data/users/rstein/tuples/qsq/"
tupleName = "MC_Bplus_Kplusmue_BDT_eta"
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

nFileName = "/net/storage03/data/users/rstein/tuples/qsq/" + tupleName+ "_newProbNN.root"
print('saving File to ' + nFileName)

nf = ROOT.TFile(nFileName, "RECREATE")
print "cloning tree..."
nt = t.CloneTree(-1, 'fast')

nt.SetBranchStatus("*", 0)
nt.SetBranchStatus("Kplus_ProbNNk", 1)
nt.SetBranchStatus("eminus_ProbNNe", 1)
nt.SetBranchStatus("muplus_ProbNNmu", 1)

Kplus_newProbNNk = (array.array('d',[0]))
Kplus_newProbNNkBranch = nt.Branch("Kplus_newProbNNk", Kplus_newProbNNk, "Kplus_newProbNNk/D")

Kplus_ProbNNk = (array.array('d',[0]))
Kplus_ProbNNkBranch = nt.GetBranch("Kplus_ProbNNk")
Kplus_ProbNNkBranch.SetAddress(Kplus_ProbNNk)

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
    Kplus_ProbNNkBranch.GetEntry(i)
    kval = Kplus_ProbNNk[0]/(1-Kplus_ProbNNk[0])
    if Kplus_ProbNNk[0] > 0.0:
        Kplus_newProbNNk[0] = math.log(kval)
    else:
        Kplus_newProbNNk[0] = -1000
    Kplus_newProbNNkBranch.Fill()
    
    muplus_ProbNNmuBranch.GetEntry(i)
    muval = muplus_ProbNNmu[0]/(1-muplus_ProbNNmu[0])
    if muplus_ProbNNmu[0] > 0.0:
        muplus_newProbNNmu[0] = math.log(muval)
    else:
        muplus_newProbNNmu[0] = -1000
    muplus_newProbNNmuBranch.Fill()
    
    eminus_ProbNNeBranch.GetEntry(i)
    eminusval = eminus_ProbNNe[0]/(1-eminus_ProbNNe[0])
    if eminus_ProbNNe[0] > 0.0:
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