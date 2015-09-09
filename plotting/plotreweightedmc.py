import ROOT
import time
from uncertainties import ufloat
import lhcbStyle as lhcb
import array

def plot(name, var1, lowerlim1, upperlim1, var2, lowerlim2, upperlim2, data, MC, c, bincount):
        
    c.cd(1)
    
    #Open Trees containing the reweighted Monte Carlo and S-Weighted data, and plot two 2D Histograms for comparison
    
    print time.asctime(time.localtime()), "Plotting 2D contour graphs"

    filename = "/net/storage03/data/users/rstein/tuples/qsq/" + MC + "_Weighted" + str(bincount)
    
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + data + "_sweight.root", "READ")
    t = f.Get("DecayTree")
    
    g = ROOT.TFile(filename + ".root", "READ")
    u = g.Get("DecayTree")    
    
    Sweight= ROOT.TH2F("Sweight", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    MonteCarlo= ROOT.TH2F("MonteCarlo", "", bincount, lowerlim1, upperlim1, bincount, lowerlim2, upperlim2)
    
    u.Draw(var2 + ":" + var1 +">>MonteCarlo", "Weight")
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
    c.Print("output/" + name + "_"+ str(bincount) + "2d_reweighted.pdf(")
    
    #Plots a 3D distribution of bin counts for S Weighted Data, with error bars
    
    c=ROOT.TCanvas()
    Sweight.SetMarkerSize(0.1)
    Sweight.DrawNormalized("e")
    c.Print("output/" + name + "_"+ str(bincount) + "2d_reweighted.pdf")
    
    #Plots a 3D distribution of bin counts for reweighted Monte Carlo Data, with error bars
    
    c=ROOT.TCanvas()
    MonteCarlo.SetMarkerSize(0.1)
    MonteCarlo.DrawNormalized("e")
    c.Print("output/" + name + "_"+ str(bincount) + "2d_reweighted.pdf)")

c=ROOT.TCanvas()
c.Divide(2,1)
lhcb.setLHCbStyle()

#Extracts the two reweighting variables and their ranges from a CSV file, and then runs the Reweight function above based this information

def plotsep(name, source, data, MC, bincount):
    import csv
    def rowcount():
        with open(source, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = sum(1 for row in reader)
            return count
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
        plot(name, v[0], ul[0], ll[0], v[1], ul[1], ll[1], data, MC, c, bincount)