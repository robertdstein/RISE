import ROOT, argparse
import lhcbStyle as lhcb
import batchextract as be

parser = argparse.ArgumentParser(description='Reweight dataset based oin JPsi Data')
parser.add_argument("-d", "--decay", default="B2Kemu")
parser.add_argument("-b", "--bins", default="100")
cfg = parser.parse_args()

#Creates seperation plots based on CSV file data listing variables and ranges

#Parameters for common B2Kemu BDT variables
if cfg.decay == "B2Kemu":
    name = "BDT_Variables_B_to_EMu"
    source = 'sources/bmueBDT.csv'
    data = "raw/DATA_Bplus_Kplusmue_1112_MagUpDownminPtBranch.root"
    datatree = "DecayTree"
    MC = "raw/MC_Bplus_Kplusmue_2012_MagUpDownminPtBranch.root"
    MCtree = "DecayTree"
    weighting=False
    
if cfg.decay == "cutB2Kemu":
    name = "cut_Variables_B_to_EMu"
    source = 'sources/cutdata.csv'
    data = "qsq/DATA_Bplus_Kplusmue_BDTcut_newProbNN_4vectormass.root"
    datatree = "DecayTree"
    MC = "qsq/MC_Bplus_Kplusmue_newresampled_Weighted_4vectormass.root"
    MCtree = "default"
    weighting=False

#arameters for common B2Kmumu BDT variables
elif cfg.decay == "B2Kmumu":
    name = "BDT_Variables_B_to_KMuMu"
    source = 'sources/rkBDT.csv'
    data = "raw/DATA_Bplus_Kplusmue_1112_MagUpDown.root"
    datatree = "Bu2LLK_meLine_TupleMDST/DecayTree"
    MC = "raw/MC_Bplus_Kplusmue_2012_MagUpDown.root"
    MCtree = "Bu2LLK_meLine_TupleMC/DecayTree"
    weighting=False

#Parameters for common B2JPsiK BDT variables    
elif cfg.decay == "B2JPsiK":
    name = "BDT_Variables_JPsi"
    source = 'sources/jsi.csv'
    data = "raw/with_bdt_kmumu_1112_isoln.root"
    datatree = "DecayTree"
    MC = "raw/with_bdt_jpsik_12_mc_isoln_newpid_corr_allvars_eta.root"
    MCtree = "DecayTree"
    weighting=False

#Parameters for common B2Kemu BDT variables, using reweighted MC and sweighted Data
elif cfg.decay == "rwB2JPsiK":
    name = "BDT_Reweight_" + cfg.bins +"_Variables_JPsi"
    source = 'sources/jsi.csv'
    data = "raw/with_bdt_kmumu_1112_isolncut_sweight.root"
    datatree = "DecayTree"
    MC = "raw/with_bdt_jpsik_12_mc_isoln_newpid_corr_allvars_etacut_weighted" + cfg.bins +".root"
    MCtree = "DecayTree"
    weighting = True

#Raise Error if invalid decay channel argument is used
else:
    print "Accepted decay channels are: B2Kemu, B2Kmumu, B2JPsiK, rwB2JPsiK, cutB2Kemu"
    raise NameError("Invalid Decay Channel")

#Plot graphs with parameters chosen above
be.plotsep(name, source, data, datatree, MC, MCtree, weighting, int(cfg.bins))