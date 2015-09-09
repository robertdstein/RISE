import ROOT
import math, time
from uncertainties import ufloat
import lhcbStyle as lhcb
import array

def reweight(name, var1, lowerlim1, upperlim1, var2, lowerlim2, upperlim2, data, MC, c, bincount):
    
    print time.asctime(time.localtime()), "Creating Empty Histogram"
    
    #Creates an empty Histogram to store the weights
    Weight = ROOT.TH2F("Weight", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    
    c.cd(1)
    
    #Open Trees containing the Monte Carlo and S-Weighted data, and plot two 2D Histograms which are saved as part of a PDF
    
    print time.asctime(time.localtime()), "Plotting 2D contour graphs"
    
    filename = "/net/storage03/data/users/rstein/tuples/qsq/" + MC
    
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + data + "_sweight.root", "READ")
    t = f.Get("DecayTree")
    
    g = ROOT.TFile(filename + ".root", "READ")
    u = g.Get("DecayTree")    
    
    Sweight= ROOT.TH2F("Sweight", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    MonteCarlo= ROOT.TH2F("MonteCarlo", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    
    u.Draw(var2 + ":" + var1 +">>MonteCarlo")
    t.Draw(var2 + ":" + var1 + ">>Sweight", "sweight")
    
    x = Sweight.GetXaxis()
    x.SetTitle(var1)
    x.SetTitleSize(0.04)
    x.SetTitleOffset(1.15)
    y = Sweight.GetYaxis()
    y.SetTitle(var2)
    y.SetTitleSize(0.04)
    y.SetTitleOffset(1.3) 
    Sweight.SetTitle("S Weighted Real Data")
    Sweight.DrawNormalized("ROOT.COLZ")
    
    c.cd(2)
    
    x = MonteCarlo.GetXaxis()
    x.SetTitle(var1)
    x.SetTitleSize(0.04)
    x.SetTitleOffset(1.15)
    y = MonteCarlo.GetYaxis()
    y.SetTitle(var2)
    y.SetTitleSize(0.04)
    y.SetTitleOffset(1.3) 
    MonteCarlo.SetTitle("Monte Carlo unweighted")
    MonteCarlo.DrawNormalized("ROOT.COLZ")
    c.Print("output/" + name + "_"+ str(bincount) + "2d.pdf(")
    
    c=ROOT.TCanvas()
    
    #Calculates a weight for each bin by dividing Sweight count by MC count
    #To Prevent generation of infinities, only bins with an MC count greater than 0 are given a weight 
    
    print time.asctime(time.localtime()), "Calculating Weight Bins"
            
    for i in range(0, bincount):
        for j in range (0, bincount):
            w=0
            sw = ufloat(Sweight.GetBinContent(i, j), Sweight.GetBinError(i,j))
            mc = ufloat(MonteCarlo.GetBinContent(i, j), MonteCarlo.GetBinError(i, j))
            if mc != 0:
                w = sw/mc
                Weight.SetBinContent(i,j,w.nominal_value)
                Weight.SetBinError(i,j,w.std_dev)
            elif mc == 0:
                Weight.SetBinContent(i,j, 0)
                Weight.SetBinError(i,j,0) 
    
    #Plots the now-filled Weight Histogram and adds this to the PDF file (named dynamically based on bincount and optional name arguments)
    
    print time.asctime(time.localtime()), "Plotting Weight Histogram"
    
    x = Weight.GetXaxis()
    x.SetTitle(var1)
    x.SetTitleSize(0.04)
    x.SetTitleOffset(1.15)
    y = Weight.GetYaxis()
    y.SetTitle(var2)
    y.SetTitleSize(0.04)
    y.SetTitleOffset(1.3) 
    Weight.DrawCopy("ROOT.COLZ")
    
    
    c.Print("output/" + name + "_" + str(bincount) + "2d.pdf")
    Weight.SetMarkerSize(0.1)
    Weight.DrawCopy("e")
    c.Print("output/" + name + "_"+ str(bincount) + "2d.pdf)")
    
    f.Close()
    
    #Creates a rewighting file, and saves the Histogram for later use
    
    h = ROOT.TFile("reweighting.root", "recreate")
        
    Weight.Write("Histogram")
    h.Write()
    h.Close()   
    
    print time.asctime(time.localtime()), "Weight Histogram saved"
    print time.asctime(time.localtime()), "Creating new Monte Carlo Tree at", filename + "_Weighted" + str(bincount) + ".root"
    
    #Creates a new MC TTree with a Weight Branch
    m = ROOT.TFile(filename + "_Weighted" + str(bincount) + ".root", "recreate")
    
    ucount = u.GetEntriesFast()
    print time.asctime(time.localtime()), "Contains", ucount, "entries"

    print time.asctime(time.localtime()), "Cloning Tree..."
    nt=u.CloneTree(-1, "fast")

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
    
    #Calculates the weight for each entry, based on the bin it lies in

    for counter in xrange(ucount):
        nt.GetEntry(counter)
        bptbinwidth = (upperlim1 - lowerlim1)/bincount
        spdbinwidth = (upperlim2 - lowerlim2)/bincount
        i = int(bpt[0]/bptbinwidth) +1
        j = int(spd[0]/spdbinwidth) + 1
        r = ROOT.TRandom3(0)
        o[0] = r.Gaus(Weight.GetBinContent(i, j), Weight.GetBinError(i, j))
        brBranch.Fill()

    nt.SetBranchStatus("*", 1)
    nt.Write()
    m.Close()

    print time.asctime(time.localtime()), "Branch Filled!"
        
c=ROOT.TCanvas()
c.Divide(2,1)
lhcb.setLHCbStyle()

#Extracts the two reweighting variables and their ranges from a CSV file, and then runs the Reweight function above based this information

def plotsep(name, source, data, MC, bincount):
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
        reweight(name, v[0], ul[0], ll[0], v[1], ul[1], ll[1], data, MC, c,bincount)
        