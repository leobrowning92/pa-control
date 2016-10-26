## Script to download data from the parameter analyser manually.
import visa
import os
import msvcrt
import sys
import time

## Timestamp to make things easier
def timeStampYMDH():
    #-> 'YYYY_MM_DD_HHMM' as a time stamp
    return time.strftime('%Y_%m_%d_%H%M')

## Path to save the file
## Modify the C:\Users\... part only
## the rest is to timestamp your data :)
PATH = ("C:\Users\cleanroom.STAFF\Desktop\\" + timeStampYMDH() + "_")

## Filename to save the file
## Modify this filename but
## leave as *.csv so you can open in excel :)
FILENAME = "S8_20um_Orco.csv" # values in the array values will be appended to the front of this

## Values to download
## Modify this array to the value of the data you wish to download
## See the user manual for how to obtain these values.
values = ['ID','IG'] 

## Obtain the data from the parameter analyser
## No error checking
device = visa.instrument("GPIB::02")
try:
    print "Parameter Analyser ID: %s"%(device.ask("ID"))
except:
    print "Could not connect to Parameter Analyser, sorry"
    sys.exit()
print("Obtaining %s parameters."%len(values))
for x in range(0,len(values)):
    try:
        print("DO '%s'"%(values[x]))
        device.write("DO '%s'"%(values[x]))  ## Change this depending on the value to download
    except:
        print "Command Timeout!"
        
    data = device.read_values()
    print("Obtained %d Data Values!"%(len(data)))
    ## Save the data to disk
    PATH_FILENAME = PATH + FILENAME
    with open(PATH_FILENAME,"a") as f:
        f.write("Downloaded Data: %s"%(values[x]))
        f.write('\n')
        for i in range(0,len(data)):
            f.write("%s, " %data[i])
        f.write('\n')

f.close()
print("Complete, Goodbye!")
