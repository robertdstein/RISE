import rwbe
import argparse
import pylab as pl

name = "JPsi"
source = 'sources/jsi2.csv'
data = "with_bdt_kmumu_1112_isolncut"
MC = "with_bdt_jpsik_12_mc_isoln_newpid_corr_allvars_etacut"

b=[]
chindofperbin=[]

for i in range(1, 15):
    n = i*600
    b.append(n)
    z = rwbe.plotsep(name, source, data, MC, n)
    chindofperbin.append(z)
    print i
    
pl.plot(b, chindofperbin)
pl.show()
raw_input("prompt")