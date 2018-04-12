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
    
channels, counts_50_50 = loadData('180403_data/50_50_task2_cal_602.mca')
energy = []
for i in channels:
    energy.append(0.01564856*i-0.07337194)
plt.figure()
plt.plot(energy[350:600],counts_50_50[350:600])
plt.xlabel('Energy [keV]')
plt.ylabel('Counts')
plt.title('Fe:Ni 50:50 counts vs. energy')
plt.legend(['Data'])

channels, counts_36_64 = loadData('180403_data/36_64_task2_cal_600.mca')
plt.figure()
energy = []
for i in channels:
    energy.append(0.01564856*i-0.07337194)
plt.plot(energy[350:600],counts_36_64[350:600])
plt.xlabel('Energy [keV]')
plt.ylabel('Counts')
plt.title('Fe:Ni 64:36 counts vs. energy')
plt.legend(['Data'])

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
    return popt

int_ratio = []

region_fe = [395,465]
#par_limits = ([1000,6,0],[1200,6.5,0.4])
#popt_fe = gaussFitPlot('180403_data/50_50_task2_cal_602.mca', region, par_limits)

region_ni = [465,500]
#par_limits = ([170,7.2,0],[200,7.6,0.4])
#popt_ni = gaussFitPlot('180403_data/50_50_task2_cal_602.mca', region, par_limits)

counts_50_50_fe = np.trapz(counts_50_50[region_fe[0]:region_fe[1]])
counts_50_50_ni = np.trapz(counts_50_50[region_ni[0]:region_ni[1]])
int_ratio.append(counts_50_50_ni / counts_50_50_fe)

region_fe = [395,465]
#par_limits = ([1200,6,0],[1500,6.5,0.4])
#popt_fe = gaussFitPlot('180403_data/36_64_task2_cal_600.mca', region, par_limits)

region_ni = [465,500]
#par_limits = ([120,7.2,0],[200,7.6,0.4])
#popt_ni = gaussFitPlot('180403_data/36_64_task2_cal_600.mca', region, par_limits)

counts_36_64_fe = np.trapz(counts_36_64[region_fe[0]:region_fe[1]])
counts_36_64_ni = np.trapz(counts_36_64[region_ni[0]:region_ni[1]])
int_ratio.append(counts_36_64_ni / counts_36_64_fe)

print('---------------------------------')
print('Intensity ratios for known matter ratios I_Ni/I_Fe:')
print(int_ratio)
print('---------------------------------')

matter_ratio = [50/50, 36/64]

def linFunc(x, a, b):
    return a*x+b

popt_lin, pcov = curve_fit(linFunc, matter_ratio, int_ratio)
print('Fitting parameters a and b')
print(popt_lin)
print('------------------------------')

plt.figure()
plt.plot(matter_ratio, int_ratio, 'r*')
plt.plot(np.arange(0, 1, 0.001), linFunc(np.arange(0, 1, 0.001),*popt_lin))
plt.xlabel(r'$\frac{I_{Ni}}{I_{Fe}}$')
plt.ylabel(r'$\frac{N_{Ni}}{N_{Fe}}$')

print('------------------------------')
print('Matter ratio for Black Rock:')
channels_blackrock, counts_blackrock = loadData('180403_data/blackrock_task2_600.mca')
region_fe = [400,470]
region_ni = [470,490]

counts_blackrock_fe = np.trapz(counts_blackrock[region_fe[0]:region_fe[1]])
counts_blackrock_ni = np.trapz(counts_blackrock[region_ni[0]:region_ni[1]])

int_ratio = counts_blackrock_ni/counts_blackrock_fe
matter_ratio = popt_lin[0]*int_ratio+popt_lin[1]
print(matter_ratio)


print('------------------------------')
print('Matter ratio for Shiny Rock')
channels_shiny, counts_shiny = loadData('180403_data/shiny_task2_600.mca')

counts_shiny_fe = np.trapz(counts_shiny[region_fe[0]:region_fe[1]])
counts_shiny_ni = np.trapz(counts_shiny[region_ni[0]:region_ni[1]])

int_ratio = counts_shiny_ni/counts_shiny_fe
matter_ratio = popt_lin[0]*int_ratio+popt_lin[1]
print(matter_ratio)

print('------------------------------')
print('Matter ratio for Smykkeskrin Rock')
channels_smykkeskrin, counts_smykkeskrin = loadData('180403_data/smykkeskrin_task2_600.mca')

counts_smykkeskrin_fe = np.trapz(counts_smykkeskrin[region_fe[0]:region_fe[1]])
counts_smykkeskrin_ni = np.trapz(counts_smykkeskrin[region_ni[0]:region_ni[1]])

int_ratio = counts_smykkeskrin_ni/counts_smykkeskrin_fe
matter_ratio = popt_lin[0]*int_ratio+popt_lin[1]
print(matter_ratio)