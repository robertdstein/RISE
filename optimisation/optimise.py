import time, os
import numpy as np
import argparse

#Code hub to run the different modules involved in optimisation

start = time.time()
print time.asctime(time.localtime()), "Starting Code"

parser = argparse.ArgumentParser(description='Optimise Branching ratio calculations')
parser.add_argument("-a", "--automate", action="store_true")
parser.add_argument("-p", "--plot", action="store_true")
parser.add_argument("-m", "--minimise", action="store_true")
parser.add_argument("-mk", "--minimisek", action="store_true")
parser.add_argument("-me", "--minimisee", action="store_true")
parser.add_argument("-mmu", "--minimisemu", action="store_true")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-s", "--source", default="results.csv")
parser.add_argument("-bdti", "--bdtinterval", default=0.01)
parser.add_argument("-bdtl", "--bdtlowerlim", default=0.70)
parser.add_argument("-bdtu", "--bdtupperlim", default=0.99)
parser.add_argument("-c", "--defaultcut", default=0.0)

cfg = parser.parse_args()

#Automatically calculates the branching ratio for a range of BDT values, outputting results in a csv file 

if cfg.automate == True:
    import automate as a
    a.process("results.csv", cfg.bdtinterval, cfg.bdtlowerlim, cfg.bdtupperlim, cfg.text)

#Reads results from a csv file, and plots a scatter graph of BDT value against branching ratio

if cfg.plot==True:
    import plotresults as p
    p.scattergraph(cfg.source)

if cfg.minimise == True:
    import minimise as m
    m.run(cfg.minimisek, cfg.minimisee, cfg.minimisemu, cfg.defaultcut, cfg.text)