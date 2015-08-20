import batchextract as be
import argparse

parser = argparse.ArgumentParser(description='plot seperation of reweighted data')
parser.add_argument("-b", "--bincount", default=100)

cfg = parser.parse_args()

bincount = cfg.bincount
name = "BDT Reweight " + str(bincount) +" Variables JSi"
source = 'sources/jsi.csv'
data = "with_bdt_kmumu_1112_isolncut_sweight.root"
datatree = "DecayTree"
MC = "with_bdt_jpsik_12_mc_isoln_newpid_corr_allvars_etacut_weighted" + str(bincount) +".root"
MCtree = "DecayTree"
weighting = True

be.plotsep(name, source, data, datatree, MC, MCtree, weighting)