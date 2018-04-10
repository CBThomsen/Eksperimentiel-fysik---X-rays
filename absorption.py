import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')

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
    
channels, counts = loadData('180403_data/baggrund_600.mca')
channels = np.array(channels)
counts = np.array(counts)
channelsabs, countsabs = loadData('180403_data/abs3_900.mca')
channelsabs = np.array(channelsabs)
countsabs = np.array(countsabs)

dt = 0.0025

attenuation = np.array([])
energy = np.array([])

for i in channels:
    if countsabs[i] > 0 and counts[i] > 0:
        attenuation = np.append(attenuation, -np.log(countsabs[i]/(counts[i]*1.5))*1/dt)
        energy = np.append(energy, 0.01564856*channels[i]-0.07337194)

rhoguess = 8.96
attguess = attenuation / rhoguess
meverg = energy / 1000

def sixpol(x, a, b, c, d, e, f, g):
    return a*x**6 + b*x**5 + c*x**4 + d*x**3 + e*x**2 + f*x + g
boon = 2 * 10**9
poop, poov = curve_fit(sixpol, meverg, attenuation, bounds = ([-boon, -boon, -boon, 0, -boon, 0, -boon],[boon, 0, 0, boon, 0, boon, 0]))
print(poop)


plt.figure()
plt.plot(meverg, attenuation, '.')
plt.plot(meverg, sixpol(meverg, *poop), 'r-')
plt.xlabel('Energy [MeV]')
plt.ylabel('Attenuation coefficient [1/cm]')
plt.yscale('log')
plt.xscale('log')
plt.grid()
plt.show()


    
