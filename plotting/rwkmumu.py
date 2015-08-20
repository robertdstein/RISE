import rwbe
import argparse
import drw
import plotreweightedmc as plt

parser = argparse.ArgumentParser(description='Fit for B_M from dataset')
parser.add_argument("-b", "--bincount", default=100)
parser.add_argument("-d", "--double", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
cfg = parser.parse_args()

name = "Reweight kmumu"
source = 'sources/jsi2.csv'
data = "DATA_Bplus_Kplusmumu_qsqcut"
MC = "MC_Bplus_KplusJpsimumu_qsqcut"

if cfg.double:
    drw.plotsep(name, source, data, MC, int(cfg.bincount))    
elif cfg.graph:
     plt.plotsep(name, source, data, MC, int(cfg.bincount)) 
else:
    rwbe.plotsep(name, source, data, MC, int(cfg.bincount))