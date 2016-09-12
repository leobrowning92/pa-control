import numpy as np
import os


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
        print path + "\ndata cleaned"
        print "----------"
    except Exception as e:
        print('error cleaning : ' + path)
        print e
        print "----------"

    return


def check(path):
    try:
        np.loadtxt(path, skiprows=1, delimiter=",", dtype=float)
        print path + "\ntest load successful"
        print "----------"
    except Exception as e:
        print e
        clean(path)
        try:
            np.loadtxt(path, skiprows=1, delimiter=",", dtype=float)
            print path + "\ntest load successful"
            print "----------"
        except Exception as e:
            print "error loading data : " +path
            print e
            print "----------"
