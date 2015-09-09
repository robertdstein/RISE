import rwbe
import argparse
import twodimensionalreweighting as tdrw
import plotreweightedmc as plt
import writekemu as wkemu
import time

parser = argparse.ArgumentParser(description='Reweight dataset based oin JPsi Data')
parser.add_argument("-b", "--bincount", default=100)
parser.add_argument("-r", "--reweight", action="store_true")
parser.add_argument("-w", "--write", action="store_true")
parser.add_argument("-cg", "--contourgraph", action="store_true")
parser.add_argument("-fg", "--flatgraph", action="store_true")
cfg = parser.parse_args()

name = "JPsi"
source = 'sources/jsi2.csv'
data = "DATA_Bplus_Kplusmumu_qsqcut"
MC = "MC_Bplus_KplusJpsimumu_qsqcut"

KemuMC = "MC_Bplus_Kplusmue_newresampled"

print time.asctime(time.localtime()), "Starting Code"

if cfg.reweight:
    #Creates a 2D weighting histogram from the JPsiK data, and adds a weight branch to the JpsiK MC
    tdrw.plotsep(name, source, data, MC, int(cfg.bincount))
    
if cfg.write:    
    #Loads the 2D Histogram and uses it to add a weight branch to the MC Data
    wkemu.extract(source, KemuMC, int(cfg.bincount))

if cfg.contourgraph:
    #Creates a PDF comparing the S Weighted Data and the Reweighted Monte Carlo Data
     plt.plotsep(name, source, data, MC, int(cfg.bincount)) 

if cfg.flatgraph:
    #Creates histograms showing the seperation betweeen Sweighted Data and Reweighted Monte Carlo for single variables
    rwbe.plotsep(name, source, data, MC, int(cfg.bincount), weighting=True)
    
print time.asctime(time.localtime()), "Code Finished"