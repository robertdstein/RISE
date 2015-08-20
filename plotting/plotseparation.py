import ROOT
import lhcbStyle as lhcb
import plotupdatedfunctions as pf

var= "nTracks"
lowerlim = 0.0
upperlim = 400

data = "with_bdt_kmumu_1112_isoln.root"
datatree = "DecayTree"
MC = "jpsik_12_mc_allVars.root"
MCtree = "DecayTree"

c=ROOT.TCanvas()
lhcb.setLHCbStyle()
c.SetTitle(var)

pf.output(var, lowerlim, upperlim, data, datatree, MC, MCtree)

raw_input("Prompt")