import numpy as np
import matplotlib.pyplot as plt


with open('180410_data/glimmer_1800.mca') as text:
    
    counts = []
    lister = text.readlines()
    begin = lister.index('<<DATA>>\n')+1
    end = lister.index('<<END>>\n')-1
    data = lister[begin:end]
    for i in data:
        counts.append(float(i))
    channels = range(0,len(counts))

plt.plot(channels,counts)
    

