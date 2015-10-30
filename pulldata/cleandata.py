import os
import numpy as np
import sys


def clean_data():
    """Cleans the raw data that comes in from download_data_as_matrix.py which
    has an extra comma at the start of each row. and an extra space at the end.
    data should be at the  """

    try:
        skip = 1
        delim = ','

        if os.path.isdir("data") == False:
            os.mkdir("data")

        filenames = os.listdir("raw")

        # print(data)

        for path in filenames:
            try:
                lines = []
                with open("raw/" + path, "r") as f:
                    for line in f:
                        # removes extra ',' at the start of each data row
                        lines.append(line[2:-1])

                with open("data/" + path, 'w') as g:

                    for line in lines:
                        # checks for 9.91e+99
                        # which is what is appended after compliance is hit
                        if line.startswith('9.91e+99') == False:
                            g.write(line + "\n")
            except:
                print('there was an error with cleaning: ' + path)

            try:
                np.loadtxt("data/" + path, skiprows=skip,
                           delimiter=delim, dtype=float)
            except:
                print('there was an error with np.loadtxt after cleaning for:\n ' + path)

    except Exception as e:
        print("Please insure the raw data is from the \
				script download_data_as_matrix.py")
        print("is in a folder called raw in the working directory")
    # print(e)

    print('------------End CleanData-------------')
