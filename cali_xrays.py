# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 02:27:21 2018

@author: Peter Georgi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')

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

def gaussFit(fileName, region, par_limits):
    
    channels, counts = loadData(fileName)
    channels = np.array(channels[region[0]:region[1]])
    counts = np.array(counts[region[0]:region[1]])

    popt, pcov = curve_fit(Gaussfunc, channels, counts, bounds = par_limits)
    
    plt.figure()
    plt.plot(channels,counts)
    plt.plot(channels,gaussFunc(channels,popt[0],popt[1],popt[2]),'r-')
    
    return channels, counts, popt, pcov

# <extraherer relevante channelværdier for Am-241. Bedømmer at der er cirka 3
peak_channels = []
energies = []
std_error = []

par_limits = ([1500,800,5],[1700,1000,50])
region = [800,1000]
channels, counts, popt, pcov = gaussFit('180320_data/kali_am_600.mca', region, par_limits)
peak_channels.append(popt[1])

#tilhørende energi i keV
energies.append(13.94)
std_error.append(np.sqrt(np.diag(pcov)[1]))

par_limits = ([900,1100,5],[1100,1200,50])
region = [1100,1200]
channels, counts, popt, pcov = gaussFit('180320_data/kali_am_600.mca', region, par_limits)
peak_channels.append(popt[1])
energies.append(17.75)
std_error.append(np.sqrt(np.diag(pcov)[1]))

par_limits = ([40,3700,5],[80,3900,50])
region = [3700,3900]
channels, counts, popt, pcov = gaussFit('180320_data/kali_am_600.mca', region, par_limits)
peak_channels.append(popt[1])
energies.append(59.54)
std_error.append(np.sqrt(np.diag(pcov)[1]))

# Det samme for Fe-55
par_limits = ([17,350,2],[23,400,20])
region = [350,400]
channels, counts, popt, pcov = gaussFit('180320_data/kali_fe_900.mca', region, par_limits)
peak_channels.append(popt[1])
energies.append(5.9)
std_error.append(np.sqrt(np.diag(pcov)[1]))

#  Det samme for Cs-137
par_limits = ([5,1950,5],[17,2150,50])
region = [1950,2150]
channels, counts, popt, pcov = gaussFit('180320_data/kali_cs_600.mca', region, par_limits)
peak_channels.append(popt[1])
energies.append(32)
std_error.append(np.sqrt(np.diag(pcov)[1]))

plt.figure()
plt.errorbar(peak_channels,energies, xerr=np.array(std_error), yerr=0, fmt='r*')

# lineært fit
def linFunc(x, a, b):
    return a*x+b

popt, pcov = curve_fit(linFunc, peak_channels, energies)

channels = np.linspace(1,4000,1000)
plt.plot(channels,linFunc(channels,popt[0],popt[1]))
print(popt)
print(np.sqrt(np.diag(pcov)))

# Resultat E = 0.01564856*ch -0.07337194











