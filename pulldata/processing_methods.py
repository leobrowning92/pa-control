import numpy as np
import os
import matplotlib.pyplot as plt

def linefit(path, skip=1, delim=","):
    """
    for fitting a line to diode files in order to get an idea of resistance
    """

    data = np.loadtxt(path, skiprows=skip, delimiter=delim, dtype=float)
    x = np.array([row[0]for row in data])
    y = np.array([row[1]for row in data])
    fit = np.polyfit(x,y,1)
    m,c=fit[0],fit[1]
    fit_fn = np.poly1d(fit)
    # fit_fn is now a function which takes in x and returns an estimate for y


    #visual representation of the fits
    plt.plot(x,y,  x, fit_fn(x), '--k')
    plt.show(block=True)
    return m

os.chdir(os.path.dirname(os.path.realpath(__file__)))
linefit('data/2016_04_05_0946_COL188_2_diode.csv')
for path in os.listdir('data'):
    print path
    print linefit('data/'+path)
