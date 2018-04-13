import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import interpolate

plt.close('all')

def plotatt(fileName, background, exp1, exp2, tyk, gaet, slope, edge):
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
    sigmacounts = np.sqrt(counts)
    sigmacountsabs = np.sqrt(countsabs)

    dt = tyk
    
    attenuation = np.array([])
    energy = np.array([])
    sigmaattenuation = np.array([])

    for i in channels:
        if countsabs[i] > 0 and counts[i] > 0:
            attenuation = np.append(attenuation, -np.log(countsabs[i]/(counts[i]*exp1/exp2))*1/dt)
            energy = np.append(energy, 0.01564856*channels[i]-0.07337194)
            sigmaattenuation = np.append(sigmaattenuation, np.sqrt((1/(dt*countsabs[i]))**2 * sigmacountsabs[i]**2 + (-1/(dt*counts[i]))**2 * sigmacounts[i]**2)) 

    rhoguess = gaet
    attguess = attenuation / rhoguess
    sigmaattguess = sigmaattenuation / rhoguess
    meverg = energy / 1000
    
    att = np.array([])
    satt = np.array([])
    mev = np.array([])
    
    for i in range(len(meverg)):
        if meverg[i] > 0.008 and meverg[i] < 0.030:
            att = np.append(att, attguess[i])
            satt = np.append(satt, sigmaattguess[i])
            mev = np.append(mev, meverg[i])
    
    print('Zero errors: ', np.where(satt == 0))
    print(len(satt))
    print(len(att))
    
    
#    spline = interpolate.interp1d(meverg, attguess, kind='cubic')
    x = np.linspace(mev[0], mev[len(mev)-1], 100000)

    tck = interpolate.splrep(mev, att, s=slope*len(mev))
    spline = interpolate.splev(x, tck)
    edgy = interpolate.splev(edge, tck)

    plt.figure()
    plt.errorbar(mev, att, yerr=satt, fmt='k.', label='Data', zorder=2)
    plt.show()
    plt.xlabel('Energy [MeV]')
    plt.ylabel('Attenuation coefficient [cm^2/g]')
    plt.yscale('log')
    plt.xscale('log')
    plt.plot(x, spline, 'r-', label='Fit', zorder=3)
    plt.plot(edge, edgy, 'bX', label='Edge Value', zorder=4)
#    plt.xlim([0.008, 0.029])
    plt.grid(zorder=1)
    plt.legend()
    plt.savefig('figurer/' + fileName[12:20] + '.pdf')
    plt.show()

plotatt('180403_data/abs1_600.mca', '180403_data/baggrund_600.mca', 600, 600, 0.0030, 11.34, 190, 0.01995)
plotatt('180403_data/abs2_900.mca', '180403_data/baggrund_600_2.mca', 900, 600, 0.0033, 10.49, 90, 0.02555)
plotatt('180403_data/abs3_900.mca', '180403_data/baggrund_600_2.mca', 900, 600, 0.0025, 19.3, 80, 0.01195)

    
