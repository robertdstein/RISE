import ROOT, time, os, csv
import numpy as np
from scipy.optimize import minimize

import newcalculate as c

#Set Default Minimisation values [BDT, probk, probe, probmu]

x0 = [0.6, 0, 0, 0]

def run(x):
    print x
    c.output(bdt = x[0], probk = x[1], probe = x[2], probmu = x[3], text=False, countoutput=False, graph = False)
         
res = minimize(run, x0,  method='Nelder-Mead')

message = str(time.asctime(time.localtime())) + " Finished minimisation with output" + res.x
print message
    
#Sends an email notification on completion     
    
import os, sys
sys.path.append('/home/rstein/pythonscripts/misc')
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message)