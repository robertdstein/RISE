import ROOT
import numpy as np

print "writing a tree"

f = ROOT.TFile("tree.root", "recreate")
t = ROOT.TTree("Tree1", "tree title")

n = np.zeros(1, dtype=float)
u = np.zeros(1, dtype=float)
g = np.zeros(1, dtype=float)

t.Branch('normal', n, 'normal/D')
t.Branch('uniform', u, 'uniform/D')
t.Branch('special', g, 'special/d')

for i in xrange(100000):
	n[0] = ROOT.gRandom.Gaus()
	u[0] = ROOT.gRandom.Uniform()
	g[0] = np.sin(np.random.rand())
	t.Fill()
		
f.Write()
f.Close()