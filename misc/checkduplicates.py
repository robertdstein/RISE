import sys, ROOT, time
import array
import argparse

print time.asctime(time.localtime()), "Starting Code"

#Parse Arguments to modify functions 
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tree", default = "DATA_Bplus_Kplusmue_BDT")
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
nt.SetBranchStatus("runNumber", 1)
nt.SetBranchStatus("eventNumber", 1)

#Creates arrays to enable each branch to be read

runNumber = (array.array('d',[0]))
runNumberBranch = nt.GetBranch("runNumber")
runNumberBranch.SetAddress(runNumber)

eventNumber = (array.array('d',[0]))
eventNumberBranch = nt.GetBranch("eventNumber")
eventNumberBranch.SetAddress(eventNumber)

print time.asctime(time.localtime()),"Itterating over", nt.GetEntries() , "events"

a = None
b = None

count = 0

#For each entry, check if any of the values match one from the previous entry
#After checking and counting any duplicate, the dynamic variables are reassigned

for i in range(nt.GetEntries()):
    runNumberBranch.GetEntry(i)
    eventNumberBranch.GetEntry(i)
    if (runNumber[0] == a) & (eventNumber[0] == b) :
        count += 1
        if cfg.output == True:
            print a, b
            print runNumber[0], eventNumber[0]
    else:
        pass
    a = runNumber[0]
    b = eventNumber[0]
    
#Produces an output message with the duplicate number. Then sends an email notification.

message = str(time.asctime(time.localtime())) + " For the tree " + str(cfg.tree)  +".root, out of " + str(nt.GetEntries()) + " total events, there are " + str(count) + " entries with at least one duplicate value from the previous entry."
print message

import os, sys
sys.path.append('/home/rstein/pythonscripts/misc')
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message)