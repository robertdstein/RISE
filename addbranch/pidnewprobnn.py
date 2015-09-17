import sys, ROOT, os, math, time
import array

#Adds a branch with transformed ProbNN branches, requiring less fine intervals for cutting/resampling

tuplePath = "/fhgfs/users/kschubert/public/robert/"
tupleName = "Kaon_Stripping20r1_MagnetDown"
treeName = "tree"

fullName = tuplePath + tupleName + ".root"

f = ROOT.TFile(fullName, "READ")

if not f.IsOpen() :
    print("file " + fullName + " not found")
    exit()

t = f.Get(treeName)

if not t :
    print("tree " + treeName + " not found")
    exit()

nFileName = "/net/storage03/data/users/rstein/tuples/pid/" + tupleName+ ".root"
print('saving File to ' + nFileName)

nf = ROOT.TFile(nFileName, "RECREATE")
print "cloning tree..."
nt = t.CloneTree(-1, 'fast')

nt.SetBranchStatus("*", 0)

#Creates new Branches for each of the 3 relevant ProbNN values

nt.SetBranchStatus("K_V3ProbNNmu", 1)

K_newProbNNmu = (array.array('d',[0]))
K_newProbNNmuBranch = nt.Branch("K_newProbNNmu", K_newProbNNmu, "K_newProbNNmu/D")

K_V3ProbNNmu = (array.array('d',[0]))
K_V3ProbNNmuBranch = nt.GetBranch("K_V3ProbNNmu")
K_V3ProbNNmuBranch.SetAddress(K_V3ProbNNmu)

nt.SetBranchStatus("K_V3ProbNNe", 1)

K_newProbNNe = (array.array('d',[0]))
K_newProbNNeBranch = nt.Branch("K_newProbNNe", K_newProbNNe, "K_newProbNNe/D")

K_V3ProbNNe = (array.array('d',[0]))
K_V3ProbNNeBranch = nt.GetBranch("K_V3ProbNNe")
K_V3ProbNNeBranch.SetAddress(K_V3ProbNNe)

nt.SetBranchStatus("K_V3ProbNNK", 1)

K_newProbNNK = (array.array('d',[0]))
K_newProbNNKBranch = nt.Branch("K_newProbNNK", K_newProbNNK, "K_newProbNNK/D")

K_V3ProbNNK = (array.array('d',[0]))
K_V3ProbNNKBranch = nt.GetBranch("K_V3ProbNNK")
K_V3ProbNNKBranch.SetAddress(K_V3ProbNNK)

#Fills the new transformed values for each ProbNN value
#Returns an error value of -1000 if ProbNN is not greater than 0

print "itterating over", nt.GetEntries() , "events"
for i in range(nt.GetEntries()):
    K_V3ProbNNmuBranch.GetEntry(i)
    if K_V3ProbNNmu[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = K_V3ProbNNmu[0]/(1-K_V3ProbNNmu[0])
    if K_V3ProbNNmu[0] > 0.0:
        K_newProbNNmu[0] = math.log(eminusval)
    else:
        K_newProbNNmu[0] = -1000
    K_newProbNNmuBranch.Fill()
    
    K_V3ProbNNeBranch.GetEntry(i)
    if K_V3ProbNNe[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = K_V3ProbNNe[0]/(1-K_V3ProbNNe[0])
    if K_V3ProbNNe[0] > 0.0:
        K_newProbNNe[0] = math.log(eminusval)
    else:
        K_newProbNNe[0] = -1000
    K_newProbNNeBranch.Fill()
    
    K_V3ProbNNKBranch.GetEntry(i)
    if K_V3ProbNNK[0] == 1.0:
        eminusval = float("inf")
    else:
        eminusval = K_V3ProbNNK[0]/(1-K_V3ProbNNK[0])
    if K_V3ProbNNK[0] > 0.0:
        K_newProbNNK[0] = math.log(eminusval)
    else:
        K_newProbNNK[0] = -1000
    K_newProbNNKBranch.Fill()

nt.SetBranchStatus("*", 1)
nt.Write("DecayTree")
nf.Close()