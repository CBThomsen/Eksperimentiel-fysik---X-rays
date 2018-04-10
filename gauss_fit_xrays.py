import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


#Klassisk Gauss Funktion
def gaussFunc(x, a, x0,  sigma):
    return a*np.exp(-(x - x0)**2 / (2*sigma**2))

# Funktion der blot indlæser counts og channels fra mca-fil
def loadData(fileName):
    
    with open(fileName) as text:
    
        counts = []
        lister = text.readlines()
        begin = lister.index('<<DATA>>\n')+1
        end = lister.index('<<END>>\n')-1
        data = lister[begin:end]
        for i in data:
            counts.append(float(i)) 
        channels = range(0,len(data))
        
        return channels, counts

# par_limits er grænserne for fitteparametrene approksimeret fra plottet fra raw_data_plot
def gaussFitPlot(fileName, region, par_limits):
    
    channels, counts = loadData(fileName)
    channels = np.array(channels[region[0]:region[1]])
    counts = np.array(counts[region[0]:region[1]])

    popt, pcov = curve_fit(gaussFunc, channels, counts, bounds = par_limits)
    plt.figure()
    plt.plot(channels,counts)
    plt.plot(channels, gaussFunc(channels, *popt), 'r-')
    plt.xlabel('Channels')
    plt.ylabel('Counts')
    
      
par_limits = ([1500,800,5],[1700,1000,50])
region = [800,1000]
gaussFitPlot('180320_data/kali_am_600.mca',region, par_limits)

par_limits = ([40,3700,5],[80,3900,50])
region = [3700,3900]
gaussFitPlot('180320_data/kali_am_600.mca',region, par_limits)


