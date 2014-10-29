#!/usr/bin/env python

import sys
import os
import numpy
import StringIO
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import norm
from scipy.stats import normaltest

def plot_string(title, content, years_limit, distance_limit):
    matrix = np.genfromtxt(StringIO.StringIO(content), delimiter=' ', comments="#").astype(int)
    years = matrix[:, 0]
    distance = matrix[:, 1]
    distance_original = distance[:]
    years_original = years[:]
    distance_limit = min(distance_limit, max(distance[:]))
    years_limit = min(years_limit, max(years[:]))
    print("Limits d = %d, y=%d"%(distance_limit, years_limit))
    distance[distance > distance_limit] = distance_limit
    years_low = 0
    years_high = 100
    distance = distance[years >= years_low]
    distance = distance[years <= years_high]
    years = years[years >= years_low]
    years = years[years <= years_high]

#    figure = plt.figure()
#    plt.plot(years, distance,'.r')
#    plt.xlabel('years')
#    plt.ylabel('distance')
#    plt.axis('scaled')
    
    f, ax = plt.subplots(2, 3)
#    plt.title(title)
    
    H, xedges, yedges = np.histogram2d(years, distance, bins=(range(18, years_limit + 1),range(1, distance_limit + 1)))
    H = np.rot90(H)
    H = np.flipud(H)
    Hmasked = np.ma.masked_where(H==0, H)
    

    ax[0][0].pcolormesh(xedges,yedges,Hmasked)
    ax[0][0].set_title(title + ' Count = ' + str(len(years)))

    ax[0][0].set_xlabel('years')
    ax[0][0].set_ylabel('distance')
#    ax[0][0].axis('scaled')
#    cbar = plt.colorbar()
#    cbar.ax.set_ylabel('Counts')    


    ax[0][1].hist(distance, bins=range(1, distance_limit + 1), color='red', alpha=0.5, linewidth=1.0, label='CDF distance', normed=True)
    ax[0][1].set_title('H distance normed')
    ax[0][1].grid(b=True, which='both', color='0.65',linestyle='-')

    ax[1][0].hist(distance, bins=range(1, distance_limit + 1), color='red', alpha=0.5, linewidth=1.0, label='CDF distance')
    ax[1][0].set_title('H distance')    
    ax[1][0].grid(b=True, which='both', color='0.65',linestyle='-')

    ax[1][1].hist(distance, bins=range(1, distance_limit + 1), cumulative=True, normed=True, color='red', alpha=0.5, histtype='bar', linewidth=1.0, label='CDF distance')
    ax[1][1].set_title('CDF distance')
    ax[1][1].grid(b=True, which='both', color='0.65',linestyle='-')
    mu, sigma = norm.fit(years_original)

    ax[0][2].hist(years, bins=range(18, years_limit + 1), color='blue', alpha=0.5, linewidth=1.0, label='CDF years', normed=True)
    ax[0][2].set_title('H years')
    ax[0][2].grid(b=True, which='both', color='0.65',linestyle='-')
    mu, sigma = norm.fit(years)
      
    xmin, xmax = ax[0][2].get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, sigma)
    fit_title = "Fit results: mu = %.2f,  sigma = %.2f, sigma/mu= %2f" % (mu, sigma, sigma/mu)
    ax[0][2].set_title('H years ' + fit_title)
    ax[0][2].plot(x, p, 'k', linewidth=2)
        
    ax[1][2].set_title('CDF years')
    ax[1][2].hist(years, bins=range(18, years_limit + 1), cumulative=True, normed=True, color='blue', alpha=0.5, histtype='bar', linewidth=1.0, label='CDF years')
    ax[1][2].grid(b=True, which='both', color='0.65',linestyle='-')

#    ax[1][2].hist(distance, bins=range(1, distance_limit + 1), color='blue', alpha=0.5, linewidth=1.0, label='distance', normed=True)
#    ax[1][2].set_title('H distance')
    plt.show()

years_limit = 1000
distance_limit = 162
path = 'data/'
listing = os.listdir(path)
print(listing)
total_str = ''

for infile in listing:
    with open(path + infile, 'r') as file:
        content = file.read()
        total_str += content
        plot_string(infile, content, years_limit, distance_limit)

plot_string('total', total_str, years_limit, distance_limit)

