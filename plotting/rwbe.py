import ROOT
import lhcbStyle as lhcb
import plotreweightinghistogram as r

ROOT.gROOT.SetBatch(ROOT.kTRUE)
c=ROOT.TCanvas()
c.Divide(1,2)
lhcb.setLHCbStyle()

#Creates plots of the seperation between reweighted MC and S-Weighted data

def plotsep(name, source, data, MC, bincount, weighting=False):
    import csv
    def rowcount():
        with open(source, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = sum(1 for row in reader)
            return count
    #Extracts the two Variables and ranges from a CSV file, and creates a PDF-page plot for each
    with open(source, 'rb') as csvfile:
        i = 0
        a = None
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            x = row
            lim = rowcount() - 1
            variable = x[0]
            uplim = float(x[1])
            lowlim = float(x[2])
            z = r.plot(variable, uplim, lowlim, data, MC, c, bincount, weighting)
            if i == 0:
                c.Print("output/" + name + "_" + str(bincount) + "1d_reweighted.pdf(")
            elif i == lim:
                c.Print("output/" + name + "_" + str(bincount) + "1d_reweighted.pdf)")
            else:
                c.Print("output/" + name + "_" + str(bincount) + "1d_reweighted.pdf")
            i+=1
            del(a)
            a = z
            del(z)
