import ROOT, time, os, csv
import numpy as np
import newcalculate

filename = 'results'

#Iteratively test a range of values with fixed intervals for a given variable

def process(source=filename, variable = "bdt", interval=0.1, lowerlim=0.7, upperlim=0.99, text=False, random=False):
    with open("sources/" + source + ".csv", 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([str(variable), 'ratio', 'error'])
        
        #Iterate over a range of BDT probabilities and signal counts, exporting results to a csv file
        
        vals = np.arange(float(lowerlim), float(upperlim), float(interval))
        
        for i in vals:
            value = i
            print time.asctime(time.localtime()), variable, "cut is", i
            ratio, error= eval("newcalculate.output(" + str(variable) + "= " + str(value) + ", countoutput=True)")
            data = [str(value), ratio, error]
            writer.writerow(data)
        pass

    #Produces an output message

    message = str(time.asctime(time.localtime())) + " Results saved in " + source
    print message