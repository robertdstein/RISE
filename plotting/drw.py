import ROOT
import math
from uncertainties import ufloat
import lhcbStyle as lhcb
import array

def reweight(name, var1, lowerlim1, upperlim1, var2, lowerlim2, upperlim2, data, MC, c, oldw, bincount):
    
    Weight = ROOT.TH2F("Weight", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    
    c.cd(1)
    
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
    c.Print(name + str(bincount) + "2d.pdf(")
    
    c=ROOT.TCanvas()
        
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
    
    x = Weight.GetXaxis()
    x.SetTitle(var1)
    x.SetTitleSize(0.04)
    x.SetTitleOffset(1.15)
    y = Weight.GetYaxis()
    y.SetTitle(var2)
    y.SetTitleSize(0.04)
    y.SetTitleOffset(1.3) 
    Weight.DrawCopy("ROOT.COLZ")
    
    
    c.Print(name + str(bincount) + "2d.pdf")
    Weight.SetMarkerSize(0.1)
    Weight.DrawCopy("e")
    c.Print(name + str(bincount) + "2d.pdf)")
    
    f.Close()
    
    h = ROOT.TFile("reweighting.root", "recreate")
        
    Weight.Write("Histogram")
    h.Write()
    h.Close()   
    
    m = ROOT.TFile(filename + "_weighted" + str(bincount) + ".root", "recreate")
    
    ucount = u.GetEntriesFast()
    print "Contains", ucount, "entries"

    print "Cloning Tree..."
    nt=u.CloneTree(-1, "fast")

    nt.SetBranchStatus("*",0)
    nt.SetBranchStatus("B_PT", 1)
    nt.SetBranchStatus("nSPDHits", 1)

    o = (array.array('d',[0]))
    brBranch = nt.Branch('weight', o, 'weight/D')

    bpt = (array.array('d',[0]))
    bptBranch = nt.GetBranch("B_PT")
    bptBranch.SetAddress(bpt)

    spd = (array.array('l',[0]))
    spdBranch = nt.GetBranch("nSPDHits")
    spdBranch.SetAddress(spd)

    print "Tree Cloned!"

    print "Filling Branch..."

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

    print "Branch Filled!"
        
c=ROOT.TCanvas()
c.Divide(2,1)
lhcb.setLHCbStyle()

def plotsep(name, source, data, MC, bincount):
    import csv
    def rowcount():
        with open(source, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = sum(1 for row in reader)
            return count
    with open(source, 'rb') as csvfile:
        i = 0
        a = None
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
        reweight(name, v[0], ul[0], ll[0], v[1], ul[1], ll[1], data, MC, c, a, bincount)
        