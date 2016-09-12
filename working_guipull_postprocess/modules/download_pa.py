# Script to download data from the parameter analyser manually.
import visa
import sys
import time
import os

import numpy as np



# Timestamp to make things easier
def timeStampYMDH():
    # -> 'YYYY_MM_DD_HHMM' as a time stamp
    return time.strftime('%Y_%m_%d_%H%M')

# Path to save the file
# Modify the C:\Users\... part only
# the rest is to timestamp your data :)
def download_data(
        path="C:\Users\cleanroom.STAFF\Desktop\Leo\\test",
        filename="COL111_device1_testing.txt",
        values=['VG', 'VDS', 'ID', 'IG'],
        skip=1):



    # adds a timestamp to the beginning of the filename
    filename=filename[:-4]+'_'+timeStampYMDH()+".csv"

    filename=filename[:-4]+"_"+timeStampYMDH()+filename[-4:]
    # Define the Matrix
    matrix = []
    # Obtain the data from the parameter analyser
    # No error checking
    device = visa.instrument("GPIB::02")
    try:
        print("Parameter Analyser ID: %s" % (device.ask("ID")))
    except:
        print("Could not connect to Parameter Analyser, sorry")
        sys.exit()
    print("Obtaining %s parameters." % len(values))

    for x in range(0, len(values)):
        try:
            print("DO '%s'" % (values[x]))
            # Change this depending on the  value to download
            device.write("DO '%s'" % (values[x]))
        except:
            print("Command Timeout!")
        data = device.read_values()
        print("Obtained %d Data Values!" % (len(data)))
        #Makes the headers for the data
        data.insert(0, "%s" % values[x])
        # Adds timestamp to the start of the file

        if(matrix == []):
            for i in xrange(len(data)):
                matrix.append
        matrix.append(data)

    matrix = zip(*matrix)

    # Save the data to disk
    PATH_FILENAME = os.path.join(path,filename)

    if os.path.isfile(PATH_FILENAME):
        print "that filename already exists, please check directory and try again"
    else:
        with open(PATH_FILENAME, "w") as f:

            for i in range(0, len(matrix)):
                for j in range(0, len(matrix[i])):
                    f.write(", %s" % matrix[i][j])
                f.write('\n')
        f.close()
        print("Data saved to: " + PATH_FILENAME)

    device.close


    #cleans the raw data from the pull section of the script
    try:
        lines = []
        with open(PATH_FILENAME, "r") as f:
            for line in f:
                # removes extra ',' at the start of each data row
                lines.append(line[2:-1])

        with open(PATH_FILENAME, 'w') as g:

            for line in lines:
                # checks for 9.91e+99
                # which is what is appended after compliance is hit
                if line.startswith('9.91e+99') == False:
                    g.write(line + "\n")
    except Exception as e:
        print('there was an error with cleaning: ' + PATH_FILENAME)
        print(e)


    try:
        np.loadtxt(PATH_FILENAME, skiprows=skip,
                   delimiter=",", dtype=float)
    except Exception as e:
        print('there was an error with np.loadtxt after cleaning for:\n ' + PATH_FILENAME)
        print(e)
