# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 20:56:02 2018

@author: Peter Georgi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.close('all')

def loadAtt(filename):
        lines = []                             #Starter tom liste kaldet lines
        attenuation = []
        energy = []
        
        with open (filename,'rt') as in_file:   #Tager hele tekstfilen som variablen in-file (En liste af strings)
            for line in in_file:                
                lines.append(line)          #Her loopes igennem hver eneste linje i tekstfilen, og disse gemmes som elementer i lines   
            for row in lines:                    #Dette loop gemmer kollonerne i data som reelle arrays 
                ny = lines[lines.index(row)].split()
                attenuation.append(float(ny[1]))
                energy.append(float(ny[0]))
    
        return attenuation, energy



att_au, eng_au = loadAtt('au_attenuation.txt')
att_as, eng_as = loadAtt('as_attenuation.txt')
att_fe, eng_fe = loadAtt('fe_attenuation.txt')
att_ni, eng_ni = loadAtt('ni_attenuation.txt')
att_ru, eng_ru = loadAtt('ru_attenuation.txt')
att_ti, eng_ti = loadAtt('ti_attenuation.txt')
att_mo, eng_mo = loadAtt('mo_attenuation.txt')
att_pt, eng_pt = loadAtt('pt_attenuation.txt')
att_ba, eng_ba = loadAtt('ba_attenuation.txt')
att_pd, eng_pd = loadAtt('pd_attenuation.txt')
att_ag, eng_ag = loadAtt('ag_attenuation.txt')
att_ge, eng_ge = loadAtt('ge_attenuation.txt')
att_sr, eng_sr = loadAtt('sr_attenuation.txt')
att_sn, eng_sn = loadAtt('sn_attenuation.txt')
att_nb, eng_nb = loadAtt('nb_attenuation.txt')

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
plt.plot(eng_mo, att_mo, 'r-')
#plt.plot(eng_nb, att_nb, 'y-')

plotatt('180403_data/abs2_900.mca', '180403_data/baggrund_600_2.mca', 900, 600, 0.0033, 10.49)
plt.plot(eng_ag, att_ag, 'r-')
#plt.plot(eng_nb, att_nb, 'y-')

plotatt('180403_data/abs3_900.mca', '180403_data/baggrund_600_2.mca', 900, 600, 0.0025, 19.3)
plt.plot(eng_au, att_au, 'r-')
#plt.plot(eng_nb, att_nb, 'y-')
