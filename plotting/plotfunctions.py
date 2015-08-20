import ROOT

def output(var, lowerlim, upperlim):
    bincount = 100
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/raw/DATA_Bplus_Kplusmue_1112_MagUpDown.root")
    t = f.Get("Bu2LLK_meLine_TupleMDST/DecayTree")

    g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/raw/MC_Bplus_Kplusmue_2012_MagUpDown.root")
    u = g.Get("Bu2LLK_meLine_TupleMC/DecayTree")

    RealData = ROOT.TH1D("RealData", "", bincount, lowerlim, upperlim)
    MonteCarlo= ROOT.TH1D("MonteCarlo", "", bincount, lowerlim, upperlim)

    t.Draw(var+">>RealData")
    u.Draw(var+">>MonteCarlo")

    RealData.SetLineColor(ROOT.kRed)
    RealData.SetMarkerColor(ROOT.kRed)
    RealData.SetMarkerStyle(ROOT.kOpenCircle)
    x = RealData.GetXaxis()
    x.SetTitle(var)
    x.SetTitleSize(0.04)
    x.SetTitleOffset(1.15)
    y = RealData.GetYaxis()
    y.SetTitle("Normalised Count")
    y.SetTitleSize(0.04)
    y.SetTitleOffset(1.3)   
    RealData.DrawNormalized("E")
    MonteCarlo.SetLineColor(ROOT.kBlue)
    MonteCarlo.SetMarkerColor(ROOT.kBlue)
    MonteCarlo.DrawNormalized("ESame")