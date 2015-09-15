from uncertainties import ufloat
import math, time, ROOT

#Calculate the branching ratio using fixed LHCb variables and calculated variables
sigma2011 = ufloat(288, math.sqrt((4**2) + (48**2)))*(10**-6)
sigma2012 = ufloat(298, math.sqrt((2**2) + (36**2)))*(10**-6)
luminosity2011 = 10**15
luminosity2012 = 2* (10**15)
f = ufloat(0.401, 0.008)

def run(sigyield, entries, ffile, t, selection):
    
    c = ROOT.TCanvas()
    
    #Finds the change in weight before and after applying the selection
    t.SetBranchStatus("Weight", 1)

    PreData = ROOT.TH1D("PreData", "", 1000, -5, 50)
    PostData= ROOT.TH1D("PostData", "", 1000, -5, 50)

    t.Draw("Weight>>PreData")
    t.Draw("Weight>>PostData", selection)
    
    PreCount = t.GetEntries("B_BKGCAT==10")
    PreMean = PreData.GetMean()
    PreWeight = PreCount*PreMean
    
    PreData.Delete()
    
    PostCount = t.GetEntries(selection)
    PostMean = PostData.GetMean()
    PostWeight = PostCount * PostMean
    
    PostData.Delete()
    c.Close()

    eff = float(PostWeight/PreWeight)
    err = math.sqrt((eff) * (1.0-eff))/math.sqrt(PreCount)
    cutefficiency = ufloat(eff, err)
    
    #Calculates the Reconstruction Efficiency
    
    magDown = 512864
    magUp = 503578
    total = magUp + magDown
    
    fractionpassing = float(PreCount)/float(total)                                                          
    
    #Calculates the Mean Particle Cut Efficiency
    
    particlecutefficiency = ufloat(0.16954, 0.00064)
    antiparticlecutefficiency = ufloat(0.16864, 0.00064)
    meanparticleefficiency = 0.5 * (particlecutefficiency + antiparticlecutefficiency)
    
    efficiency = cutefficiency*meanparticleefficiency*fractionpassing
    
    #Calculates the consequent upper limit on branching ratio
    
    combined = (sigma2011*luminosity2011) + (sigma2012*luminosity2012)
    factor = 2 * f * combined * efficiency
    br = sigyield / factor
    
    print time.asctime(time.localtime()), "Branching Ratio would be", br
    print "eficiency is", cutefficiency
    return br.nominal_value, br.std_dev