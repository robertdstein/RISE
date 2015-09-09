from uncertainties import ufloat
import math, time, ROOT

sigma2011 = ufloat(288, math.sqrt((4**2) + (48**2)))*(10**-6)
sigma2012 = ufloat(298, math.sqrt((2**2) + (36**2)))*(10**-6)
luminosity2011 = 10**15
luminosity2012 = 2* (10**15)
f = ufloat(0.401, 0.008)

def run(sigyield, entries, ffile, t, selection):
    
    #Calculate the branching ratio using fixed LHCb variables and calculated variables
    t.SetBranchStatus("Weight", 1)

    PreData = ROOT.TH1D("PreData", "", 1000, -5, 50)
    PostData= ROOT.TH1D("PostData", "", 1000, -5, 50)

    t.Draw("Weight>>PreData")
    t.Draw("Weight>>PostData", selection)
    
    PreCount = t.GetEntries("B_BKGCAT==10")
    PreMean = PreData.GetMean()
    PreWeight = PreCount*PreMean
    
    PostCount = t.GetEntries(selection)
    PostMean = PostData.GetMean()
    PostWeight = PostCount * PostMean

    eff = float(PostWeight/PreWeight)
    err = math.sqrt((eff) * (1.0-eff))/math.sqrt(PreCount)
    cutefficiency = ufloat(eff, err)
    
    print time.asctime(time.localtime()), "Cut Efficiency would be", cutefficiency
    
    magDown = 512864
    magUp = 503578
    total = magUp + magDown
    
    fractionpassing = float(PreCount)/float(total)
    
    print time.asctime(time.localtime()), "Reconstruction Efficiency is", fractionpassing
                         
    particlecutefficiency = ufloat(0.16954, 0.00064)
    antiparticlecutefficiency = ufloat(0.16864, 0.00064)
    meanparticleefficiency = 0.5 * (particlecutefficiency + antiparticlecutefficiency)
    
    efficiency = cutefficiency*meanparticleefficiency*fractionpassing
    
    combined = (sigma2011*luminosity2011) + (sigma2012*luminosity2012)
    factor = 2 * f * combined * efficiency
    br = sigyield / factor
    
    print time.asctime(time.localtime()), "Branching Ratio would be", br
    return br.nominal_value, br.std_dev