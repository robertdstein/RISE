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
parser.add_argument("-d", "--dynamic", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-s", "--source", default="results")
parser.add_argument("-v", "--variable", default="bdt")
parser.add_argument("-vi", "--variableinterval", default=0.01)
parser.add_argument("-vl", "--variablelowerlim", default=0.70)
parser.add_argument("-vu", "--variableupperlim", default=0.99)
parser.add_argument("-sig", "--sigma", default=5)
parser.add_argument("-c", "--defaultcut", default=0.0)
parser.add_argument("-r", "--ratio", action="store_true")

cfg = parser.parse_args()

#Automatically calculates the branching ratio for a range of variable values, outputting results in a csv file 

if cfg.automate == True:
    import automate as a
    a.process("results.csv", cfg.variable, cfg.variableinterval, cfg.variablelowerlim, cfg.variableupperlim, text=cfg.text)

#Reads results from a csv file, and plots a scatter graph of variable value against branching ratio

if cfg.plot==True:
    import plotresults as p
    p.scattergraph(cfg.source)

#Run a Minimisation algorith to find the optimal cuts

if cfg.minimise == True:
    import minimise as m
    m.run(cfg.minimisek, cfg.minimisee, cfg.minimisemu, cfg.text)

#Calculate the ratio precicely, and with all status messages displayed on screen

if cfg.ratio == True:
    import newcalculate as c
    c.output(graph=cfg.graph, sigma = cfg.sigma)