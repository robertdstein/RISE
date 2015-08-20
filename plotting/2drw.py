import ROOT
import math
from uncertainties import ufloat
import lhcbStyle as lhcb

def reweight(var1, lowerlim1, upperlim1, var2, lowerlim2, upperlim2, data, MC, c, oldw, bincount):
    
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/raw/" + data + "_sweight.root")
    t = f.Get("DecayTree")
    
    g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/raw/" + MC + ".root")
    u = g.Get("DecayTree")    
    
    Sweight= ROOT.TH2("Sweight", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    MonteCarlo= ROOT.TH2("MonteCarlo", "", bincount, lowerlim1, upperlim1, lowerlim2, upperlim2)
    
    u.Draw(var1+">>MonteCarlo", var2+">>MonteCarlo")
    t.Draw(var1 + ">>Sweight", var2 + ">>Sweight", "sweight", "sweight")
    

    x = Sweight.GetXaxis()
    x.SetTitle(var1)
    x.SetTitleSize(0.04)
    x.SetTitleOffset(1.15)
    y = Sweight.GetYaxis()
    y.SetTitle(var2)
    y.SetTitleSize(0.04)
    y.SetTitleOffset(1.3) 
    Sweight.DrawNormalized("ROOT.COL")
        
c=ROOT.TCanvas()
c.Divide(2,3)
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
        reweight(v[0], ul[0], ll[0], v[1], ul[1], ll[1], data, MC, c, a, bincount)
        c.Print(name + str(bincount) + "2d.pdf")