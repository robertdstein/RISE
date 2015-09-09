import ROOT, time

def plot(var, lowerlim, upperlim, data, MC, c, bincount, weighting=False):
    c.cd(1)
    
    #Plot both unweighted and weighted MC and Data on a single histogram, along with the Weighting
    
    print time.asctime(time.localtime()), "Plotting 1D Graphs"
        
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + data + "_sweight.root")
    t = f.Get("DecayTree")
    
    g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + MC + "_Weighted" + str(bincount) + ".root")
    u = g.Get("DecayTree") 
    
    h = ROOT.TFile("/home/rstein/pythonscripts/plotting/reweighting.root")
    v = h.Get("Histogram")
    
    rwmc = ROOT.TH1D("rwmc", "", bincount, lowerlim, upperlim)
    RealData = ROOT.TH1D("RealData", "", bincount, lowerlim, upperlim)
    Sweight= ROOT.TH1D("Sweight", "", bincount, lowerlim, upperlim)
    MonteCarlo= ROOT.TH1D("MonteCarlo", "", bincount, lowerlim, upperlim)
        
    u.Draw(var+">>MonteCarlo")
    u.Draw(var+">>rwmc", "Weight")
    t.Draw(var+">>RealData")
    t.Draw(var + ">>Sweight", "sweight")
    
    print "Weighting is", weighting    
    
    if weighting:
        
        if var == "B_PT":
            Weight = v.ProjectionX("Weight1d", 0, bincount)
        else:
            Weight = v.ProjectionY("Weight1d", 0, bincount)
    
        Weight.SetLineColor(ROOT.kOrange)
        Weight.SetMarkerColor(ROOT.kOrange)
        Weight.SetMarkerStyle(ROOT.kOpenCircle)
        x = Weight.GetXaxis()
        x.SetTitle(var)
        x.SetTitleSize(0.04)
        x.SetTitleOffset(1.15)
        y = Weight.GetYaxis()
        y.SetTitle("Relative Weight")
        y.SetTitleSize(0.04)
        y.SetTitleOffset(1.3)
    
        Weight.DrawCopy("E")
        
        c.cd(2)
    
    MonteCarlo.SetLineColor(ROOT.kBlue)
    MonteCarlo.SetMarkerColor(ROOT.kBlue)
    
    RealData.SetLineColor(ROOT.kRed)
    RealData.SetMarkerColor(ROOT.kRed)
    RealData.SetMarkerStyle(ROOT.kOpenCircle)
    
    Sweight.SetLineColor(ROOT.kGreen)
    Sweight.SetMarkerColor(ROOT.kGreen)
    Sweight.SetMarkerStyle(ROOT.kOpenCircle)

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
        
    print time.asctime(time.localtime()), "Completed variable", str(var)
    
    return Weight
