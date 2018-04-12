import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')

def plotatt(fileName, background, exp1, exp2, tyk, gaet):
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
    
    channels, counts = loadData(background)
    channels = np.array(channels)
    counts = np.array(counts)
    channelsabs, countsabs = loadData(fileName)
    channelsabs = np.array(channelsabs)
    countsabs = np.array(countsabs)

    dt = tyk
    
    attenuation = np.array([])
    energy = np.array([])

    for i in channels:
        if countsabs[i] > 0 and counts[i] > 0:
            attenuation = np.append(attenuation, -np.log(countsabs[i]/(counts[i]*exp1/exp2))*1/dt)
            energy = np.append(energy, 0.01564856*channels[i]-0.07337194)

    rhoguess = gaet
    attguess = attenuation / rhoguess
    meverg = energy / 1000

    plt.figure()
    plt.plot(meverg, attguess, '-')
    plt.xlabel('Energy [MeV]')
    plt.ylabel('Attenuation coefficient [cm^2/g]')
    plt.yscale('log')
    plt.xscale('log')
#    plt.xlim([0.008, 0.029])
    plt.grid()
    plt.show()

plotatt('180403_data/abs1_600.mca', '180403_data/baggrund_600.mca', 600, 600, 0.0030, 11.34)
plotatt('180403_data/abs2_900.mca', '180403_data/baggrund_600_2.mca', 900, 600, 0.0033, 10.49)
plotatt('180403_data/abs3_900.mca', '180403_data/baggrund_600_2.mca', 900, 600, 0.0025, 19.3)

    
