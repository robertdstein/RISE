import ROOT
import math
from uncertainties import ufloat

def reweight(var, lowerlim, upperlim, data, MC, c, oldw, bincount):
    
    
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + data + "_sweight.root")
    t = f.Get("DecayTree")
    
    g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + MC + "_weighted" + str(bincount) + ".root")
    u = g.Get("DecayTree") 
      
    rwmc = ROOT.TH1D("rwmc", "", bincount, lowerlim, upperlim)
    RealData = ROOT.TH1D("RealData", "", bincount, lowerlim, upperlim)
    Sweight= ROOT.TH1D("Sweight", "", bincount, lowerlim, upperlim)
    MonteCarlo= ROOT.TH1D("MonteCarlo", "", bincount, lowerlim, upperlim)
    
    
    u.Draw(var+">>MonteCarlo")
    u.Draw(var+">>rwmc", "weight")
    t.Draw(var+">>RealData")
    t.Draw(var + ">>Sweight", "sweight")
    
    tcount = RealData.GetEntries()
    ucount = MonteCarlo.GetEntries()
                
    MonteCarlo.SetLineColor(ROOT.kBlue)
    MonteCarlo.SetMarkerColor(ROOT.kBlue)
    
    RealData.SetLineColor(ROOT.kRed)
    RealData.SetMarkerColor(ROOT.kRed)
    RealData.SetMarkerStyle(ROOT.kOpenCircle)
    
    Sweight.SetLineColor(ROOT.kGreen)
    Sweight.SetMarkerColor(ROOT.kGreen)
    Sweight.SetMarkerStyle(ROOT.kOpenCircle)
    
    datamax = RealData.GetMaximum()/tcount
    mcmax = MonteCarlo.GetMaximum()/ucount
    
    if datamax > mcmax:    
        x = RealData.GetXaxis()
        x.SetTitle(var)
        x.SetTitleSize(0.04)
        x.SetTitleOffset(1.15)
        y = RealData.GetYaxis()
        y.SetTitle("Normalised Count")
        y.SetTitleSize(0.04)
        y.SetTitleOffset(1.3) 
        RealData.DrawNormalized("E")
        MonteCarlo.DrawNormalized("ESame")
        Sweight.DrawNormalized("ESame")
        rwmc.DrawNormalized("ESame")
        
    else:
        x = MonteCarlo.GetXaxis()
        x.SetTitle(var)
        x.SetTitleSize(0.04)
        x.SetTitleOffset(1.15)
        y = MonteCarlo.GetYaxis()
        y.SetTitle("Normalised Count")
        y.SetTitleSize(0.04)
        y.SetTitleOffset(1.3)        
        MonteCarlo.DrawNormalized("E")
        RealData.DrawNormalized("ESame")
        Sweight.DrawNormalized("ESame")
        rwmc.DrawNormalized("ESame")
    
    c.Update()
    pull = 0
    nbins = 0
    for i in range(0, bincount):
        mc = ufloat((rwmc.GetBinContent(i)/ucount), (rwmc.GetBinError(i)/ucount))
        rd = ufloat((Sweight.GetBinContent(i)/tcount), (Sweight.GetBinError(i)/tcount))
        if rd !=0:
            p = ((mc - rd)**2)/rd
            pull +=p
            nbins +=1
    cndof = pull/nbins
    print "Total Pull", pull
    print "Total Bins", nbins
    print "Chi per bin", cndof
    print "relative chi per bin uncertainty", cndof.s/cndof.n
