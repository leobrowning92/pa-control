#!/var/run/python
# Agilent Parameter Analyser Sweep function script.
"""
Original script = python program_test6_TimeScanHannah.py
Created on Wed Oct 21 10:20:18 2013
@author b.hall + j.lovellsmith

This script = sweepandcollect_diode.py
Nov 11th 2015
@author L.Browning

Runs with python 2.7x
"""
# ----------------------
# DON'T MODIFY THIS
# ----------------------
import os.path
import msvcrt
import sys
import time
import serial
import visa

# ----------------------
# MODIFY THESE SETTINGS
# ----------------------

# Path to save files
directory = "C:/Users/Cleanroom.STAFF/Desktop/Leo/outputs"
# File header information
sample_name = 'SNT080'  # Information about the sample used
sample_conditions = 'dropcastAg_reactivation_0.5Vx5_sweep_run002'  # Information about production conditions


# Source Settings

### var1 ###
sweep_mode = '1'  # 1:Linear 2:Log10 3:Log25 4:Log50
# Single: sweep up or down depending on the sign of VDS_step
# Double: sweep both up and down
# the sign of VDS_step just denotes which direction happens first.
sweep = 'Double'
var1_voltage = 'VF'  # var1 voltage label
var1_current = 'IF'  # var1 current label
var1_start = '0'  # -100 to 100V for SMU; -200 to 200V for HPSMU; -20 to 20V for VSU
var1_stop = '100E-3'  # -100 to 100V for SMU; -200 to 200V for HPSMU; -20 to 20V for VSU
var1_step = '2E-3'  # 0 to 200V for SMU; 0 to 400V for HPSMU; 0 to 40V for VSU
var1_compliance = '1E-6'  # -0.1 to 0.1A for SMU; -1 to 1A for HPSMU


#### var2 ###
var2_voltage = 'VG'  # var2 voltage label
var2_current = 'IG'  # var2 current label
var2_start = '0'  # -100 to 100V for SMU; -200 to 200V for HPSMU
var2_step = '0'  # -100 to 100V for SMU; -200 to 200V for HPSMU
var2_number_of_steps = '1'  # 1 to 128
var2_compliance = '1E-3'  # -0.1 to 0.1A for SMU; -1 to 1A for HPSMU

# Time Settings
cycles = 1  # number of cycles the script should run # REMEMBER IF VG_STEP IS SET TO INCREMENT THE NUMBER OF CYCLES VG COULD BECOME AN EXTREMELY HIGH VALUE
time_between_cycles = 100
integration_time = '2'  # 1 = Short, 2 = Medium, 3 = Long
##num_readings = abs(float(var1_start) - float(var1_stop) / float(var1_step))
num_readings = abs((float(var1_start) - float(var1_stop)) /
                  float(var1_step)) * int(var2_number_of_steps)
print("Number of readings to obtain: %d" % num_readings)

# Measurement Display - Graph scaling on the parameter analyser
x_axis_scale = '1'  # 1:Linear 2:Logarithmic
x_axis_minimum = var1_start  # numeric value
x_axis_maximum = var1_stop  # numeric value
y_axis_var1_scale = '1'  # 1:Linear 2:Logarithmic
y_axis_var1_minimum = '0'  # numeric value
y_axis_var1_maximum = '1E-3'  # numeric value
y_axis_var2_scale = '1'  # 1:Linear 2:Logarithmic
y_axis_var2_minimum = '-1E-3'  # numeric value
y_axis_var2_maximum = '1E-3'  # numeric value


# ----------------------
# DON'T MODIFY THIS
# ----------------------
matrix = []
for i in xrange(int(num_readings)):
    matrix.append
# Check to press ctrl+c to escape the script


def check_escape():
    return msvcrt.kbhit() and msvcrt.getch() == chr(27)



# Error codes from the parameter analyser


def print_error(sp):
    "Parameter Analyser eror message"
    message = {
        0: "data ready",
        1: "syntax error",
        2: "end status",
        3: "illegal program",
        4: "busy",
        5: "self-test fail",
        6: "service request",
        7: "emergency"
    }
    for i in xrange(7):
        if sp & 2**i:
            print " %i: %s" % (i + 1, message[i])

#timestamp functions
def timestampYMDH():
    #-> 'YYYY_MM_DD_HHMM' as a time stamp
    return time.strftime('%Y_%m_%d_%H%M')
def timestampHHMMSS():
    #-> 'HH:MM:SS' as a time stamp
    return time.strftime('%H:%M:%S')
def timestampDDMMYYYY():
    #-> 'DD.MM.YYYY' as a time stamp
    return time.strftime('%d.%m.%Y')




# Different loop modes


class ModeCycle(object):

    def __init__(self, interval):
        self.interval = interval

    def begin(self, *args):
        self.cycle_start = time.clock()
        # print "begin worked"

    @property
    def message(self):
        return ""

    def end(self, *args):
        elapsed = time.clock() - self.cycle_start
        remaining = self.interval - elapsed
        # print "end worked"
        if remaining < 0:
            print "interval exceeded by %G s" % abs(remaining)
        else:
            print "waiting %G s" % remaining
            time.sleep(remaining)

# File setup methods




# simplified script to control the Agilent Parameter Analyser
# this script just throws GPIB commands into the parameter analyser
# it could cause USB buffer overflow errors on the GPIB converter unit

# File setup methods matrix


def initialise_matrix_file(path):
    """

    """
    with open(path, 'w') as f:
        f.write('Sweep data\n')
        f.write('Date of experiment: %s\n' % (timestampDDMMYYYY()))
        f.write('Time of experiment: %s\n' % (timestampHHMMSS()))
        f.write('Sample:%s\n' % (sample_name))
        f.write('%s : %s to %s in %sV step(s)\n' %
                (var1_voltage, float(var1_start), float(var1_stop), float(var1_step)))
        f.write('%s : %s to %s in %sV step(s)\n' % (var2_voltage,       float(var2_start), (float(var2_start) + (float(var2_step) * float(var2_number_of_steps))), float(var2_step)))



def update_matrix_file(path, info, data):
    with open(path, 'a') as f:
        # f.write(info[0])
        #f.write(', ')
        # f.write(info[1])
        #f.write(', ')
        # f.write(info[2])
        #f.write(', ')
        #f.write(", ".join("%.16G" % x_i for x_i in data))
        f.write(", ".join("%s" % x_i for x_i in transpose_matrix[i]))
        f.write('\n')

# Initialise each file
string_YMDH = timestampYMDH()

filename_matrix = "%s_%s_matrix_%s.txt" % (sample_name, sample_conditions, string_YMDH)


path_matrix = os.path.join(directory, filename_matrix)

print path_matrix






initialise_matrix_file( path_matrix )

#===================================================

#===================================================
LF = serial.to_bytes([10])
CR = serial.to_bytes([13])
CRLF = serial.to_bytes([13, 10])
start_char = 0
end_char = 0

# Open the GPIB bus
print "Initialising the Analyser"
try:
    HP4145B = visa.instrument("GPIB::02")  # 4145 Code
    HP4145B.timeout = 60
    HP4145B.term_char = CR + LF
    HP4145B.delay = 1
    # Clear the device errors
    HP4145B.clear()
    # Set to 4145B Mode
    # to enable this would require rewriting all GPIB commands
    # with one function per line, and then reads may be dodgy
    # like in HP4155C mode still
    # HP4145B.write("US42 31") ## would need to rewrite with separate lines for each command
    # Check communications
    print "Parameter Analyser ID:"
    print HP4145B.ask("ID")  # 4145 Code
    # HP4155B.write("*IDN?") ## 4155 Code
except:
    print "Could not connect to the Parameter Analyser!"

    sys.exit()

# Setup Program parameters
program_parameters = "IT%s CA1 DR1 BC" % (integration_time)
print program_parameters
HP4145B.write(program_parameters)
# Setup Channel Definitions for sweep
channel_definitions = "DE CH1,'VS','IS',3,3;CH2,'%s','%s',1,1;CH3,'%s','%s',1,2;CH4;" % (
    var1_voltage, var1_current, var2_voltage, var2_current)
# Channel 1
# Channel 2
# Channel 3
# Channel 4
print channel_definitions
HP4145B.write(channel_definitions)
# Setup Measurement display
measurement_display = "SM DM1 XN '%s',%s,%s,%s; YA '%s',%s,%s,%s; YB '%s',%s,%s,%s" % (
    var1_voltage, x_axis_scale, x_axis_minimum, x_axis_maximum, var1_current, y_axis_var1_scale, y_axis_var1_minimum, y_axis_var1_maximum, var2_current, y_axis_var2_scale, y_axis_var2_minimum, y_axis_var2_maximum)
# this needs to be modified to include variable var1 and var2 names.
print measurement_display
HP4145B.write(measurement_display)

# Check error flag
sp = HP4145B.stb
if sp != 0:
    print "Instrument state problem, spoll = %s" % hex(sp)
    print_error(sp)

    sys.exit()
# record start time
start_time = time.clock()
# Data Acquisition loop
mode = ModeCycle(time_between_cycles)
for i in xrange(cycles):
    print "cycle: %i of %i" % (i, cycles)

    mode.begin()
    # Setup var1 Source
    var1_setup = "SS VR %s,%s,%s,%s,%s" % (
        sweep_mode, var1_start, var1_stop, var1_step, var1_compliance)
    print var1_setup
    HP4145B.write(var1_setup)
    # Setup var2 Source
    var2_setup = "SS VP %s,%s,%s,%s" % (
        var2_start, var2_step, var2_number_of_steps, var2_compliance)
    print var2_setup
    HP4145B.write(var2_setup)
    HP4145B.write("BC")
    time_since_start = str(time.clock() - start_time)
    T_start_sweep = time.clock()
    # Start Measurement
    HP4145B.write("MD ME1")
    # HP4145B.wait_for_ready()
    while not HP4145B.stb & 1:
        sys.stdout.write('.')
        time.sleep(HP4145B.delay)
    print
    # Get Measured values
    ## var1_down=HP4145B.ask_for_values("DO '%s'" % var1_current)
    ## var2_down=HP4145B.ask_for_values("DO '%s'" % var2_current)
    try:
        visa.instrument("GPIB::02").write("DO '%s'" % var1_current)
    except:
        print("Timeout processing DO '%s'" % var2_current)
    var1_down = visa.instrument("GPIB::02").read_values()
    try:
        visa.instrument("GPIB::02").write("DO '%s'" % var2_current)
    except:
        print("Timeout processing DO '%s'" % var2_current)
    var2_down = visa.instrument("GPIB::02").read_values()

    # Do we want to loop up and down?
    if sweep == 'Double':
        # Reverse sweep direction
        var1_setup = "SS VR %s,%s,%s,%s,%s" % (
            sweep_mode, var1_stop, var1_start, '-' + var1_step, var1_compliance)
        print var1_setup
        HP4145B.write(var1_setup)
        # Start Measurement
        HP4145B.write("MD ME1")
        # HP4145B.wait_for_ready()
        while not HP4145B.stb & 1:
            # Update the screen to inform user of progress
            sys.stdout.write('.')
            time.sleep(HP4145B.delay)
        print
        # Get Measured values
        ##var1_ask = "DO '%s'" % (var1_current)
        ##var2_ask = "DO '%s'" % (var2_current)
        ##var1_total = var1_down + HP4145B.ask_for_values(var1_ask)
        ##var2_total = var2_down + HP4145B.ask_for_values(var2_ask)
        try:
            visa.instrument("GPIB::02").write("DO '%s'" % var1_current)
        except:
            print("Timeout processing DO '%s'" % var2_current)
        var1_total = var1_down + visa.instrument("GPIB::02").read_values()
        try:
            visa.instrument("GPIB::02").write("DO '%s'" % var2_current)
        except:
            print("Timeout processing DO '%s'" % var2_current)
        var2_total = var2_down + visa.instrument("GPIB::02").read_values()

    else:
        var1_total = var1_down
        var2_total = var2_down
    T_stop_sweep = time.clock()
    time_for_sweep = str(T_stop_sweep - T_start_sweep)
    print 'sweep time', time_for_sweep
    # Print Values
    # print var1_down
    # print var2_down
    # Save values to disk
    msg = mode.message

    var1_total.insert(0, var1_current)
    var2_total.insert(0, var2_current)
    # X axis title, insert X axis period and label
    X_axis = [var1_voltage]
    X_values = abs((float(var1_start) - float(var1_stop)) /
                   float(var1_step)) + 1
    for x in range(0, int(var2_number_of_steps)):
        for j in range(0, int(X_values)):
            X_axis.append(float(var1_start) + (j * float(var1_step)))
        if sweep == 'double':
            for j in range(1, int(X_values)):
                X_axis.append(float(var1_stop) - (j * float(var1_step)))
    matrix.append(X_axis)
    matrix.append(var1_total)
    matrix.append(var2_total)
    transpose_matrix = zip(*matrix)
    print("Matrix Length %d" % len(matrix))
    print("Matrix Width %d" % len(matrix[0]))
    # print transpose_matrix
    if i == cycles - 1:
        for i in range(0, len(transpose_matrix)):
            update_matrix_file(path_matrix, (time_since_start,
                                             time_for_sweep, "%s" % msg), transpose_matrix[i])
    # Exit nicely
    if check_escape():
        sys.exit()

    mode.end()
