import ROOT
import lhcbStyle as lhcb
import plotfunctions as pf

ROOT.gROOT.SetBatch(ROOT.kTRUE)
c=ROOT.TCanvas()
lhcb.setLHCbStyle()

#Creates plots of the seperation between MC and Data

def plotsep(name, source, data, datatree, MC, MCtree, weighting=False):
    import csv
    def rowcount():
        with open(source, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = sum(1 for row in reader)
            return count
    #Extracts the Variables and ranges from a CSV file, and creates a PDF-page plot for each
    with open(source, 'rb') as csvfile:
        i = 0
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            x = row
            lim = rowcount() - 1
            variable = x[0]
            print variable
            uplim = float(x[1])
            lowlim = float(x[2])
            pf.output(variable, uplim, lowlim, data, datatree, MC, MCtree, weighting)
            if i == 0:
                c.Print("output/" + name + ".pdf(")
            elif i == lim:
                c.Print("output/" + name + ".pdf)")
            else:
                c.Print("output/" + name + ".pdf")
            i+=1