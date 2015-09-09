import sys, ROOT, os, math, time
import array

tuplePath = "/net/storage03/data/users/rstein/tuples/qsq/"
tupleName = "DATA_Bplus_Kplusmumu_qsq_sweight"
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

nt.SetBranchStatus("Kplus_ProbNNmu", 1)

Kplus_newProbNNmu = (array.array('d',[0]))
Kplus_newProbNNmuBranch = nt.Branch("Kplus_newProbNNmu", Kplus_newProbNNmu, "Kplus_newProbNNmu/D")

Kplus_ProbNNmu = (array.array('d',[0]))
Kplus_ProbNNmuBranch = nt.GetBranch("Kplus_ProbNNmu")
Kplus_ProbNNmuBranch.SetAddress(Kplus_ProbNNmu)

nt.SetBranchStatus("Kplus_ProbNNe", 1)

Kplus_newProbNNe = (array.array('d',[0]))
Kplus_newProbNNeBranch = nt.Branch("Kplus_newProbNNe", Kplus_newProbNNe, "Kplus_newProbNNe/D")

Kplus_ProbNNe = (array.array('d',[0]))
Kplus_ProbNNeBranch = nt.GetBranch("Kplus_ProbNNe")
Kplus_ProbNNeBranch.SetAddress(Kplus_ProbNNe)

nt.SetBranchStatus("Kplus_ProbNNk", 1)

Kplus_newProbNNk = (array.array('d',[0]))
Kplus_newProbNNkBranch = nt.Branch("Kplus_newProbNNk", Kplus_newProbNNk, "Kplus_newProbNNk/D")

Kplus_ProbNNk = (array.array('d',[0]))
Kplus_ProbNNkBranch = nt.GetBranch("Kplus_ProbNNk")
Kplus_ProbNNkBranch.SetAddress(Kplus_ProbNNk)

nt.SetBranchStatus("muplus_ProbNNmu", 1)

muplus_newProbNNmu = (array.array('d',[0]))
muplus_newProbNNmuBranch = nt.Branch("muplus_newProbNNmu", muplus_newProbNNmu, "muplus_newProbNNmu/D")

muplus_ProbNNmu = (array.array('d',[0]))
muplus_ProbNNmuBranch = nt.GetBranch("muplus_ProbNNmu")
muplus_ProbNNmuBranch.SetAddress(muplus_ProbNNmu)

nt.SetBranchStatus("muplus_ProbNNe", 1)

muplus_newProbNNe = (array.array('d',[0]))
muplus_newProbNNeBranch = nt.Branch("muplus_newProbNNe", muplus_newProbNNe, "muplus_newProbNNe/D")

muplus_ProbNNe = (array.array('d',[0]))
muplus_ProbNNeBranch = nt.GetBranch("muplus_ProbNNe")
muplus_ProbNNeBranch.SetAddress(muplus_ProbNNe)

nt.SetBranchStatus("muplus_ProbNNk", 1)

muplus_newProbNNk = (array.array('d',[0]))
muplus_newProbNNkBranch = nt.Branch("muplus_newProbNNk", muplus_newProbNNk, "muplus_newProbNNk/D")

muplus_ProbNNk = (array.array('d',[0]))
muplus_ProbNNkBranch = nt.GetBranch("muplus_ProbNNk")
muplus_ProbNNkBranch.SetAddress(muplus_ProbNNk)

nt.SetBranchStatus("muminus_ProbNNmu", 1)

muminus_newProbNNmu = (array.array('d',[0]))
muminus_newProbNNmuBranch = nt.Branch("muminus_newProbNNmu", muminus_newProbNNmu, "muminus_newProbNNmu/D")

muminus_ProbNNmu = (array.array('d',[0]))
muminus_ProbNNmuBranch = nt.GetBranch("muminus_ProbNNmu")
muminus_ProbNNmuBranch.SetAddress(muminus_ProbNNmu)

nt.SetBranchStatus("muminus_ProbNNe", 1)

muminus_newProbNNe = (array.array('d',[0]))
muminus_newProbNNeBranch = nt.Branch("muminus_newProbNNe", muminus_newProbNNe, "muminus_newProbNNe/D")

muminus_ProbNNe = (array.array('d',[0]))
muminus_ProbNNeBranch = nt.GetBranch("muminus_ProbNNe")
muminus_ProbNNeBranch.SetAddress(muminus_ProbNNe)

nt.SetBranchStatus("muminus_ProbNNk", 1)

muminus_newProbNNk = (array.array('d',[0]))
muminus_newProbNNkBranch = nt.Branch("muminus_newProbNNk", muminus_newProbNNk, "muminus_newProbNNk/D")

muminus_ProbNNk = (array.array('d',[0]))
muminus_ProbNNkBranch = nt.GetBranch("muminus_ProbNNk")
muminus_ProbNNkBranch.SetAddress(muminus_ProbNNk)


print "itterating over", nt.GetEntries() , "events"
for i in range(nt.GetEntries()):
    Kplus_ProbNNmuBranch.GetEntry(i)
    if Kplus_ProbNNmu[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = Kplus_ProbNNmu[0]/(1-Kplus_ProbNNmu[0])
    if Kplus_ProbNNmu[0] > 0.0:
        Kplus_newProbNNmu[0] = math.log(eminusval)
    else:
        Kplus_newProbNNmu[0] = -1000
    Kplus_newProbNNmuBranch.Fill()
    
    Kplus_ProbNNeBranch.GetEntry(i)
    if Kplus_ProbNNe[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = Kplus_ProbNNe[0]/(1-Kplus_ProbNNe[0])
    if Kplus_ProbNNe[0] > 0.0:
        Kplus_newProbNNe[0] = math.log(eminusval)
    else:
        Kplus_newProbNNe[0] = -1000
    Kplus_newProbNNeBranch.Fill()
    
    Kplus_ProbNNkBranch.GetEntry(i)
    if Kplus_ProbNNk[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = Kplus_ProbNNk[0]/(1-Kplus_ProbNNk[0])
    if Kplus_ProbNNk[0] > 0.0:
        Kplus_newProbNNk[0] = math.log(eminusval)
    else:
        Kplus_newProbNNk[0] = -1000
    Kplus_newProbNNkBranch.Fill()
    
    muplus_ProbNNmuBranch.GetEntry(i)
    if muplus_ProbNNmu[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = muplus_ProbNNmu[0]/(1-muplus_ProbNNmu[0])
    if muplus_ProbNNmu[0] > 0.0:
        muplus_newProbNNmu[0] = math.log(eminusval)
    else:
        muplus_newProbNNmu[0] = -1000
    muplus_newProbNNmuBranch.Fill()
    
    muplus_ProbNNeBranch.GetEntry(i)
    if muplus_ProbNNe[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = muplus_ProbNNe[0]/(1-muplus_ProbNNe[0])
    if muplus_ProbNNe[0] > 0.0:
        muplus_newProbNNe[0] = math.log(eminusval)
    else:
        muplus_newProbNNe[0] = -1000
    muplus_newProbNNeBranch.Fill()
    
    muplus_ProbNNkBranch.GetEntry(i)
    if muplus_ProbNNk[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = muplus_ProbNNk[0]/(1-muplus_ProbNNk[0])
    if muplus_ProbNNk[0] > 0.0:
        muplus_newProbNNk[0] = math.log(eminusval)
    else:
        muplus_newProbNNk[0] = -1000
    muplus_newProbNNkBranch.Fill()
    
    muminus_ProbNNmuBranch.GetEntry(i)
    if muminus_ProbNNmu[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = muminus_ProbNNmu[0]/(1-muminus_ProbNNmu[0])
    if muminus_ProbNNmu[0] > 0.0:
        muminus_newProbNNmu[0] = math.log(eminusval)
    else:
        muminus_newProbNNmu[0] = -1000
    muminus_newProbNNmuBranch.Fill()
    
    muminus_ProbNNeBranch.GetEntry(i)
    if muminus_ProbNNe[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = muminus_ProbNNe[0]/(1-muminus_ProbNNe[0])
    if muminus_ProbNNe[0] > 0.0:
        muminus_newProbNNe[0] = math.log(eminusval)
    else:
        muminus_newProbNNe[0] = -1000
    muminus_newProbNNeBranch.Fill()
    
    muminus_ProbNNkBranch.GetEntry(i)
    if muminus_ProbNNk[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = muminus_ProbNNk[0]/(1-muminus_ProbNNk[0])
    if muminus_ProbNNk[0] > 0.0:
        muminus_newProbNNk[0] = math.log(eminusval)
    else:
        muminus_newProbNNk[0] = -1000
    muminus_newProbNNkBranch.Fill()


nt.SetBranchStatus("*", 1)
nt.Write("DecayTree")
nf.Close()

message = str(time.asctime(time.localtime())) + " Created new tree at /net/storage03/data/users/rstein/tuples/pid/" + tupleName+ ".root"
print message

import os, sys
sys.path.append('/home/rstein/pythonscripts/misc')
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message)