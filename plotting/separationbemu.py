import batchextract as be

name = "BDT Variables B to EMu"
source = 'sources/bmueBDT.csv'
data = "DATA_Bplus_Kplusmue_1112_MagUpDownminPtBranch.root"
datatree = "DecayTree"
MC = "MC_Bplus_Kplusmue_2012_MagUpDownminPtBranch.root"
MCtree = "DecayTree"

be.plotsep(name, source, data, datatree, MC, MCtree)