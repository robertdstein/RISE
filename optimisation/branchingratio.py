from uncertainties import ufloat
import math, time

sigma2011 = ufloat(288, math.sqrt((4**2) + (48**2)))*(10**-6)
sigma2012 = ufloat(298, math.sqrt((2**2) + (36**2)))*(10**-6)
luminosity2011 = 10**15
luminosity2012 = 2* (10**15)
f = ufloat(0.401, 0.008)

def run(sigyield, efficiency):
    
    #Calculate the branching ratio using fixed LHCb variables and calculated variables
    
    combined = (sigma2011*luminosity2011) + (sigma2012*luminosity2012)
    factor = 2 * f * combined * efficiency
    br = sigyield / factor
    
    print time.asctime(time.localtime()), "Branching Ratio would be", br
    return br.nominal_value, br.std_dev