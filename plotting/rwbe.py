import ROOT
import lhcbStyle as lhcb
import reweight as r
import rwmc

ROOT.gROOT.SetBatch(ROOT.kTRUE)
c=ROOT.TCanvas()
c.Divide(1,2)
lhcb.setLHCbStyle()

def plotsep(name, source, data, MC, bincount):
    import csv
    def rowcount():
        with open(source, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = sum(1 for row in reader)
            return count
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
            z = r.weight(variable, uplim, lowlim, data, MC, c, a, bincount)
            if i == 0:
                c.Print(name + str(bincount) + ".pdf(")
            elif i == lim:
                c.Print(name + str(bincount) + ".pdf)")
            else:
                c.Print(name + str(bincount) + ".pdf")
            i+=1
            del(a)
            a = z
            del(z)
