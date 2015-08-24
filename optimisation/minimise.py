import ROOT, time, os, csv
import numpy as np
import argparse
import branchingratio as br
import fit as f
import simulate as s
from iminuit import Minuit

import calculate

m = Minuit(calculate.output, bdt = 0.8, limit_bdt = (0.0, 0.999), error_bdt=0.1, probk = 0.2, limit_probk=(0,1.), error_probk=0.1, probe = 0.2, limit_probe=(0,1.), error_probe = 0.1, probmu = 0.2, limit_probmu=(0,1.), error_probmu=0.1)
m.migrad()

print m.print_param()

message = str(time.asctime(time.localtime())) + " Finished minimisation with output "  + str(m.print_param())
print message

import os, sys
sys.path.append('/home/rstein/pythonscripts/misc')
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message)