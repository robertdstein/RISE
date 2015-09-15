import ROOT
import array, time, math

#Add a branch with the minimum transverse momentum

print time.asctime(time.localtime()), "writing a tree"

datasource2 = "DATA_Bplus_Kplusmue_BDTcut_newProbNN.root"

treename = "DecayTree"
filename = "/net/storage03/data/users/rstein/tuples/qsq/" + datasource2

f = ROOT.TFile(filename, "READ")
t = f.Get(treename)
g = ROOT.TFile(filename[:filename.find(".root")] + "_4vectormass.root", "recreate")

tcount = t.GetEntriesFast()
print time.asctime(time.localtime()), "Contains", tcount, "entries"

print time.asctime(time.localtime()), "Cloning Tree..."
nt=t.CloneTree(-1, "fast")

nt.SetBranchStatus("*",0)
nt.SetBranchStatus("eminus_PX", 1)
nt.SetBranchStatus("eminus_PY", 1)
nt.SetBranchStatus("eminus_PZ", 1)
nt.SetBranchStatus("eminus_M", 1)
nt.SetBranchStatus("muplus_PX", 1)
nt.SetBranchStatus("muplus_PY", 1)
nt.SetBranchStatus("muplus_PZ", 1)
nt.SetBranchStatus("muplus_M", 1)
nt.SetBranchStatus("Kplus_PX", 1)
nt.SetBranchStatus("Kplus_PY", 1)
nt.SetBranchStatus("Kplus_PZ", 1)
nt.SetBranchStatus("Kplus_M", 1)

ek = (array.array('f',[0]))
ekBranch = nt.Branch('ElectronKaonMass', ek, 'ElectronKaonMass/F')

mk = (array.array('f',[0]))
mkBranch = nt.Branch('MuonKaonMass', mk, 'MuonKaonMass/F')

electronpx = (array.array('d',[0]))
electronpxBranch = nt.GetBranch("eminus_PX")
electronpxBranch.SetAddress(electronpx)

electronpy = (array.array('d',[0]))
electronpyBranch = nt.GetBranch("eminus_PY")
electronpyBranch.SetAddress(electronpy)

electronpz = (array.array('d',[0]))
electronpzBranch = nt.GetBranch("eminus_PZ")
electronpzBranch.SetAddress(electronpz)

electronm = (array.array('d',[0]))
electronmBranch = nt.GetBranch("eminus_M")
electronmBranch.SetAddress(electronm)

muonpx = (array.array('d',[0]))
muonpxBranch = nt.GetBranch("muplus_PX")
muonpxBranch.SetAddress(muonpx)

muonpy = (array.array('d',[0]))
muonpyBranch = nt.GetBranch("muplus_PY")
muonpyBranch.SetAddress(muonpy)

muonpz = (array.array('d',[0]))
muonpzBranch = nt.GetBranch("muplus_PZ")
muonpzBranch.SetAddress(muonpz)

muonm = (array.array('d',[0]))
muonmBranch = nt.GetBranch("muplus_M")
muonmBranch.SetAddress(muonm)

kaonpx = (array.array('d',[0]))
kaonpxBranch = nt.GetBranch("Kplus_PX")
kaonpxBranch.SetAddress(kaonpx)

kaonpy = (array.array('d',[0]))
kaonpyBranch = nt.GetBranch("Kplus_PY")
kaonpyBranch.SetAddress(kaonpy)

kaonpz = (array.array('d',[0]))
kaonpzBranch = nt.GetBranch("Kplus_PZ")
kaonpzBranch.SetAddress(kaonpz)

kaonm = (array.array('d',[0]))
kaonmBranch = nt.GetBranch("Kplus_M")
kaonmBranch.SetAddress(kaonm)

print time.asctime(time.localtime()), "Tree Cloned!"

#Fills the branch with the magnitude of the sum of the e/k and mu/k 4 vectors

print time.asctime(time.localtime()), "Filling Branch..."

for i in xrange(tcount):
    nt.GetEntry(i)
    
    eenergy = math.sqrt((electronm[0]**2) + (electronpx[0]**2) + (electronpy[0]**2) + (electronpz[0]**2))
    
    e4vector = ROOT.TLorentzVector(electronpx[0], electronpy[0], electronpz[0], eenergy) 
    
    muenergy =  math.sqrt((muonm[0]**2) + (muonpx[0]**2) + (muonpy[0]**2) + (muonpz[0]**2))
    
    mu4vector = ROOT.TLorentzVector(muonpx[0], muonpy[0], muonpz[0], muenergy) 
    
    kenergy = math.sqrt((kaonm[0]**2) + (kaonpx[0]**2) + (kaonpy[0]**2) + (kaonpz[0]**2))
    
    k4vector = ROOT.TLorentzVector(kaonpx[0], kaonpy[0], kaonpz[0], kenergy) 
    
    ek4vector = e4vector + k4vector
    ek[0] = ek4vector.M()
    ekBranch.Fill()
    
    mk4vector = mu4vector + k4vector
    mk[0] = mk4vector.M()
    mkBranch.Fill()

nt.SetBranchStatus("*", 1)
nt.Write()
g.Close()

print time.asctime(time.localtime()), "Branch Filled!"