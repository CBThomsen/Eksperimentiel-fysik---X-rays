import numpy as np
import matplotlib.pyplot as plt

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

channels, counts = loadData('180320_data/kali_am_600.mca')
plt.figure()
plt.plot(channels,counts)
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.title('Am-241 counts vs. channels')
plt.legend(['Data Am-241'])


channels, counts = loadData('180320_data/kali_fe_900.mca')
plt.figure()
plt.plot(channels,counts)
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.title('Fe-55 counts vs. channels')
plt.legend(['Data Fe-55'])

channels, counts = loadData('180320_data/kali_cs_600.mca')
plt.figure()
plt.plot(channels,counts)
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.title('Cs-137 counts vs. channels')
plt.legend(['Data Cs-137'])

channels, counts = loadData('180403_data/baggrund_600_2.mca')
plt.figure()
plt.plot(channels,counts)
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.title('Baggrund counts vs. channels')
plt.legend(['Data Baggrund'])


channels, counts = loadData('180403_data/abs3_900.mca')
plt.figure()
plt.plot(channels,counts)
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.title('Absorber 3 counts vs. channels')
plt.legend(['Data'])

channels, counts = loadData('180403_data/50_50_task2_cal_602.mca')
plt.figure()
plt.plot(channels,counts)
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.title('Fe:Ni 50:50 counts vs. channels')
plt.legend(['Data'])

channels, counts = loadData('180403_data/36_64_task2_cal_600.mca')
plt.figure()
plt.plot(channels,counts)
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.title('Fe:Ni 64:36 counts vs. channels')
plt.legend(['Data'])



