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
    
channels, counts = loadData('180403_data/50_50_task2_cal_602.mca')
energy = []
for i in channels:
    energy.append(0.01564856*i-0.07337194)
plt.figure()
plt.plot(energy[350:600],counts[350:600])
plt.xlabel('Energy [keV]')
plt.ylabel('Counts')
plt.title('Fe:Ni 50:50 counts vs. energy')
plt.legend(['Data'])

channels, counts = loadData('180403_data/36_64_task2_cal_600.mca')
plt.figure()
energy = []
for i in channels:
    energy.append(0.01564856*i-0.07337194)
plt.plot(energy[350:600],counts[350:600])
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

region = [390,430]
par_limits = ([1000,6,0],[1200,6.5,0.4])
popt_fe = gaussFitPlot('180403_data/50_50_task2_cal_602.mca', region, par_limits)

region = [460,500]
par_limits = ([170,7.2,0],[200,7.6,0.4])
popt_ni = gaussFitPlot('180403_data/50_50_task2_cal_602.mca', region, par_limits)

int_ratio.append(popt_ni[0]/popt_fe[0])

region = [390,430]
par_limits = ([1200,6,0],[1500,6.5,0.4])
popt_fe = gaussFitPlot('180403_data/36_64_task2_cal_600.mca', region, par_limits)

region = [460,500]
par_limits = ([120,7.2,0],[200,7.6,0.4])
popt_ni = gaussFitPlot('180403_data/36_64_task2_cal_600.mca', region, par_limits)

int_ratio.append(popt_ni[0]/popt_fe[0])

print('---------------------------------')
print('Intensity ratios for known matter ratios I_Ni/I_Fe:')
print(int_ratio)
print('---------------------------------')

matter_ratio = [50/50, 34/36]

def linFunc(x, a, b):
    return a*x+b

popt, pcov = curve_fit(linFunc, int_ratio, matter_ratio)
print('Fitting parameters a and b')
print(popt)
print('------------------------------')

plt.figure()
plt.plot(int_ratio, matter_ratio, 'r*')
plt.plot(np.linspace(0,0.4,100), linFunc(np.linspace(0,0.4,100),*popt))
plt.xlabel(r'$\frac{I_{Ni}}{I_{Fe}}$')
plt.ylabel(r'$\frac{N_{Ni}}{N_{Fe}}$')

# Resultatet er matter_ratio = 0.84625081*int_ratio+0.84800939

region = [390,430]
par_limits = ([600,6,0],[800,6.5,0.4])
popt_fe = gaussFitPlot('180403_data/blackrock_task2_600.mca', region, par_limits)

region = [465,500]
par_limits = ([3,7.4,0],[10,7.6,0.4])
popt_ni = gaussFitPlot('180403_data/blackrock_task2_600.mca', region, par_limits)

int_ratio = popt_ni[0]/popt_fe[0]
matter_ratio = 0.84625081*int_ratio+0.84800939

print('------------------------------')
print('Matter ratio for Black Rock:')
print(matter_ratio)


region = [390,430]
par_limits = ([1200,6,0],[1500,6.5,0.4])
popt_fe = gaussFitPlot('180403_data/shiny_task2_600.mca', region, par_limits)

region = [465,500]
par_limits = ([20,7.4,0],[33,7.6,0.4])
popt_ni = gaussFitPlot('180403_data/shiny_task2_600.mca', region, par_limits)

int_ratio = popt_ni[0]/popt_fe[0]
matter_ratio = 0.84625081*int_ratio+0.84800939

print('------------------------------')
print('Matter ratio for Shiny Rock')
print(matter_ratio)
    

region = [390,430]
par_limits = ([1000,6,0],[1300,6.5,0.4])
popt_fe = gaussFitPlot('180403_data/smykkeskrin_task2_600.mca', region, par_limits)

region = [465,500]
par_limits = ([10,7.4,0],[18,7.6,0.4])
popt_ni = gaussFitPlot('180403_data/smykkeskrin_task2_600.mca', region, par_limits)

int_ratio = popt_ni[0]/popt_fe[0]
matter_ratio = 0.84625081*int_ratio+0.84800939

print('------------------------------')
print('Matter ratio for Smykkeskrin Rock')
print(matter_ratio)
    



