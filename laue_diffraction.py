import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')

#constants
h = 4.135667662*10**(-18)
#keV*s
c = 299792458
#m/s
theta = 45*np.pi/180

def gaussFunc(x, a, x0,  sigma):
    return a*np.exp(-(x - x0)**2 / (2*sigma**2))

def linFunc(x, a, b):
    return a*x+b
    
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
            channels = np.array(channels)
            counts = np.array(counts)
            
            return channels, counts
        
def laueDiffFit(fileName, peak_width, peaks_x):
    
    peak_channels = np.array([])
    channels, counts = loadData(fileName)
    for i in peaks_x:
        par_limits = ([0,i-peak_width,0] ,[1200, i+peak_width , 10])
        peak_interval = [(channels[i]-peak_width),(channels[i]+peak_width)]
        x = channels[peak_interval[0]:peak_interval[1]]
        y = counts[peak_interval[0]:peak_interval[1]]
        popt, pcov = curve_fit(gaussFunc, x, y, bounds = par_limits)
        plt.plot(x, y, 'b.')
        plt.plot(x, gaussFunc(x, *popt))
        peak_channels = np.append(peak_channels,popt[1])
    
    peak_energies = 0.01564856*peak_channels-0.07337194
    lambdas = h*c/peak_energies
    # keV
    n = range(10,10+len(peak_energies))
    d = np.array([])
    
    for i in range(len(n)):
        d = np.append(d,n[i]*lambdas[i]/(2*np.sin(theta)))
    
    return lambdas, d

lambdas, d = laueDiffFit('180410_data/glimmer_1800.mca', 25, [412, 453, 514, 566, 622, 677, 735])
ratio = lambdas[0:6]/lambdas[1:7]
avg_ratio = sum(ratio)/6
print(ratio)
print(avg_ratio)
print(d)
print(d[0]-d[len(d)-1])
        






