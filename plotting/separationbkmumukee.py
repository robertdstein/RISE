import batchextract as be

name = "BDT Variables B to KMuMu and Kee"
source = 'sources/rkBDT.csv'
data = "DATA_Bplus_Kplusmue_1112_MagUpDown.root"
datatree = "Bu2LLK_meLine_TupleMDST/DecayTree"
MC = "MC_Bplus_Kplusmue_2012_MagUpDown.root"
MCtree = "Bu2LLK_meLine_TupleMC/DecayTree"

be.plotsep(name, source, data, datatree, MC, MCtree)