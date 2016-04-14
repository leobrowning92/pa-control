# Script to download data from the parameter analyser manually.
import visa
import sys
import time


def clean(path):
    try:
        lines = []
        with open(path, "r") as f:
            for line in f:
                # removes extra ',' at the start of each data row
                lines.append(line[2:-1])
        f.close()

        with open(path, 'w') as g:

            for line in lines:
                # checks for 9.91e+99
                # which is what is appended after compliance is hit
                if line.startswith('9.91e+99') == False:
                    g.write(line + "\n")
        g.close()
    except:
        print('there was an error with cleaning: ' + path)

    pass
# Timestamp to make things easier
def timeStampYMDH():
    # -> 'YYYY_MM_DD_HHMM' as a time stamp
    return time.strftime('%Y_%m_%d_%H%M')

# Path to save the file
# Modify the C:\Users\... part only
# the rest is to timestamp your data :)
def download_data(
        path="C:\Users\cleanroom.STAFF\Desktop\Leo\\test",
        filename="COL_chip1111_device1_testing.txt",
        values=['VG', 'VDS', 'ID', 'IG']):



    # adds a timestamp to the beginning of the filename
    path = path + timeStampYMDH() + "_"



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
        data.insert(0, "%s" % values[x])
        if(matrix == []):
            for i in xrange(len(data)):
                matrix.append
        matrix.append(data)
    matrix = zip(*matrix)

    # Save the data to disk
    PATH_FILENAME = os.path.join(path,filename)
    with open(PATH_FILENAME, "a") as f:
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                f.write(", %s" % matrix[i][j])
            f.write('\n')
    f.close()

    clean(PATH_FILENAME)
    print("Complete, Goodbye!")
