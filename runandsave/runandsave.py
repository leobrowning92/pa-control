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
ROOT = "C:/Users/Cleanroom.STAFF/Desktop/Leo/outputs"
# File header information
SAMPLE = 'Blank'  # Information about the sample used
CONDITIONS = 'test'  # Information about production conditions


# Source Settings

### VAR1 ###
sweep_mode = '1'  # 1:Linear 2:Log10 3:Log25 4:Log50
# Single: sweep up or down depending on the sign of VDS_step
# Double: sweep both up and down
# the sign of VDS_step just denotes which direction happens first.
sweep = 'Single'
VAR1_voltage = 'VDS'  # VAR1 voltage label
VAR1_current = 'ID'  # VAR1 current label
VAR1_start = '-10'  # -100 to 100V for SMU; -200 to 200V for HPSMU; -20 to 20V for VSU
VAR1_stop = '10'  # -100 to 100V for SMU; -200 to 200V for HPSMU; -20 to 20V for VSU
VAR1_step = '0.2'  # 0 to 200V for SMU; 0 to 400V for HPSMU; 0 to 40V for VSU
VAR1_compliance = '1E-3'  # -0.1 to 0.1A for SMU; -1 to 1A for HPSMU


#### VAR2 ###
VAR2_voltage = 'VG'  # VAR2 voltage label
VAR2_current = 'IG'  # VAR2 current label
VAR2_start = '0'  # -100 to 100V for SMU; -200 to 200V for HPSMU
VAR2_step = '0'  # -100 to 100V for SMU; -200 to 200V for HPSMU
VAR2_number_of_steps = '1'  # 1 to 128
VAR2_compliance = '1E-3'  # -0.1 to 0.1A for SMU; -1 to 1A for HPSMU

# Time Settings
Cycles = 1  # number of cycles the script should run # REMEMBER IF VG_STEP IS SET TO INCREMENT THE NUMBER OF CYCLES VG COULD BECOME AN EXTREMELY HIGH VALUE
Time_between_cycles = 100
Integration_time = '2'  # 1 = Short, 2 = Medium, 3 = Long
waitTime = '5'
intervalTime = '0'
##numReadings = abs(float(VAR1_start) - float(VAR1_stop) / float(VAR1_step))
numReadings = abs((float(VAR1_start) - float(VAR1_stop)) /
                  float(VAR1_step)) * int(VAR2_number_of_steps)
print("Number of readings to obtain: %d" % numReadings)

# Measurement Display - Graph scaling on the parameter analyser
x_axis_scale = '1'  # 1:Linear 2:Logarithmic
x_axis_minimum = '-12'  # numeric value
x_axis_maximum = '12'  # numeric value
y_axis_VAR1_scale = '1'  # 1:Linear 2:Logarithmic
y_axis_VAR1_minimum = '-1E-3'  # numeric value
y_axis_VAR1_maximum = '1E-3'  # numeric value
y_axis_VAR2_scale = '1'  # 1:Linear 2:Logarithmic
y_axis_VAR2_minimum = '-1E-3'  # numeric value
y_axis_VAR2_maximum = '1E-3'  # numeric value

# Pressure Pump
pump_disabled = 1  # stopgap to ensure that no residual pump code is operating


# ----------------------
# DON'T MODIFY THIS
# ----------------------
matrix = []
for i in xrange(int(numReadings)):
    matrix.append
# Check to press ctrl+c to escape the script


def check_escape():
    return msvcrt.kbhit() and msvcrt.getch() == chr(27)


def Integration_text(x):
    return{'1': "Short", '2': "Medium", '3': "Long"}[x]

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
def timeStampYMDH():
    #-> 'YYYY_MM_DD_HHMM' as a time stamp
    return time.strftime('%Y_%m_%d_%H%M')
def timeStampHHMMSS():
    #-> 'HH:MM:SS' as a time stamp
    return time.strftime('%H:%M:%S')
def timeStampDDMMYYYY():
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
        f.write('Carbon Nanotube Semiconductor Analysis\n')
        f.write('Date of experiment: %s\n' % (timeStampDDMMYYYY()))
        f.write('Time of experiment: %s\n' % (timeStampHHMMSS()))
        f.write('\n')
        f.write('Sample:%s\n' % (SAMPLE))
        f.write('%s : %s to %s in %sV step(s)\n' %
                (VAR1_voltage, float(VAR1_start), float(VAR1_stop), float(VAR1_step)))
        f.write('%s : %s to %s in %sV step(s)\n' % (VAR2_voltage,       float(VAR2_start), (float(VAR2_start) + (float(VAR2_step) * float(VAR2_number_of_steps))), float(VAR2_step)))



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
string_YMDH = timeStampYMDH()

filename_matrix = "%s_%s_matrix_%s.txt" % (SAMPLE, CONDITIONS, string_YMDH)


path_matrix = os.path.join(ROOT, filename_matrix)

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
program_parameters = "IT%s CA1 DR1 BC" % (Integration_time)
print program_parameters
HP4145B.write(program_parameters)
# Setup Channel Definitions for sweep
channel_definitions = "DE CH1,'VS','IS',3,3;CH2,'%s','%s',1,1;CH3,'%s','%s',1,2;CH4;" % (
    VAR1_voltage, VAR1_current, VAR2_voltage, VAR2_current)
# Channel 1
# Channel 2
# Channel 3
# Channel 4
print channel_definitions
HP4145B.write(channel_definitions)
# Setup Measurement display
measurement_display = "SM DM1 XN '%s',%s,%s,%s; YA '%s',%s,%s,%s; YB '%s',%s,%s,%s" % (
    VAR1_voltage, x_axis_scale, x_axis_minimum, x_axis_maximum, VAR1_current, y_axis_VAR1_scale, y_axis_VAR1_minimum, y_axis_VAR1_maximum, VAR2_current, y_axis_VAR2_scale, y_axis_VAR2_minimum, y_axis_VAR2_maximum)
# this needs to be modified to include variable VAR1 and VAR2 names.
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
Mode = ModeCycle(Time_between_cycles)
for i in xrange(Cycles):
    print "cycle: %i of %i" % (i, Cycles)

    Mode.begin()
    # Setup VAR1 Source
    var1_setup = "SS VR %s,%s,%s,%s,%s" % (
        sweep_mode, VAR1_start, VAR1_stop, VAR1_step, VAR1_compliance)
    print var1_setup
    HP4145B.write(var1_setup)
    # Setup VAR2 Source
    var2_setup = "SS VP %s,%s,%s,%s" % (
        VAR2_start, VAR2_step, VAR2_number_of_steps, VAR2_compliance)
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
    ## VAR1_down=HP4145B.ask_for_values("DO '%s'" % VAR1_current)
    ## VAR2_down=HP4145B.ask_for_values("DO '%s'" % VAR2_current)
    try:
        visa.instrument("GPIB::02").write("DO '%s'" % VAR1_current)
    except:
        print("Timeout processing DO '%s'" % VAR2_current)
    VAR1_down = visa.instrument("GPIB::02").read_values()
    try:
        visa.instrument("GPIB::02").write("DO '%s'" % VAR2_current)
    except:
        print("Timeout processing DO '%s'" % VAR2_current)
    VAR2_down = visa.instrument("GPIB::02").read_values()

    # Do we want to loop up and down?
    if sweep == 'double':
        # Reverse sweep direction
        var1_setup = "SS VR %s,%s,%s,%s,%s" % (
            sweep_mode, VAR1_stop, VAR1_start, '-' + VAR1_step, VAR1_compliance)
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
        ##VAR1_ask = "DO '%s'" % (VAR1_current)
        ##VAR2_ask = "DO '%s'" % (VAR2_current)
        ##VAR1_total = VAR1_down + HP4145B.ask_for_values(VAR1_ask)
        ##VAR2_total = VAR2_down + HP4145B.ask_for_values(VAR2_ask)
        try:
            visa.instrument("GPIB::02").write("DO '%s'" % VAR1_current)
        except:
            print("Timeout processing DO '%s'" % VAR2_current)
        VAR1_total = VAR1_down + visa.instrument("GPIB::02").read_values()
        try:
            visa.instrument("GPIB::02").write("DO '%s'" % VAR2_current)
        except:
            print("Timeout processing DO '%s'" % VAR2_current)
        VAR2_total = VAR2_down + visa.instrument("GPIB::02").read_values()

    else:
        VAR1_total = VAR1_down
        VAR2_total = VAR2_down
    T_stop_sweep = time.clock()
    time_for_sweep = str(T_stop_sweep - T_start_sweep)
    print 'sweep time', time_for_sweep
    # Print Values
    # print VAR1_down
    # print VAR2_down
    # Save values to disk
    msg = Mode.message

    VAR1_total.insert(0, VAR1_current)
    VAR2_total.insert(0, VAR2_current)
    # X axis title, insert X axis period and label
    X_axis = [VAR1_voltage]
    X_values = abs((float(VAR1_start) - float(VAR1_stop)) /
                   float(VAR1_step)) + 1
    for x in range(0, int(VAR2_number_of_steps)):
        for j in range(0, int(X_values)):
            X_axis.append(float(VAR1_start) + (j * float(VAR1_step)))
        if sweep == 'double':
            for j in range(1, int(X_values)):
                X_axis.append(float(VAR1_stop) - (j * float(VAR1_step)))
    matrix.append(X_axis)
    matrix.append(VAR1_total)
    matrix.append(VAR2_total)
    transpose_matrix = zip(*matrix)
    print("Matrix Length %d" % len(matrix))
    print("Matrix Width %d" % len(matrix[0]))
    # print transpose_matrix
    if i == Cycles - 1:
        for i in range(0, len(transpose_matrix)):
            update_matrix_file(path_matrix, (time_since_start,
                                             time_for_sweep, "%s" % msg), transpose_matrix[i])
    # Exit nicely
    if check_escape():
        sys.exit()

    Mode.end()
