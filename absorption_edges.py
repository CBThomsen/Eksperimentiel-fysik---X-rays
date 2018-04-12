import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.close('all')

def plotatt(fileName, background, ratio):
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

    
    attenuation = np.array([])
    energy = np.array([])

    diff_count = counts*ratio-countsabs
    energy = np.append(energy, 0.01564856*channels-0.07337194)
    # i keV

    plt.figure()
    plt.plot(energy, diff_count, '-')
    plt.xlabel('Energy [keV]')
    plt.ylabel('dI')
#    plt.yscale('log')
#    plt.xscale('log')
    plt.xlim([9, 40])
    plt.ylim([-10,60])
    plt.grid()
    plt.show()

plotatt('180403_data/abs1_600.mca', '180403_data/baggrund_600.mca',1)
plotatt('180403_data/abs2_900.mca', '180403_data/baggrund_600_2.mca',1.5)
plotatt('180403_data/abs3_900.mca', '180403_data/baggrund_600_2.mca',1.5)

    
