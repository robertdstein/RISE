import sys, ROOT, os, math
import array

tuplePath = "/net/storage03/data/users/rstein/tuples/qsq/"
tupleName = "MC_Bplus_Kplusmue_BDT"
treeName = "DecayTree"

tuplePath = "/net/storage03/data/users/dberninghoff/B2Kll/Merged/MC_Bplus_Kplusmue"
tupleName = "MC_Bplus_Kplusmue"
treeName = "Bu2LLK_meLine_TupleMC/DecayTree"

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
nt.SetBranchStatus("Kplus_P", 1)
nt.SetBranchStatus("Kplus_PZ", 1)
nt.SetBranchStatus("eminus_P", 1)
nt.SetBranchStatus("eminus_PZ", 1)
nt.SetBranchStatus("muplus_P", 1)
nt.SetBranchStatus("muplus_PZ", 1)

Kplus_LOKI_ETA = (array.array('d',[0]))
Kplus_LOKI_ETABranch = nt.Branch("Kplus_LOKI_ETA", Kplus_LOKI_ETA, "Kplus_LOKI_ETA/D")

Kplus_P = (array.array('d',[0]))
Kplus_PBranch = nt.GetBranch("Kplus_P")
Kplus_PBranch.SetAddress(Kplus_P)

Kplus_PZ = (array.array('d',[0]))
Kplus_PZBranch = nt.GetBranch("Kplus_PZ")
Kplus_PZBranch.SetAddress(Kplus_PZ)

muplus_LOKI_ETA = (array.array('d',[0]))
muplus_LOKI_ETABranch = nt.Branch("muplus_LOKI_ETA", muplus_LOKI_ETA, "muplus_LOKI_ETA/D")

muplus_P = (array.array('d',[0]))
muplus_PBranch = nt.GetBranch("muplus_P")
muplus_PBranch.SetAddress(muplus_P)

muplus_PZ = (array.array('d',[0]))
muplus_PZBranch = nt.GetBranch("muplus_PZ")
muplus_PZBranch.SetAddress(muplus_PZ)

eminus_LOKI_ETA = (array.array('d',[0]))
eminus_LOKI_ETABranch = nt.Branch("eminus_LOKI_ETA", eminus_LOKI_ETA, "eminus_LOKI_ETA/D")

eminus_P = (array.array('d',[0]))
eminus_PBranch = nt.GetBranch("eminus_P")
eminus_PBranch.SetAddress(eminus_P)

eminus_PZ = (array.array('d',[0]))
eminus_PZBranch = nt.GetBranch("eminus_PZ")
eminus_PZBranch.SetAddress(eminus_PZ)

print "itterating over", nt.GetEntries() , "events"
for i in range(nt.GetEntries()):
    Kplus_PBranch.GetEntry(i)
    Kplus_PZBranch.GetEntry(i)
    kplusval = (math.fabs(Kplus_P[0]) + Kplus_PZ[0])/(math.fabs(Kplus_P[0]) - Kplus_PZ[0])
    if kplusval > -1.0:
        Kplus_LOKI_ETA[0] = 0.5*math.log(kplusval)
    else:
        Kplus_LOKI_ETA[0] = -2000
    Kplus_LOKI_ETABranch.Fill()
    muplus_PBranch.GetEntry(i)
    muplus_PZBranch.GetEntry(i)
    muval = (math.fabs(muplus_P[0]) + muplus_PZ[0])/(math.fabs(muplus_P[0]) - muplus_PZ[0])
    if muval > -1.0:
        muplus_LOKI_ETA[0] = 0.5*math.log(muval)
    else:
        muplus_LOKI_ETA[0] = -2000
    muplus_LOKI_ETABranch.Fill()
    eminus_PBranch.GetEntry(i)
    eminus_PZBranch.GetEntry(i)
    eminusval = (math.fabs(eminus_P[0]) + eminus_PZ[0])/(math.fabs(eminus_P[0]) - eminus_PZ[0])
    print eminus_P[0]
    if eminusval > -1.0:
        eminus_LOKI_ETA[0] = 0.5*math.log(eminusval)
    else:
        eminus_LOKI_ETA[0] = -2000
    eminus_LOKI_ETABranch.Fill()

nt.SetBranchStatus("*", 1)
nt.Write("DecayTree")
nf.Close()