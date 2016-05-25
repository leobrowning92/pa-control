import PAplot
import os
import cleandata
import traceback
import sys
#Plotter.plot_two(os.getcwd()+"\\10umgap0_10V.csv",skip=26,title="",xlabel="Gate Voltage (V)",ylabel="Current (A) x$10^{-8}$",data1="$I_G$",data2="$I_D$")
#Plotter.plot_from_file("pa/10umgap-10_10Vdiode.csv",title="",xlabel="Voltage (V)",ylabel="Current (I) x$10^{-12}$")


# allows the Run script to be used within
os.chdir(os.path.dirname(os.path.realpath(__file__)))

filenames = os.listdir("data")
paths = []

for name in filenames:
    paths.append("data/" + name)
# uncomment for fet measurements#
for name in paths:
    try:
        cleandata.check(name)

        if "FET" in name:
            try:
                PAplot.plot_two_yscales(path, skip=2, title="", show=False, log=True,
                                        xlabel="Gate Voltage (VG)", y1label="ID (A)", y2label="IG (A)")
                PAplot.plot_two_yscales(path, skip=2, title="", show=False, log=False,
                                        xlabel="Gate Voltage (VG)", y1label="ID (A)", y2label="IG (A)")
            except Exception as e:
                print('could not make a plot for:\n ' + path)
                print(e)

        elif "diode" in name:
            try:
                PAplot.plot_IV(path, skip=2, title="", show=False,
                               xlabel="Gate Voltage (VG)", ylabel="ID (A)", log=False)
            except Exception as e:
                print('could not make a plot for:\n ' + path)
                print(e)
        else:
            print name + "unprocessed"
    except Exception as e:
        print e
