import ROOT, time, os, csv
import numpy as np
import argparse
import branchingratio as br
import fit as f
import simulate as s
from iminuit import Minuit
from sklearn.externals import joblib

import calculate

def run(Kmin=False, Emin=False, Mumin=False, defaultcut = 0.2):
    argument = "bdt = 0.5, limit_bdt = (0.0, 0.99), error_bdt=0.1" 
    if Kmin == True:
        argument += ", probk = " + str(defaultcut) + ", limit_probk=(0,1.), error_probk=0.1,"
    else:
        argument += ", probk=" + str(defaultcut) + ", fix_probk=True"
    
    if Emin == True:
        argument += ", probe = " + str(defaultcut) + ", limit_probe=(0,1.), error_probe = 0.1"
    else:
        argument += ", probe=" + str(defaultcut) + ", fix_probe=True"
    
    if Mumin == True:
        argument += ", probmu = " + str(defaultcut) + ", limit_probmu=(0,1.), error_probmu=0.1"
    else:
        argument += ", probmu=" + str(defaultcut) + ", fix_probmu=True"
    
    argument += ", countoutput = False, fix_countoutput=True, errordef=(10**-9)"
    
    m = eval("Minuit(calculate.output," +  argument + ")")
    
    print m.print_param()  
    
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