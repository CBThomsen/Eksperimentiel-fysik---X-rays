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

def doLinFit(plot=False):
    channels, counts_50_50 = loadData('180403_data/50_50_task2_cal_602.mca')
    energy = []

    channels, counts_36_64 = loadData('180403_data/36_64_task2_cal_600.mca')
    energy = []
    
    for i in channels:
        energy.append(0.01564856*i-0.07337194)
    
    
    if(plot == True):
        plt.figure()
    
        plt.figure()
        plt.plot(energy[350:600],counts_50_50[350:600])
        plt.xlabel('Energy [keV]')
        plt.ylabel('Counts')
        plt.title('Fe:Ni 50:50 counts vs. energy')
        plt.legend(['Data'])
                
        plt.plot(energy[350:600],counts_36_64[350:600])
        plt.xlabel('Energy [keV]')
        plt.ylabel('Counts')
        plt.title('Fe:Ni 64:36 counts vs. energy')
        plt.legend(['Data'])
        
    
    measured_ratio = []
    
    region_fe = [395,465]
    region_ni = [465,500]
    region_small_ni = [521, 545]
    counts_50_50_fe = np.trapz(counts_50_50[region_fe[0]:region_fe[1]])
    counts_50_50_ni = np.trapz(counts_50_50[region_ni[0]:region_ni[1]])
    #counts_50_50_ni += np.trapz(counts_50_50[region_small_ni[0]:region_small_ni[1]])
    measured_ratio.append(counts_50_50_ni / counts_50_50_fe)
    
    region_fe = [395,465]
    region_ni = [465,500]
    
    counts_36_64_fe = np.trapz(counts_36_64[region_fe[0]:region_fe[1]])
    counts_36_64_ni = np.trapz(counts_36_64[region_ni[0]:region_ni[1]])
    #counts_36_64_ni += np.trapz(counts_36_64[region_small_ni[0]:region_small_ni[1]])
    measured_ratio.append(counts_36_64_ni / counts_36_64_fe)
    
    print('---------------------------------')
    print('Intensity ratios for known matter ratios I_Ni/I_Fe:')
    print(measured_ratio)
    print('---------------------------------')
    
    actual_ratio = [50/50, 36/64]
    
    def linFunc(x, a):
        return a*x
    
    popt_lin, pcov = curve_fit(linFunc, measured_ratio, actual_ratio)
    print('Fitting parameters a and b')
    print(popt_lin)
    print("Uncertainity: ", np.sqrt(np.diag(pcov)))
    print('------------------------------')
    
    if(plot == True):
        plt.figure()
        plt.plot(measured_ratio, actual_ratio, 'r*')
        plt.plot(np.arange(0, 0.3, 0.001), linFunc(np.arange(0, 0.3, 0.001),*popt_lin))
        plt.xlabel(r'$ratio_{measured}$')
        plt.ylabel(r'$ratio_{actual}$')
        plt.title('Calibration of Ni/Fe ratios')
        
    return popt_lin, pcov

# par_limits er grænserne for fitteparametrene approksimeret fra plottet fra raw_data_plot
def gaussFitPlot(fileName, region, par_limits):
    
    energy = []
    channels, counts = loadData(fileName)
    channels = np.array(channels[region[0]:region[1]])
    counts = np.array(counts[region[0]:region[1]])
    for i in channels:
        energy.append(0.01564856*i-0.07337194)

    popt, pcov = curve_fit(gaussFunc, energy, counts, bounds = par_limits)
    plt.figure()
    plt.plot(energy,counts)
    plt.plot(energy, gaussFunc(energy, *popt), 'r-')
    plt.xlabel('Energy [keV]')
    plt.ylabel('Counts')
    return popt, pcov

def doAnalysis():
    popt_lin, pcov_lin = doLinFit(True)
    a = popt_lin[0]
    a_error = np.sqrt(np.diag(pcov_lin))[0]
    
    print('------------------------------')
    print('Matter ratio for Black Rock:')
    channels_blackrock, counts_blackrock = loadData('180403_data/blackrock_task2_600.mca')
    region_fe = [400,470]
    region_ni = [470,500]
    region_small_ni = [521, 545] #Small peak at 8.264 keV
    
    counts_blackrock_fe = np.trapz(counts_blackrock[region_fe[0]:region_fe[1]])
    counts_blackrock_ni = np.trapz(counts_blackrock[region_ni[0]:region_ni[1]])
    counts_error_fe = np.sqrt(counts_blackrock_fe)
    counts_error_ni = np.sqrt(counts_blackrock_ni)
    #counts_blackrock_ni += np.trapz(counts_blackrock[region_small_ni[0]:region_small_ni[1]])
    
    measured_ratio = counts_blackrock_ni/counts_blackrock_fe
    measured_ratio_err = np.sqrt((1/ counts_blackrock_fe * counts_error_ni)**2 + (-counts_blackrock_ni/counts_blackrock_fe**2 * counts_error_fe)**2)
    actual_ratio = popt_lin[0] * measured_ratio
    actual_ratio_err = np.sqrt((counts_blackrock_ni / counts_blackrock_fe * a_error)**2+ (a * 1/ counts_blackrock_fe * counts_error_ni)**2 + (- a * counts_blackrock_ni/counts_blackrock_fe**2 * counts_error_fe)**2)
    pct_err = np.sqrt((1 / (1+actual_ratio) * actual_ratio_err)**2)

    print("Measured ratio", measured_ratio, "error", measured_ratio_err)
    print("Actual ratio", actual_ratio, "error", actual_ratio_err)
    print("Pct ni", actual_ratio / (actual_ratio + 1) * 100, "pct Fe", 1 / (actual_ratio + 1) * 100)
    print("Pct err", pct_err*100)
    
    print('------------------------------')
    print('Matter ratio for Shiny Rock')
    channels_shiny, counts_shiny = loadData('180403_data/shiny_task2_600.mca')
    
    counts_shiny_fe = np.trapz(counts_shiny[region_fe[0]:region_fe[1]])
    counts_shiny_ni = np.trapz(counts_shiny[region_ni[0]:region_ni[1]])
    counts_error_fe = np.sqrt(counts_shiny_fe)
    counts_error_ni = np.sqrt(counts_shiny_ni)
    #counts_shiny_ni += np.trapz(counts_shiny[region_small_ni[0]:region_small_ni[1]])
    
    measured_ratio = counts_shiny_ni/counts_shiny_fe
    measured_ratio_err = np.sqrt((1/ counts_shiny_fe * counts_error_ni)**2 + (counts_shiny_ni/counts_shiny_fe**2 * counts_error_fe)**2)
    actual_ratio = popt_lin[0]*measured_ratio
    actual_ratio_err = np.sqrt((counts_shiny_ni / counts_shiny_fe * a_error)**2 + (a * 1/ counts_shiny_fe * counts_error_ni)**2 + (- a * counts_shiny_ni/counts_shiny_fe**2 * counts_error_fe)**2)    
    pct_err = np.sqrt((1 / (1+actual_ratio) * actual_ratio_err)**2)
    
    print("Measured ratio", measured_ratio, "error", measured_ratio_err)
    print("Actual ratio", actual_ratio, "error", actual_ratio_err)
    print("Pct ni", actual_ratio / (actual_ratio + 1) * 100, "pct Fe", 1 / (actual_ratio + 1) * 100)
    print("Pct err", pct_err * 100)
    
    print('------------------------------')
    print('Matter ratio for Spotted Rock')
    channels_smykkeskrin, counts_smykkeskrin = loadData('180403_data/smykkeskrin_task2_600.mca')
    
    counts_smykkeskrin_fe = np.trapz(counts_smykkeskrin[region_fe[0]:region_fe[1]])
    counts_smykkeskrin_ni = np.trapz(counts_smykkeskrin[region_ni[0]:region_ni[1]])
    counts_error_fe = np.sqrt(counts_smykkeskrin_fe)
    counts_error_ni = np.sqrt(counts_smykkeskrin_ni)
    #counts_smykkeskrin_ni += np.trapz(counts_smykkeskrin[region_small_ni[0]:region_small_ni[1]])
    
    measured_ratio = counts_smykkeskrin_ni/counts_smykkeskrin_fe
    measured_ratio_err = np.sqrt((1/ counts_smykkeskrin_fe * counts_error_ni)**2 + (-counts_smykkeskrin_ni/counts_smykkeskrin_fe**2 * counts_error_fe)**2)
    actual_ratio = popt_lin[0]*measured_ratio
    actual_ratio_err = np.sqrt((counts_smykkeskrin_ni / counts_smykkeskrin_fe * a_error)**2 + (a * 1/ counts_smykkeskrin_fe * counts_error_ni)**2 + (- a * counts_smykkeskrin_ni/counts_smykkeskrin_fe**2 * counts_error_fe)**2)
    pct_err = np.sqrt((1 / (1+actual_ratio) * actual_ratio_err)**2)
    
    print("Measured ratio", measured_ratio, "error", measured_ratio_err)
    print("Actual ratio", actual_ratio, "error", actual_ratio_err)
    print("Pct ni", actual_ratio / (actual_ratio + 1) * 100, "pct Fe", 1 / (actual_ratio + 1) * 100)
    print("Pct err", pct_err * 100)
    
    start = 350
    end = 550
    energy = np.arange(0, len(channels_blackrock), 1) * 0.01564856 - 0.07337194
    energy = energy[start:end]
    
    plt.figure()
    plt.title('Spectrum of the 3 meteorites')
    plt.plot(energy, counts_blackrock[start:end], label='Black rock')
    plt.plot(energy, counts_shiny[start:end], label='Shiny rock')
    plt.plot(energy, counts_smykkeskrin[start:end], label='Spotted rock')
    plt.ylabel('Counts')
    plt.xlabel('Energy [keV]')
    plt.legend()
    #plt.save('figurer/meteorite_spectrums.pdf')

doAnalysis()
plt.show()