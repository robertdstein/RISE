import ROOT, time, os, csv
import numpy as np
import argparse
import branchingratio as br
import fit as f
import simulate as s
from iminuit import Minuit
from sklearn.externals import joblib

import calculate

defaultbdtcut = 0.90
defaultkcut = -4.0
defaultecut = 4.0
defaultmucut = 2.0


def run(Kmin=False, Emin=False, Mumin=False, text=False):
    argument = "bdt = " + str(defaultbdtcut) + ", limit_bdt = (0.0, 0.99), error_bdt=0.1" 
    if Kmin == True:
        argument += ", probk = " + str(defaultkcut) + ", limit_probk=(-10, 7.), error_probk=0.1"
    else:
        argument += ", probk = " + str(defaultkcut) + ", fix_probk=True"
    
    if Emin == True:
        argument += ", probe = " + str(defaultecut) + ", limit_probe=(-10, 7.), error_probe = 0.1"
    else:
        argument += ", probe = " + str(defaultecut) + ", fix_probe=True"
    
    if Mumin == True:
        argument += ", probmu = " + str(defaultmucut) + ", limit_probmu=(-10, 7.), error_probmu=0.1"
    else:
        argument += ", probmu=" + str(defaultmucut) + ", fix_probmu=True"
    
    argument += ", countoutput = False, fix_countoutput=True, text = " + str(text) + ", fix_text=True, dynamic = False, fix_dynamic=True, errordef=(10**-9)"
    
    m = eval("Minuit(calculate.output," +  argument + ")")
    
    m.migrad()

    print m.print_param()
    print('fval', m.fval)
    
    message = str(time.asctime(time.localtime())) + " Finished minimisation with output "  + str(m.print_param()) + " and minimum Branching Ratio of " + m.fval()
    print message

    import os, sys
    sys.path.append('/home/rstein/pythonscripts/misc')
    import sendemail as se
    name = os.path.basename(__file__)
    se.send(name, message)
    
    joblib.dump(m, 'pickle/minimisation.pkl')