import ROOT, argparse

ROOT.gROOT.SetBatch(ROOT.kTRUE)

parser = argparse.ArgumentParser(description='Reweight dataset based oin JPsi Data')
parser.add_argument("-s", "--source", default="MC_Bplus_Kplusmue_newresampled_Weighted_4vectormass.root")
parser.add_argument("-t", "--tree", default="default")
parser.add_argument("-b", "--bins", default="100")
parser.add_argument("-l", "--lowerlim", default="-10")
parser.add_argument("-u", "--upperlim", default="7")
parser.add_argument("-v", "--variable", default="B_M")
parser.add_argument("-w", "--weighting", action="store_true")
cfg = parser.parse_args()

c=ROOT.TCanvas()

#Plots a graph for the Data
f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + cfg.source)
t = f.Get(cfg.tree)
        
RealData = ROOT.TH1D("RealData", "", int(cfg.bins), float(cfg.lowerlim), float(cfg.upperlim))
    
#If Weighting is true, the reweighted Data will be plotted    

if cfg.weighting == True:
    t.Draw(cfg.variable+">>RealData", "Weight")

#If not, the raw Data will be plotted
    
else:
    t.Draw(cfg.variable+">>RealData")

RealData.SetLineColor(ROOT.kRed)
RealData.SetMarkerColor(ROOT.kRed)

x = RealData.GetXaxis()
x.SetTitle(cfg.variable)
x.SetTitleSize(0.04)
x.SetTitleOffset(1.15)
y = RealData.GetYaxis()
y.SetTitle("Normalised Count")
y.SetTitleSize(0.04)
y.SetTitleOffset(1.3) 
RealData.DrawNormalized("E")

c.Print("output/presentation/" + cfg.variable + ".pdf")