import sys, ROOT, time
import array
import argparse

print time.asctime(time.localtime()), "Starting Code"

#Parse Arguments to trigger each BDT module that is needed, as well as additional arguments

parser = argparse.ArgumentParser(description='Train BDT and analyse performance')
parser.add_argument("-t", "--tree", default = "MC_Bplus_Kplusmue_BDT")
parser.add_argument("-o", "--output", action="store_true")

cfg = parser.parse_args()

tuplePath = "/net/storage03/data/users/rstein/tuples/qsq/"
tupleName = str(cfg.tree)
treeName = "DecayTree"

#Load Tree and relevant branches

fullName = tuplePath + tupleName + ".root"

gtree = ROOT.TFile(fullName, "READ")

nt = gtree.Get(treeName)

nt.SetBranchStatus("*", 0)
nt.SetBranchStatus("Kplus_P", 1)
nt.SetBranchStatus("Kplus_PZ", 1)
nt.SetBranchStatus("eminus_P", 1)
nt.SetBranchStatus("eminus_PZ", 1)
nt.SetBranchStatus("muplus_P", 1)
nt.SetBranchStatus("muplus_PZ", 1)
nt.SetBranchStatus("B_M", 1)

#Creates arrays to enable each branch to be read

B_M = (array.array('d',[0]))
B_MBranch = nt.GetBranch("B_M")
B_MBranch.SetAddress(B_M)

Kplus_P = (array.array('d',[0]))
Kplus_PBranch = nt.GetBranch("Kplus_P")
Kplus_PBranch.SetAddress(Kplus_P)

Kplus_PZ = (array.array('d',[0]))
Kplus_PZBranch = nt.GetBranch("Kplus_PZ")
Kplus_PZBranch.SetAddress(Kplus_PZ)

muplus_P = (array.array('d',[0]))
muplus_PBranch = nt.GetBranch("muplus_P")
muplus_PBranch.SetAddress(muplus_P)

muplus_PZ = (array.array('d',[0]))
muplus_PZBranch = nt.GetBranch("muplus_PZ")
muplus_PZBranch.SetAddress(muplus_PZ)

eminus_P = (array.array('d',[0]))
eminus_PBranch = nt.GetBranch("eminus_P")
eminus_PBranch.SetAddress(eminus_P)

eminus_PZ = (array.array('d',[0]))
eminus_PZBranch = nt.GetBranch("eminus_PZ")
eminus_PZBranch.SetAddress(eminus_PZ)

print time.asctime(time.localtime()),"Itterating over", nt.GetEntries() , "events"

a = None
b = None
c = None
d = None
e = None
f = None
g = None

count = 0

#For each entry, check if any of the values match one from the previous entry
#After checking and counting any duplicate, the dynamic variables are reassigned

for i in range(nt.GetEntries()):
    Kplus_PBranch.GetEntry(i)
    Kplus_PZBranch.GetEntry(i)
    muplus_PBranch.GetEntry(i)
    muplus_PZBranch.GetEntry(i)
    eminus_PBranch.GetEntry(i)
    eminus_PZBranch.GetEntry(i)
    B_MBranch.GetEntry(i)
    if (Kplus_P[0]!= a) & (Kplus_PZ[0] != b) & (muplus_P[0] != c) & (muplus_PZ[0] != d) & (eminus_P[0] != e) & (eminus_PZ[0] != f) & (B_M[0] != g):
        pass
    else:
        count += 1
        if cfg.output == True:
            print a, b, c, d, e, f, g
            print Kplus_P[0], Kplus_PZ[0], muplus_P[0], muplus_PZ[0], eminus_P[0], eminus_PZ[0], B_M[0]
    a = Kplus_P[0]
    b = Kplus_PZ[0]
    c = muplus_P[0]
    d = muplus_PZ[0]
    e = eminus_P[0]
    f = eminus_PZ[0]
    g = B_M[0]
    
#Produces an output message with the duplicate number. Then sends an email notification.

message = str(time.asctime(time.localtime())) + " For the tree " + str(cfg.tree)  +".root, out of " + str(nt.GetEntries()) + " total events, there are " + str(count) + " entries with at least one duplicate value from the previous entry."
print message

import os, sys
sys.path.append('/home/rstein/pythonscripts/misc')
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message)