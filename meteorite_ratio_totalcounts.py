import numpy as np
import matplotlib.pyplot as plt
from meteorite_ratio import loadData
from scipy.optimize import curve_fit

def linCalFit(plot=False):
    channels, counts_50_50 = loadData('180403_data/50_50_task2_cal_602.mca')
    channels, counts_36_64 = loadData('180403_data/36_64_task2_cal_600.mca')
    
    energy = []
    for i in channels:
        energy.append(0.01564856*i-0.07337194)
        
    #Getting counts
    region_fe = [395,465]
    region_ni = [465,500]
    
    total_counts_50_50 = np.trapz(counts_50_50[region_fe[0]:region_ni[1]])
    total_counts_36_64 = np.trapz(counts_36_64[region_fe[0]:region_ni[1]])
    
    counts_50_50_fe = np.trapz(counts_50_50[region_fe[0]:region_fe[1]])
    counts_50_50_ni = np.trapz(counts_50_50[region_ni[0]:region_ni[1]])
    
    counts_36_64_fe = np.trapz(counts_36_64[region_fe[0]:region_fe[1]])
    counts_36_64_ni = np.trapz(counts_36_64[region_ni[0]:region_ni[1]])
    
    int_ratio_fe = []
    int_ratio_fe.append(counts_50_50_fe / total_counts_50_50)
    int_ratio_fe.append(counts_36_64_fe / total_counts_36_64)
    
    int_ratio_ni = []
    int_ratio_ni.append(counts_36_64_ni / total_counts_36_64)
    int_ratio_ni.append(counts_50_50_ni / total_counts_50_50)
    
    #Fitting part
    def linFunc(x, a, b):
        return a*x+b
    
    matter_ratio_fe = [0.5, 0.64]
    matter_ratio_ni = [0.36, 0.5]
    popt_lin_fe, pcov_fe = curve_fit(linFunc, matter_ratio_fe, int_ratio_fe)
    popt_lin_ni, pcov_ni = curve_fit(linFunc, matter_ratio_ni, int_ratio_ni)
    
    print(popt_lin_fe, popt_lin_ni)
   
    if(plot == True):
        plt.figure()
        plt.plot(matter_ratio_fe, int_ratio_fe, 'r*', label='Fe data')
        plt.plot(np.arange(0, 1, 0.001), linFunc(np.arange(0, 1, 0.001),*popt_lin_fe), label='Fe fit')
        
        plt.plot(matter_ratio_ni, int_ratio_ni, 'r*', label='Ni data')
        plt.plot(np.arange(0, 1, 0.001), linFunc(np.linspace(0, 1, 1000),*popt_lin_ni), label='Ni fit')
        
        plt.xlabel(r'$\frac{I}{I_{total}}$')
        plt.ylabel(r'$\frac{N}{N_{total}}$')
        
        total =  linFunc(np.arange(0, 1, 0.001),*popt_lin_fe) + (linFunc(np.linspace(1, 0, 1000),*popt_lin_ni))
        plt.plot(np.arange(0, 1, 0.001), total, label='Total')
    
        
        plt.legend()
    
    
    
    
linCalFit(True)
plt.show()
    
    
    
    