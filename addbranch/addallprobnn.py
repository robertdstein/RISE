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
nt.SetBranchStatus("eminus_ProbNNk", 1)
nt.SetBranchStatus("muplus_ProbNNk", 1)

Kplus_newProbNNk = (array.array('d',[0]))
Kplus_newProbNNkBranch = nt.Branch("Kplus_newProbNNk", Kplus_newProbNNk, "Kplus_newProbNNk/D")

Kplus_ProbNNk = (array.array('d',[0]))
Kplus_ProbNNkBranch = nt.GetBranch("Kplus_ProbNNk")
Kplus_ProbNNkBranch.SetAddress(Kplus_ProbNNk)

muplus_newProbNNk = (array.array('d',[0]))
muplus_newProbNNkBranch = nt.Branch("muplus_newProbNNk", muplus_newProbNNk, "muplus_newProbNNk/D")

muplus_ProbNNk = (array.array('d',[0]))
muplus_ProbNNkBranch = nt.GetBranch("muplus_ProbNNk")
muplus_ProbNNkBranch.SetAddress(muplus_ProbNNk)

eminus_newProbNNk = (array.array('d',[0]))
eminus_newProbNNkBranch = nt.Branch("eminus_newProbNNk", eminus_newProbNNk, "eminus_newProbNNk/D")

eminus_ProbNNk = (array.array('d',[0]))
eminus_ProbNNkBranch = nt.GetBranch("eminus_ProbNNk")
eminus_ProbNNkBranch.SetAddress(eminus_ProbNNk)

nt.SetBranchStatus("Kplus_ProbNNe", 1)
nt.SetBranchStatus("eminus_ProbNNe", 1)
nt.SetBranchStatus("muplus_ProbNNe", 1)

Kplus_newProbNNe = (array.array('d',[0]))
Kplus_newProbNNeBranch = nt.Branch("Kplus_newProbNNe", Kplus_newProbNNe, "Kplus_newProbNNe/D")

Kplus_ProbNNe = (array.array('d',[0]))
Kplus_ProbNNeBranch = nt.GetBranch("Kplus_ProbNNe")
Kplus_ProbNNeBranch.SetAddress(Kplus_ProbNNe)

muplus_newProbNNe = (array.array('d',[0]))
muplus_newProbNNeBranch = nt.Branch("muplus_newProbNNe", muplus_newProbNNe, "muplus_newProbNNe/D")

muplus_ProbNNe = (array.array('d',[0]))
muplus_ProbNNeBranch = nt.GetBranch("muplus_ProbNNe")
muplus_ProbNNeBranch.SetAddress(muplus_ProbNNe)

eminus_newProbNNe = (array.array('d',[0]))
eminus_newProbNNeBranch = nt.Branch("eminus_newProbNNe", eminus_newProbNNe, "eminus_newProbNNe/D")

eminus_ProbNNe = (array.array('d',[0]))
eminus_ProbNNeBranch = nt.GetBranch("eminus_ProbNNe")
eminus_ProbNNeBranch.SetAddress(eminus_ProbNNe)

nt.SetBranchStatus("Kplus_ProbNNmu", 1)
nt.SetBranchStatus("eminus_ProbNNmu", 1)
nt.SetBranchStatus("muplus_ProbNNmu", 1)

Kplus_newProbNNmu = (array.array('d',[0]))
Kplus_newProbNNmuBranch = nt.Branch("Kplus_newProbNNmu", Kplus_newProbNNmu, "Kplus_newProbNNmu/D")

Kplus_ProbNNmu = (array.array('d',[0]))
Kplus_ProbNNmuBranch = nt.GetBranch("Kplus_ProbNNmu")
Kplus_ProbNNmuBranch.SetAddress(Kplus_ProbNNmu)

muplus_newProbNNmu = (array.array('d',[0]))
muplus_newProbNNmuBranch = nt.Branch("muplus_newProbNNmu", muplus_newProbNNmu, "muplus_newProbNNmu/D")

muplus_ProbNNmu = (array.array('d',[0]))
muplus_ProbNNmuBranch = nt.GetBranch("muplus_ProbNNmu")
muplus_ProbNNmuBranch.SetAddress(muplus_ProbNNmu)

eminus_newProbNNmu = (array.array('d',[0]))
eminus_newProbNNmuBranch = nt.Branch("eminus_newProbNNmu", eminus_newProbNNmu, "eminus_newProbNNmu/D")

eminus_ProbNNmu = (array.array('d',[0]))
eminus_ProbNNmuBranch = nt.GetBranch("eminus_ProbNNmu")
eminus_ProbNNmuBranch.SetAddress(eminus_ProbNNmu)

print "itterating over", nt.GetEntries() , "events"
for i in range(nt.GetEntries()):
    Kplus_ProbNNkBranch.GetEntry(i)
    kval = Kplus_ProbNNk[0]/(1-Kplus_ProbNNk[0])
    if Kplus_ProbNNk[0] > 0.0:
        Kplus_newProbNNk[0] = math.log(kval)
    else:
        Kplus_newProbNNk[0] = -1000
    Kplus_newProbNNkBranch.Fill()
    
    muplus_ProbNNkBranch.GetEntry(i)
    muval = muplus_ProbNNk[0]/(1-muplus_ProbNNk[0])
    if muplus_ProbNNk[0] > 0.0:
        muplus_newProbNNk[0] = math.log(muval)
    else:
        muplus_newProbNNk[0] = -1000
    muplus_newProbNNkBranch.Fill()
    
    eminus_ProbNNkBranch.GetEntry(i)
    eminusval = eminus_ProbNNk[0]/(1-eminus_ProbNNk[0])
    if eminus_ProbNNk[0] > 0.0:
        eminus_newProbNNk[0] = math.log(eminusval)
    else:
        eminus_newProbNNk[0] = -1000
    eminus_newProbNNkBranch.Fill()
    
    Kplus_ProbNNeBranch.GetEntry(i)
    kval = Kplus_ProbNNe[0]/(1-Kplus_ProbNNe[0])
    if Kplus_ProbNNe[0] > 0.0:
        Kplus_newProbNNe[0] = math.log(kval)
    else:
        Kplus_newProbNNe[0] = -1000
    Kplus_newProbNNeBranch.Fill()
    
    muplus_ProbNNeBranch.GetEntry(i)
    muval = muplus_ProbNNe[0]/(1-muplus_ProbNNe[0])
    if muplus_ProbNNe[0] > 0.0:
        muplus_newProbNNe[0] = math.log(muval)
    else:
        muplus_newProbNNe[0] = -1000
    muplus_newProbNNeBranch.Fill()
    
    eminus_ProbNNeBranch.GetEntry(i)
    eminusval = eminus_ProbNNe[0]/(1-eminus_ProbNNe[0])
    if eminus_ProbNNe[0] > 0.0:
        eminus_newProbNNe[0] = math.log(eminusval)
    else:
        eminus_newProbNNe[0] = -1000
    eminus_newProbNNeBranch.Fill()
    
    Kplus_ProbNNmuBranch.GetEntry(i)
    kval = Kplus_ProbNNmu[0]/(1-Kplus_ProbNNmu[0])
    if Kplus_ProbNNmu[0] > 0.0:
        Kplus_newProbNNmu[0] = math.log(kval)
    else:
        Kplus_newProbNNmu[0] = -1000
    Kplus_newProbNNmuBranch.Fill()
    
    muplus_ProbNNmuBranch.GetEntry(i)
    muval = muplus_ProbNNmu[0]/(1-muplus_ProbNNmu[0])
    if muplus_ProbNNmu[0] > 0.0:
        muplus_newProbNNmu[0] = math.log(muval)
    else:
        muplus_newProbNNmu[0] = -1000
    muplus_newProbNNmuBranch.Fill()
    
    eminus_ProbNNmuBranch.GetEntry(i)
    eminusval = eminus_ProbNNmu[0]/(1-eminus_ProbNNmu[0])
    if eminus_ProbNNmu[0] > 0.0:
        eminus_newProbNNmu[0] = math.log(eminusval)
    else:
        eminus_newProbNNmu[0] = -1000
    eminus_newProbNNmuBranch.Fill()

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