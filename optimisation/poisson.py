# -*- coding: utf-8 -*-
#//
#// limits.C - function to get simple poissonian (upper) limits
#//
#// Author:  Maximilian Schlupp
#// E-Mail:  max.schlupp@cern.ch
#// Date: 		2014-05-30

import ROOT
import math

#return expected upper 95% limit. 
def getExpectedLimit(bkg):
    nobs = int(0)
    nsum = 0.
    doWhile = True
    while doWhile:
        nobs += 1
        if (ROOT.TMath.Poisson(nobs-1,bkg) < 1e-06) & (nobs-1 < bkg):
            pass
	if(ROOT.TMath.Poisson(nobs-1,bkg) < 1e-06) & (nobs-1 > bkg):
	    doWhile = False
	add = ROOT.TMath.Poisson(nobs-1,bkg) * getUpperLimitPoisson(bkg, nobs-1)
	nsum += add 
    return nsum

#// get upper 95% limit on s, if nObs is observed. calculate limit for µ=s+b and subtrack b.
#// how TMath::ChisquareQuantile works, have a look into the PDG, eg booklet 2008, §32.3.2.5 p. 270
#// or download full statistics review on PDG homepage
def getUpperLimitPoisson(bkg, nObs):
    limit  = 0.5*ROOT.TMath.ChisquareQuantile(0.999999426697,2*(nObs+1))
    return limit-bkg

#// return median of the distribution of the expected limits calculated from variations of the background
def getPoissonLimit(bkg, bkgErr, tries = 10000, bins = 100):
    rnd = ROOT.TRandom3()
    nTries= int(tries)
    #// define variable histo boundaries
    expLim = getExpectedLimit(bkg)
    low	= int(expLim-5* math.sqrt(expLim))
    if (expLim>1.5):
        up = int(expLim+5*math.sqrt(expLim))
    else:
        up = 8 
    nbins = int(bins)
    dist= ROOT.TH1D("h","h",nbins,low,up)
    #std::vector<double> v
    while(nTries):
        #//cout << rnd->Poisson(bkg) << endl;
	#// randomize bkg according to uncertainty - the easiest way
        #if number of background events is drawn as < 0: b = 0 
        b= rnd.Gaus(bkg,bkgErr)
        if(b<0):
            b = 0
        expLim = getExpectedLimit(b)
        dist.Fill(expLim)
        nTries += -1
    dist.Draw()
    lim = median1(dist)
    print "expected limit as median of distribution (histo): ", lim
    return lim


#// external C macro, from a statistics school 2013, as crosscheck. 
def GetExpectedLimit(cl,b):
    #/* calculate the expected signal limit, given the confidence level
    #and the background b. Note: does not work for very large b */
    n0=int(b)
    n1=n0+1
    p0=1.0
    if(b > 0.0):
        p0= ROOT.TMath.Exp(n0*ROOT.TMath.Log(b)-b-ROOT.TMath.LnGamma(n0+1.))
    p1= p0 * b/n1
    nsum = 0.0
    #// sum up poisson terms from n0 to infinity
    #//  (stop as the contribution vanishes)
    while((p0 > 0.) & (n0 >= 0)):
        muLimit= 0.5 * ROOT.TMath.ChisquareQuantile(cl,2*(n0+1))
        signal= muLimit-b
        nsum += p0*signal
        p0 = p0 *n0/b
        n0 += -1
    #// sum up poisson terms from n1 down to zero
    #//  (stop earlier if the contribution vanishes)x
    while(p1>0.0):
        muLimit=0.5*ROOT.TMath.ChisquareQuantile(cl,2*(n1+1))
        signal=muLimit-b
        nsum += p1*signal
        n1 += 1
        p1 *= b/n1
    print "Given the background b=", b, "the expected limit on the signal is ", nsum
    return nsum
    
#// helper function.
def median1(h1):
    #//compute the median for 1-d histogram h1
    xaxis = h1.GetXaxis()
    nbins = xaxis.GetNbins()
    x = nbins
    y = nbins
    for i in range (1, nbins):
        xaxis = h1.GetXaxis()
        x[i] = xaxis.GetBinCenter(i)
        y[i]= h1.GetBinContent(i)
    median = ROOT.TMath.Median(nbins,x,y)
    return median