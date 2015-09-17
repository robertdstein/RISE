import ROOT, time, os, csv
import numpy as np
import argparse
import branchingratio as br
import fit as f
import simulate as s
from iminuit import Minuit
from sklearn.externals import joblib

import newcalculate

#Set Default Minimisation values

defaultbdtcut = 0.9
defaultkcut = 0.0
defaultecut = 0.0
defaultmucut = 0.0


def run(Kmin=False, Emin=False, Mumin=False, text=False):
    
    #Constructs argument string based on argparse arguments
    
    argument = "bdt = " + str(defaultbdtcut) + ", limit_bdt = (0.0, 0.99), error_bdt=50.0" 
    if Kmin == True:
        argument += ", probk = " + str(defaultkcut) + ", limit_probk=(-10, 7.), error_probk=10.0"
    else:
        argument += ", probk = " + str(defaultkcut) + ", fix_probk=True"
    
    if Emin == True:
        argument += ", probe = " + str(defaultecut) + ", limit_probe=(-10, 6.), error_probe = 5.0"
    else:
        argument += ", probe = " + str(defaultecut) + ", fix_probe=True"
    
    if Mumin == True:
        argument += ", probmu = " + str(defaultmucut) + ", limit_probmu=(-10, 7.), error_probmu=10.0"
    else:
        argument += ", probmu=" + str(defaultmucut) + ", fix_probmu=True"
    
    argument += ", countoutput = False, fix_countoutput=True, text = " + str(text) + ", fix_text=True, graph = False, fix_graph = True, errordef = 10**-3"
    
    #Runs Minimisation and outputs results
    
    print time.asctime(time.localtime()), argument
    
    m = eval("Minuit(newcalculate.output," +  argument + ")")
    
    m.migrad()

    print m.print_param()
    print('fval', m.fval)
    
    message = str(time.asctime(time.localtime())) + " Finished minimisation with output "  + str(m.print_param())
    print message