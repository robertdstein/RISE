import ROOT

def output(var, lowerlim, upperlim, data, datatree, MC, MCtree, weighting):
    bincount = 600
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/raw/" + data)
    t = f.Get(datatree)

    g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/raw/" + MC)
    u = g.Get(MCtree)
        
    RealData = ROOT.TH1D("RealData", "", bincount, lowerlim, upperlim)
    MonteCarlo= ROOT.TH1D("MonteCarlo", "", bincount, lowerlim, upperlim)

    if weighting == True:
        t.Draw(var+">>RealData", "sweight")
        u.Draw(var+">>MonteCarlo", "weight")
        
    else:
        t.Draw(var+">>RealData")
        u.Draw(var+">>MonteCarlo")

    RealData.SetLineColor(ROOT.kRed)
    RealData.SetMarkerColor(ROOT.kRed)
    RealData.SetMarkerStyle(ROOT.kOpenCircle)
  
    MonteCarlo.SetLineColor(ROOT.kBlue)
    MonteCarlo.SetMarkerColor(ROOT.kBlue)
    
    tcount = RealData.GetEntries()
    ucount = MonteCarlo.GetEntries()
    
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
        