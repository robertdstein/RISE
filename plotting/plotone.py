import ROOT
import lhcbStyle as lhcb


c=ROOT.TCanvas()
lhcb.setLHCbStyle()

bincount = 100
upperlim = 0.00001
lowerlim = 0
var = "sweight"

f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/raw/with_bdt_jpsik_12_mc_isoln_newpid_corr_allvars_etacut_sweight.root")
t = f.Get("DecayTree")

RealData = ROOT.TH1D("RealData", "", bincount, lowerlim, upperlim)

t.Draw(var+">>RealData")

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

raw_input("Prompt")