# -*- coding: utf-8 -*-
#//
#// limits.C - function to get simple poissonian (upper) limits
#//
#// Author:  Maximilian Schlupp
#// E-Mail:  max.schlupp@cern.ch
#// Date: 		2014-05-30

import ROOT
import math

#return expected upper percentage% limit. 
def getExpectedLimit(bkg, percentage):
    nobs = int(0)
    nsum = 0.
    doWhile = True
    while doWhile:
        nobs += 1
        if (ROOT.TMath.Poisson(nobs-1,bkg) < 1e-06) & (nobs-1 < bkg):
            pass
	if(ROOT.TMath.Poisson(nobs-1,bkg) < 1e-06) & (nobs-1 > bkg):
	    doWhile = False
	add = ROOT.TMath.Poisson(nobs-1,bkg) * getUpperLimitPoisson(bkg, nobs-1, percentage)
	nsum += add 
    return nsum

#// get upper 95% limit on s, if nObs is observed. calculate limit for µ=s+b and subtrack b.
#// how TMath::ChisquareQuantile works, have a look into the PDG, eg booklet 2008, §32.3.2.5 p. 270
#// or download full statistics review on PDG homepage
def getUpperLimitPoisson(bkg, nObs, percentage):
    limit  = 0.5*ROOT.TMath.ChisquareQuantile(percentage,2*(nObs+1))
    return limit-bkg