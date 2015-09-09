import ROOT, time
import math
from uncertainties import ufloat
import lhcbStyle as lhcb
import array

def reweight(var1, lowerlim1, upperlim1, var2, lowerlim2, upperlim2, MC, bincount):
    
    #Open the MC data to be reweighted, as well as the Histogram storing the Weights
    
    filename = "/net/storage03/data/users/rstein/tuples/qsq/" + MC
    
    f = ROOT.TFile(filename + ".root", "READ")
    t = f.Get("default")
    
    g = ROOT.TFile("/home/rstein/pythonscripts/plotting/reweighting.root", "READ")
    WeightHistogram = g.Get("Histogram")
    
    #Create a new Tree with a Weight Branch 
    
    m = ROOT.TFile(filename + "_Weighted.root", "recreate")
    
    print time.asctime(time.localtime()), "Creating new Monte Carlo Tree at", filename + "_Weighted.root"
    
    tcount = t.GetEntriesFast()
    print time.asctime(time.localtime()), "Contains", tcount, "entries"

    print time.asctime(time.localtime()), "Cloning Tree..."
    nt=t.CloneTree(-1, "fast")

    nt.SetBranchStatus("*",0)
    nt.SetBranchStatus("B_PT", 1)
    nt.SetBranchStatus("nSPDHits", 1)

    o = (array.array('d',[0]))
    brBranch = nt.Branch('Weight', o, 'Weight/D')

    bpt = (array.array('d',[0]))
    bptBranch = nt.GetBranch("B_PT")
    bptBranch.SetAddress(bpt)

    spd = (array.array('l',[0]))
    spdBranch = nt.GetBranch("nSPDHits")
    spdBranch.SetAddress(spd)

    print time.asctime(time.localtime()), "Tree Cloned!"

    print time.asctime(time.localtime()), "Filling Branch..."
    
    #Calculates the weight for each entry by reading the Histogram

    for counter in xrange(tcount):
        nt.GetEntry(counter)
        bptbinwidth = (upperlim1 - lowerlim1)/bincount
        spdbinwidth = (upperlim2 - lowerlim2)/bincount
        i = int(bpt[0]/bptbinwidth) +1
        j = int(spd[0]/spdbinwidth) + 1
        r = ROOT.TRandom3(0)
        o[0] = r.Gaus(WeightHistogram.GetBinContent(i, j), WeightHistogram.GetBinError(i, j))
        brBranch.Fill()

    nt.SetBranchStatus("*", 1)
    nt.Write()
    m.Close()

    print time.asctime(time.localtime()), "Branch Filled!"
     
#Extracts the two reweighting variables and their ranges from a CSV file, and then runs the Reweight function above based this information

def extract(source, MC, bincount):
    import csv
    print time.asctime(time.localtime()), "Extracting information from " + str(source)
    with open(source, 'rb') as csvfile:
        i = 0
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        v = []
        ul = []
        ll = []
        for row in reader:
            x = row
            v.append(x[0])
            ul.append(float(x[1]))
            ll.append(float(x[2]))
            i+=1
        reweight(v[0], ul[0], ll[0], v[1], ul[1], ll[1], MC, bincount)    