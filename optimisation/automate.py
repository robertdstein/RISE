import ROOT, time, os, csv
import numpy as np
import calculate

print time.asctime(time.localtime()), "Starting Code"

def process(source= 'results.csv', interval=0.1, lowerlim=0.7, upperlim=0.99):
    with open(source, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['bdt', 'ratio', 'error'])
        
        bdtvals = np.arange(float(lowerlim), float(upperlim), float(interval))
        
        #Iterate over a range of BDT probabilities and signal counts, exporting results to a csv file
        
        for i in bdtvals:
            bdt = i
            print time.asctime(time.localtime()), "BDT cut is", i
            ratio, error= calculate.output(bdt, countoutput=True)
            data = [bdt, ratio, error]
            writer.writerow(data)

    #Produces an output message with the duplicate number. Then sends an email notification.

    message = str(time.asctime(time.localtime())) + " Results saved in " + filename
    print message

    import os, sys
    sys.path.append('/home/rstein/pythonscripts/misc')
    import sendemail as se
    name = os.path.basename(__file__)
    se.send(name, message)