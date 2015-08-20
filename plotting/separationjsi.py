import batchextract as be

name = "BDT Variables JSi"
source = 'sources/jsi.csv'
data = "with_bdt_kmumu_1112_isoln.root"
datatree = "DecayTree"
MC = "with_bdt_jpsik_12_mc_isoln_newpid_corr_allvars_eta.root"
MCtree = "DecayTree"

be.plotsep(name, source, data, datatree, MC, MCtree)