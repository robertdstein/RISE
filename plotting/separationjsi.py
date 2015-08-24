import batchextract as be

name = "BDT Variables JSi"
source = 'sources/jsi.csv'
data = "with_bdt_kmumu_1112_isoln.root"
datatree = "DecayTree"
MC = "with_bdt_jpsik_12_mc_isoln_newpid_corr_allvars_eta.root"
MCtree = "DecayTree"

be.plotsep(name, source, data, datatree, MC, MCtree)

import os, sys
sys.path.append('/home/rstein/pythonscripts/misc')
import sendemail as se
name = os.path.basename(__file__)
se.send(name, "Plotting completed")