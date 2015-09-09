import ROOT, time, os, csv
import numpy as np
import calculate

filename = 'results.csv'

def process(source=filename, variable = "bdt", interval=0.1, lowerlim=0.7, upperlim=0.99, text=False):
    with open("sources/" + source, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([str(variable), 'ratio', 'error'])
        
        #Iterate over a range of BDT probabilities and signal counts, exporting results to a csv file
        
        vals = np.arange(float(lowerlim), float(upperlim), float(interval))
        
        for i in vals:
            value = i
            print time.asctime(time.localtime()), variable, "cut is", i
            ratio, error= eval("calculate.output(" + str(variable) + "= " + str(value) + ", countoutput=True, text=" + str(text) + ", dynamic=True)")
            data = [str(value), ratio, error]
            writer.writerow(data)
        pass

    #Produces an output message. Then sends an email notification.

    message = str(time.asctime(time.localtime())) + " Results saved in " + source
    print message

    import os, sys
    sys.path.append('/home/rstein/pythonscripts/misc')
    import sendemail as se
    name = os.path.basename(__file__)
    se.send(name, message)