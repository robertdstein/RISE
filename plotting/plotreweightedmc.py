import ROOT
import math
from uncertainties import ufloat
import lhcbStyle as lhcb
import array

def plot(name, var1, lowerlim1, upperlim1, var2, lowerlim2, upperlim2, data, MC, c, oldw, bincount):
        
    c.cd(1)
    
    filename = "/net/storage03/data/users/rstein/tuples/qsq/" + MC + "_weighted" + str(bincount)
    
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + data + "_sweight.root", "READ")
    t = f.Get("DecayTree")
    
    g = ROOT.TFile(filename + ".root", "READ")
    u = g.Get("DecayTree")    
    
    Sweight= ROOT.TH2F("Sweight", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    MonteCarlo= ROOT.TH2F("MonteCarlo", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    
    u.Draw(var2 + ":" + var1 +">>MonteCarlo", "weight")
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
    MonteCarlo.SetTitle("Monte Carlo weighted")
    MonteCarlo.DrawNormalized("ROOT.COLZ")
    c.Print(name + str(bincount) + "2dreweighted.pdf(")
    
    c=ROOT.TCanvas()
    Sweight.SetMarkerSize(0.1)
    Sweight.DrawNormalized("e")
    c.Print(name + str(bincount) + "2dreweighted.pdf")
    
    c=ROOT.TCanvas()
    MonteCarlo.SetMarkerSize(0.1)
    MonteCarlo.DrawNormalized("e")
    c.Print(name + str(bincount) + "2dreweighted.pdf)")

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
        plot(name, v[0], ul[0], ll[0], v[1], ul[1], ll[1], data, MC, c, a, bincount)