#!trial_script.py
"""
Original script
Created on Wed Oct 21 10:20:18 2013
@author b.hall + j.lovellsmith

This script
Created Thu Dec 12 09:15:10 2013
@author h.colenso
"""
##----------------------
## DON'T MODIFY THIS
##----------------------
import os.path
import os
import msvcrt
import sys
import serial
import io
import visa
import time
##----------------------
## MODIFY THESE SETTINGS
##----------------------
#Path to save files
ROOT = "D:/from desktop/"
# File header information
SAMPLE = 'Test'# Information about the sample used
CONDITIONS = 'Script Test' # Information about production conditions
# Source Settings
# Constant source
VDS_const = '0.1' # -100 to 100V for SMU; -200 to 200V for HPSMU; -20 to 20V for VSU
VDS_step = '0' # 0 to 200V for SMU; 0 to 400V for HPSMU; 0 to 40V for VSU
ID_compliance = '20E-3' # -0.1 to 0.1A for SMU; -1 to 1A for HPSMU
# Constant source
VG_const = '0' # -100 to 100V for SMU; -200 to 200V for HPSMU
VG_step = '0' # SET TO ZERO IF YOU DON'T WANT TO INCREMENT BETWEEN CYCLES # ONLY SET SO THAT THE MAXIMUM VALUE OF VG WILL BE REACHED AFTER THE NUMBER OF CYCLES => VG_MAX = VG_CONST + (VG_step * Cycles) 
IG_compliance = '1E-3' # -0.1 to 0.1A for SMU; -1 to 1A for HPSMU 

# Time Settings
Cycles = 1 # number of cycles the script should run # REMEMBER IF VG_STEP IS SET TO INCREMENT THE NUMBER OF CYCLES VG COULD BECOME AN EXTREMELY HIGH VALUE
Time_between_cycles = 80 # stabilisation time, script will pause until this elapses between cycles. Ignore if using a single cycle.
waitTime = '0' # -30.0ms to 838.8607 s 
intervalTime = '0.2' # 60us to 65.532s # time between measurements
numReadings = '8250' # 1 to 8250 # number of measurements
prompt_between_cycles = 0 # do you want to press enter to continue between cycles?
Integration_time = 2 # 1 - short 2 - medium 3 - long
# Measurement Display - Graph scaling on the parameter analyser
x_axis_scale = '1' # 1:Linear 2:Logarithmic
x_axis_minimum = '0' # numeric value
x_axis_maximum = '4000' # numeric value
y_axis_ID_scale = '1' # 1:Linear 2:Logarithmic
y_axis_ID_minimum = '0' # numeric value
y_axis_ID_maximum = '10E-9' # numeric value
y_axis_IG_scale = '1' # 1:Linear 2:Logarithmic
y_axis_IG_minimum = '-10E-9' # numeric value
y_axis_IG_maximum = '10E-9' # numeric value

# Pressure Pump
pump_disabled = 1 # set to one to disable pressure pump operation
pressure = 200 # Pressure to set the pump in mbar
# time_period = 300 # Time in seconds to leave the pressure pump running for
wait_time = 10 # time to wait between status updates
COM = 2 # COM port (starts from 0, so subtract one from the COM number windows states, ie COM1 in windows is 0 here.)
#
# Only inserted to keep MATLAB Happy - These settings do nothing!
matrix = []
for i in xrange(int(numReadings)):
	matrix.append
sweep_mode = '1' # 1:Linear 2:Log10 3:Log25 4:Log50
sweep = 'single' # Single: sweep up or down depending on the sign of VDS_step  Double: sweep both up and down the sign of VDS_step just denotes which direction happens first.

##----------------------
## DON'T MODIFY THIS
##----------------------
def check_escape():
    return msvcrt.kbhit() and msvcrt.getch() == chr(27)

def Integration_text(x):
    return{1:"Short",2:"Medium",3:"Long"}[x]

def print_error(sp):
	"error message"
	message = {
		0 : "data ready",
		1 : "syntax error",
		2 : "end status",
		3 : "illegal program",
		4 : "busy",
		5 : "self-test fail",
		6 : "service request",
		7 : "emergency"
	}
	for i in xrange(7):
		if sp & 2**i:
			print " %i: %s" %(i+1,message[i])

# Different loop modes
class ModeCycle(object):
    def __init__(self,interval):
        self.interval = interval
        
    def begin(self,*args):
        self.cycle_start = time.clock()
    
    @property
    def message(self):
        return ""
        
    def end(self,*args):
        elapsed = time.clock() - self.cycle_start
        remaining = self.interval - elapsed
        if remaining < 0:
            print "interval exceeded by %G s" % abs(remaining)
        else:
            print "waiting %G s" % remaining
            time.sleep(remaining)

def timeStampYMDH():
    #-> 'YYYY_MM_DD_HHMM' as a time stamp
    return time.strftime('%Y_%m_%d_%H%M')
def timeStampHHMMSS():
    #-> 'HH:MM:SS' as a time stamp
    return time.strftime('%H:%M:%S')
def timeStampDDMMYYYY():
	#-> 'DD.MM.YYYY' as a time stamp
	return time.strftime('%d.%m.%Y')
def timeStampYYMMDD():
    #-> 'YYMMDD' as a time stamp (JLS)
    return time.strftime('%Y%m%d')
    
def xlTimeStamp():
    #-> 'HH:MM:SS DD/MM/YYYY' as a time stamp
    return time.strftime('%H:%M:%S %d/%m/%Y')

## File setup methods ID + IG
def initialise_file(path,info):
    """

    """
    with open(path,'w') as f:
        f.writelines(info)
        f.write('\n')
        f.write('Directory,%s\n' % (str(ROOT)))
        f.write('Sample,%s\n' % (SAMPLE))
        f.write('Conditions,%s\n' % (CONDITIONS))
	f.write('Script Type,Timed')
        f.write('Sweep Mode,%s\n' % (sweep_mode))
	f.write('Sweep direction,%s\n' % (sweep))
        f.write('Number of Cycles,%s\n' % (Cycles))
        f.write('VDS Initial Value,%s\n' % (VDS_const))
        f.write('VDS Increment Value,%s\n' %(VDS_step))
        f.write('VDS Final Cycle Value,%s\n' % (float(VDS_const) + (float(VDS_step)*float(Cycles))))
        f.write('ID Compliance Value,%s\n' % (ID_compliance))
        f.write('VG Value,%s\n' % (VG_const))
        f.write('VG Increment Between Cycles,%s\n' %(VG_step))
        f.write('VG Final Cycle Value,%s\n' % (float(VG_const) + (float(VG_step)*float(Cycles))))
        f.write('IG Compliance Value,%s\n' % (IG_compliance))
	f.write('Wait Time,%s\n' % (waitTime))
	f.write('Interval Time,%s\n' % (intervalTime))
	f.write('Number of Readings,%s\n' % (numReadings))
	f.write('Integration time, %s\n' % (Integration_text(Integration_time)))
	if pump_disabled == 0:
            f.write('Microfluidic Pump Pressure, %s\n' % (pressure))
        else:
            f.write('Microfluidic Pump Pressure, Pump Disabled\n')
        if x_axis_scale == str(1):
            f.write('X axis is Linear\n')
        else: 
            f.write('X axis is Logarithmic\n')
        f.write('X axis Minimum Value,%s\n' % (x_axis_minimum))
        f.write('X axis Maximum Value,%s\n' % (x_axis_maximum))
        if y_axis_ID_scale == str(1):
            f.write('Y axis ID is Linear\n')
        else: 
            f.write('Y axis ID is Logarithmic\n')
        f.write('Y axis ID Minimum Value,%s\n' %(y_axis_ID_minimum))
        f.write('Y axis ID Maximum Value,%s\n' % (y_axis_ID_maximum))
        if y_axis_IG_scale == str(1):
            f.write('Y axis IG is Linear\n')
        else: 
            f.write('Y axis IG is Logarithmic\n')
        f.write('Y axis IG Minimum Value,%s\n' % (y_axis_IG_minimum))
        f.write('Y axis IG Maximum Value,%s\n' % (y_axis_IG_maximum))
        f.write('\n')

def update_file(path,info,data):
    with open(path,'a') as f:
        f.write(info[0])
        f.write(', ')
        f.write(info[1])
        f.write(', ')
        f.write(info[2])
        f.write(', ')
        # this is a silly thing to do as we are writing an
        # entire matrix in one file operation
        for i in range(len(data)):
           f.write(", %.16G" % data[i])
        #f.write(
        #    ", ".join("%.16G" % x_i for x_i in data)
        #)
        f.write('\n')

## File setup methods matrix
def initialise_matrix_file(path,info):
    """

    """
    with open(path,'w') as f:
	f.write('Carbon Nanotube Semiconductor Analysis\n')
	f.write('Date of experiment:,%s\n' % (timeStampDDMMYYYY()))
	f.write('Time of experiment:,%s\n' % (timeStampHHMMSS()))
	f.write('\n')
	f.write('Sample:\n%s\n' % (SAMPLE))
	f.write('\n')
	f.write('Device being measured\n')
	f.write('FET\n')
	f.write('\n')
	f.write('VG\n')
	f.write(' ,%s,to,%s,in,%s,step(s)\n' % (float(VG_const),(float(VG_const)+(float(VG_step)*float(Cycles))),float(VG_step)))
	f.write('VDS\n')
	f.write(' ,%s,to,%s,in,%s,step(s)\n' % (float(VDS_const),(float(VDS_const)+(float(VDS_step)*float(Cycles))),float(VDS_step)))
	f.write('\n')
	# f.writelines(info)
        # f.write('\n')
        # f.write('Directory,%s\n' % (str(ROOT)))
        # f.write('Sample,%s\n' % (SAMPLE))
        # f.write('Conditions,%s\n' % (CONDITIONS))
	# f.write('Script Type,Timed')
        # f.write('Sweep Mode,%s\n' % (sweep_mode))
	# f.write('Sweep direction,%s\n' % (sweep))
        # f.write('Number of Cycles,%s\n' % (Cycles))
        # f.write('VDS Initial Value,%s\n' % (VDS_const))
        # f.write('VDS Increment Value,%s\n' %(VDS_step))
        # f.write('VDS Final Cycle Value,%s\n' % (float(VDS_const) + (float(VDS_step)*float(Cycles))))
        # f.write('ID Compliance Value,%s\n' % (ID_compliance))
        # f.write('VG Value,%s\n' % (VG_const))
        # f.write('VG Increment Between Cycles,%s\n' %(VG_step))
        # f.write('VG Final Cycle Value,%s\n' % (float(VG_const) + (float(VG_step)*float(Cycles))))
        # f.write('IG Compliance Value,%s\n' % (IG_compliance))
	# f.write('Wait Time,%s\n' % (waitTime))
	# f.write('Interval Time,%s\n' % (intervalTime))
	# f.write('Number of Readings,%s\n' % (numReadings))
    #    if x_axis_scale == str(1):
    #        f.write('X axis is Linear\n')
    #    else: 
    #        f.write('X axis is Logarithmic\n')
    #        f.write('X axis Minimum Value,%s\n' % (x_axis_minimum))
    #        f.write('X axis Maximum Value,%s\n' % (x_axis_maximum))
    #    if y_axis_ID_scale == str(1):
    #        f.write('Y axis ID is Linear\n')
    #    else: 
    #        f.write('Y axis ID is Logarithmic\n')
    #        f.write('Y axis ID Minimum Value,%s\n' %(y_axis_ID_minimum))
    #        f.write('Y axis ID Maximum Value,%s\n' % (y_axis_ID_maximum))
    #    if y_axis_IG_scale == str(1):
    #        f.write('Y axis IG is Linear\n')
    #    else: 
    #        f.write('Y axis IG is Logarithmic\n')
    #        f.write('Y axis IG Minimum Value,%s\n' % (y_axis_IG_minimum))
    #        f.write('Y axis IG Maximum Value,%s\n' % (y_axis_IG_maximum))
    #    f.write('\n')

def update_matrix_file(path,info,data):
    with open(path,'a') as f:
        #f.write(info[0])
        #f.write(', ')
        #f.write(info[1])
        #f.write(', ')
        #f.write(info[2])
        #f.write(', ')
        #f.write(", ".join("%.16G" % x_i for x_i in data))
        for i in range(len(data)):
           f.write(", %s" % data[i])

        # this is a silly thing to do, as we are
        # writing a whole matrix to disk in one operation
	#f.write(", ".join("%s" % x_i for x_i in transpose_matrix[i]))
        f.write('\n')

## simplified script to control the Agilent Parameter Analyser
## this script just throws GPIB commands into the parameter analyser
## it could cause USB buffer overflow errors on the GPIB converter unit

## Initialise each file
string_YMDH=timeStampYMDH();
filename_Id = "%s_%s_Id_%s.txt" % (SAMPLE,CONDITIONS,string_YMDH)
filename_Ig = "%s_%s_Ig_%s.txt" % (SAMPLE,CONDITIONS,string_YMDH)
filename_matrix = "%s_%s_matrix_%s.txt" % (SAMPLE,CONDITIONS,string_YMDH) 

path_Id = os.path.join(ROOT,filename_Id)
path_Ig = os.path.join(ROOT,filename_Ig)
path_matrix = os.path.join(ROOT,filename_matrix)

print path_Id
print path_Ig
print path_matrix


info_string="%s: Const VG: %s VS: %s V to %s V \n" % (
    filename_Id, 
    VG_const,
    VDS_const,
    (float(VDS_const) + (float(VDS_step)*float(Cycles)))
    
)
    
string_xlTimeStamp=xlTimeStamp()
Header_string="Start time,%s, \n" % (string_xlTimeStamp)

initialise_file(
    path_Id,
    (info_string,Header_string)
)
initialise_file(
    path_Ig,
    (info_string,Header_string)
)
initialise_matrix_file(
    path_matrix,
    (info_string,Header_string)
)    
## simplified script to control the Agilent Parameter Analyser
## this script just throws GPIB commands into the parameter analyser
## it could cause USB buffer overflow errors on the GPIB converter unit

## Start Analyser object
## -------------------------------------
class Analyzer(object):
	def __init__(self,analyzer):
		self.analyzer = analyzer
		self.timeout = 3600
		## self.chunk_size = 1024 # 300kByte
		## self.timeout = None # 5minute timeout
                self.term_chars = CR+LF
		self.wait = 1 # wait one second between commands

	def device_clear(self):
		vpp43.clear(self.analyzer.vi)	# Clear parameter analyser errors
						
	def write(self,x):
                try:
                    self.problem()
                except:
                    print "Exception Caught when sending %s" %(x)
                    sys.exit()
		self.analyzer.write(x)		# Write data to the parameter analyser		
		time.sleep(self.wait)
                try:
                    self.problem()
                except:
                    print "Exception caught after sending %s" %(x)
                    sys.exit()

	def read(self):
		self.problem()
		result = self.analyzer.read()	# read data from the parameter analyser
		time.sleep(self.wait)
		self.problem()
		return result

	def spoll(self):
		return vpp43.read_stb(self.analyzer.vi) # check the status flag

	def problem(self):
		# print "reached problem call" # check that weve got this far
		sp = self.spoll()
		if sp & 2**6:
			print_error(sp)
			raise RuntimeError("SRQ Detected")

	def wait_for_clear(self):
		#while self.spoll() & 1:
                while self.spoll() & 1:
			sys.stdout.write('*')
			time.sleep(self.wait)
		print

	def wait_for_ready(self):
		while not self.spoll() & 1:
                        if pump_disabled == 0:
                            ser.write("s"+CRLF)
                            status_string = sio.readline()
                            status()
                        else:
                            sys.stdout.write('.') # Update the screen to inform user of progress
			time.sleep(self.wait)
		print
	def ask_for_values(self,msg):
            ## I've removed the try from here
            ## I've placed it outside the command
            ## then I can perform a reconnection
            ## and assign the device back once a connection
            ## is established
            ## seq = list() 
            print "numReadings s:%s d:%d" % (numReadings,int(numReadings))
            ## print self.spoll()
            try:
                self.analyzer.write(msg)
            except:
                print "Timeout Attempting to obtain values"
            ## print self.spoll()
            try:    
                ## i = 1;
                seq = self.analyzer.read_values()
                print len(seq)
                ## if(len(seq) > 1575*i):
                ##    print "Difference = %d" %(len(seq) - 1575*i)
                ##    for x in range(0:i):
                ##        print seq(end:) ## this line is wrong
                ## print self.spoll()
                # If there is data in the buffer still
                # we need to obtain this data also
                while len(seq) < int(numReadings):
                    ## delete the last obtained value
                    ## for the end value append an exponent
                    seq = seq + self.analyzer.read_values()
                    print "Length: %s" %len(seq)
                     
                    ## print self.spoll()
            except:
                print "Could not obtain data, so sorry"
            print 'end read'
            self.wait_for_clear()
            self.problem()
            return seq
    
		

##-------------------------------------------
## Finished Analyzer

#===================================================
# Pump Controller Setup!
if pump_disabled == 0:
    print "Pressure Pump Controller\n"
    try:
        ser = serial.Serial(COM,57600,timeout=2) # pump com port
    except:
        print "COM%s not found. Aborting communication with pressure pump!" % (COM+1)
        pump_disabled = 1
    if pump_disabled == 0:
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser)) # serial data reply wrapper
else:
    print "Pressure Pump Disabled\n"
LF = serial.to_bytes([10])
CR = serial.to_bytes([13])
CRLF = serial.to_bytes([13, 10])
start_char = 0
end_char = 0
# Status Interpreter
def status_decode(status_string,start,end):
	while status_string[end] != ",":
		end = end + 1
	code = status_string[start:end]	
	start = end + 1
	end = end + 2
	return [code,start,end]
	
def status():
	[error_code,start_char,end_char] = status_decode(status_string,2,3)
	[pump_state,start_char,end_char] = status_decode(status_string,start_char,end_char)
	[remote_state,start_char,end_char] = status_decode(status_string,start_char,end_char)
	[chamber_pressure,start_char,end_char] = status_decode(status_string,start_char,end_char)
	[supply_pressure,start_char,end_char] = status_decode(status_string,start_char,end_char)
	[target_pressure,start_char,end_char] = status_decode(status_string,start_char,end_char)
	print "Error Code: %s %s" % (error_code,Errors(error_code))
	print "Pump state: %s %s" % (pump_state,States(pump_state))
	print "Remote state: %s %s" % (remote_state,Remote(remote_state))
	print "Chamber Pressure: %s mbar" % chamber_pressure
	print "Supply Pressure: %s mbar" % supply_pressure
	print "Target Pressure: %s mbar" % target_pressure
	return[error_code,pump_state,remote_state,chamber_pressure,supply_pressure,target_pressure]
	
def Errors(x):
	return{
		'0': "no error",
		'1': "Supply pressure: too high",
		'2': "Tare: timeout",
		'3': "Tare: Supply still connected",
		'4': "Control: timeout",
		'5': "Target Pressure: too low",
		'6': "Target Pressure: too high",
		'7': "Leak test: Supply too low",
		'8': "Leak test: timeout",
		'100': "Fatal Error: Service needed on pressure pump"}[x]
		
def Remote(x):	
	return{
		'0': "Manual control mode",
		'1': "Remote control mode"}[x]
		
def States(x):
	return{
		'0': "Idle",
		'1': "Controlling",
		'2': "Tare",
		'3': "Error",
		'4': "Leak Test"}[x]

##-------------------------------------------

#===================================================
# Enter remote
if pump_disabled == 0:
    print "\n================================="

    #print "Serial Write A1"
    ser.write("A1"+CRLF)
    reply = sio.readline()
    #print reply
    if reply == "#A0%c"%LF:
            print "Entered Remote Mode"
            pump_disabled = 0
    else:
            print "Failed to Enter Remote Mode"
            pump_disabled = 1
            # May want to exit here? 
            # Disable pressure pump usage.
    #print "=================================\n"
# Clear status bit
if pump_disabled == 0:
    #print "\n================================="
    ser.write("C"+CRLF)
    #print "Clearing error conditions.\n"
    reply = sio.readline()
    if reply == "#C0%c"%LF:
            print "Status Cleared, Pump Idle"
    else:
            print "Failed to clear status"
    #print "=================================\n"
    #===================================================

    #===================================================  
    # Get pump information
    #print "\n================================="
    ser.write("v"+CRLF)
    version = sio.readline()
    print "Version: %s" % version[2:]
    ser.write("n"+CRLF)
    serial = sio.readline()
    print "Serial: %s" % serial[2:]
    #print "=================================\n"
    #=================================================== 

    #===================================================
    # Pump status
    #print "\n================================="
    ser.write("s"+CRLF)
    status_string = sio.readline()
    #print status_string[2:]
    status()			
    #print "=================================\n"
    #===================================================

    #===================================================
    # Set Pressure
    #print "\n================================="
    ser.write("P%d" % pressure +CRLF)
    reply = sio.readline()
    if reply == "#P0%c"%LF:
            print "Pressure Set OK\n"
    else:
            print "Failed to Set Pressure\n"
    # Check the status compare chamber pressure to target pressure
    # If the pressure has not reached target pressure within 60 seconds, vent the chamber and exit
    time.sleep(wait_time)
    ser.write("s"+CRLF)
    status_string = sio.readline()
    #print status_string[2:]
    status()
    print "=================================\n"
    #===================================================

## Open the GPIB bus
## Perform initial device setup
print "Initialising the Parameter Analyser"		
try:
    HP4145B = visa.instrument("GPIB::02") ## 4145 Code
    HP4145B.timeout = 60
    HP4145B.term_char = CR+LF
    HP4145B.delay = 1
    ## Clear the device errors
    HP4145B.clear()
    ## Check communications
    print "Parameter Analyser ID:"
    print HP4145B.ask("ID") ## 4145 Code
    # HP4155B.write("*IDN?") ## 4155 Code
except:
    print "Could not connect to the Parameter Analyser!"
    sys.exit()

## Setup Program parameters
HP4145B.write("IT1 CA1 DR1 BC") ## testing integration time issues

## Setup Channel Definitions
HP4145B.write("DE CH1,'VS','IS',3,3;CH2,'VDS','ID',1,3;CH3,'VG','IG',1,3;CH4;")

## Setup Measurement display
HP4145B.write("SM DM1 XT %s,%s; YA 'ID',%s,%s,%s; YB 'IG',%s,%s,%s" % (x_axis_minimum,x_axis_maximum,y_axis_ID_scale,y_axis_ID_minimum,y_axis_ID_maximum,y_axis_IG_scale,y_axis_IG_minimum,y_axis_IG_maximum))

# 0.0 T_stop y1min y1max y2min y2max

## Check error flag
## sp = HP4145B.spoll()
sp = HP4145B.stb
if sp != 0:
	print "Instrument state problem, spoll = %s" % hex(sp)
	print_error(sp)
	sys.exit()
# record start time
start_time = time.clock()
# Data Acquisition loop
Mode = ModeCycle(Time_between_cycles)
data = ''
for i in xrange(Cycles):
    print "cycle: %i of %i" % (i,Cycles)
    
    Mode.begin()	
    ## Setup Variable Source
    HP4145B.write("SS VC 2,%s,%s" % (VDS_const,ID_compliance)) # VDS_const, ID_COMPLIANCE
    ## Setup Constant Source
    HP4145B.write("SS VC 3,%s,%s" % (VG_const,IG_compliance)) # VG_constant IG_compliance
    ## Setup Time base
    HP4145B.write("SM WT %s;IN %s;NR %s" % (waitTime,intervalTime,numReadings)) # wait_time interval_time number_of_readings
    ## Device Clear Before Reading Values
    HP4145B.write("BC")
    time_since_start = str(time.clock()-start_time)
    T_start_sweep = time.clock()
    ## Start Measurements
    HP4145B.write("MD ME1")
    ## HP4145B.wait_for_ready()
    ## Wait until measurements finished
    while not HP4145B.stb & 1:
        if pump_disabled == 0:
            ser.write("s"+CRLF)
            status_string = sio.readline()
            status()
        else:
            sys.stdout.write('.') # Update the screen to inform user of progress
        time.sleep(HP4145B.delay)
    print
    # Get measured values
    ## I've inserted a try here incase of a
    ## GPIB timeout this is not ideal and marely a hack
    ## to see if I can perform a reconnection in case
    ## the GPIB bus times out during transfer
    ## ID_down=HP4145B.ask_for_values("DO 'ID'")
    ## IG_down=HP4145B.ask_for_values("DO 'IG'")
    ## Trial replacement for ask_for_values
    try:
        visa.instrument("GPIB::02").write("DO 'ID'")
    except:
        print("Timeout processing DO 'ID'")
    ID_down = visa.instrument("GPIB::02").read_values()
    try:
        visa.instrument("GPIB::02").write("DO 'IG'")
    except:
        print("Timeout processing DO 'IG'")
    IG_down = visa.instrument("GPIB::02").read_values()
    ## End of trial replacement for ask_for_values
    msg = Mode.message
    T_stop_sweep = time.clock()
    time_for_sweep = str(T_stop_sweep - T_start_sweep)
    update_file(path_Id,(time_since_start,time_for_sweep,"ID %s" % msg),ID_down)
    update_file(path_Ig,(time_since_start,time_for_sweep,"IG %s" % msg),IG_down)
    print "Number of time values %d" % len(ID_down)
    number_time_values = len(ID_down)
    
    ID_down.insert(0,'ID')
    IG_down.insert(0,'IG')

    print 'sweep time', time_for_sweep
    # Print Valuesti
    # print ID_down
    # print IG_down
	# ID_down and IG_down are just comma separated values
	# for numpy to be able to manipulate the data we need to be able to push it into an array
	# The array size will be the number of cycles x number of readings
    # Save values to disk

    # update_file(path_Id,(time_since_start,time_for_sweep,"ID %s" % msg),ID_down)
    # update_file(path_Ig,(time_since_start,time_for_sweep,"IG %s" % msg),IG_down)
    # data = data + ID_down + '\n' + IG_down + '\n'
    #print data
    # print ID_down[x]
    Time = ['Time',T_start_sweep]
    Time_step = (T_stop_sweep - T_start_sweep) / number_time_values  
    for j in range(1,number_time_values):
            Time.append(T_start_sweep + (j * Time_step))
    print "Time length %d" % len(Time)
    print "ID_down length %d" % len(ID_down)
    print "IG_down length %d" % len(IG_down)
    matrix.append(Time)
    matrix.append(ID_down)
    matrix.append(IG_down)
    print 'matrix length %d' % len(matrix)
    transpose_matrix = zip(*matrix)
    print '\n'
    print 'transpose matrix length = %d ' % len(transpose_matrix)
    # the problem here is we don't want to transpose the matrix until we exit
    # should we transpose the matrix in the exit loop?
    # should we transpose the matrix after the cycle for loop?
    # print transpose_matrix
    if i == Cycles - 1:
            for i in range(0,len(transpose_matrix)):	
                    update_matrix_file(path_matrix,(time_since_start,time_for_sweep,"ID %s" % msg),transpose_matrix[i])
	# how do you post processs this information after a quit command?
	# processing the information on the fly is difficult, hence we do it line by line
	# if the information is stored in a variable transposed
	# then every cycle the transposed variable is overwritten with new transposed data
	# this could overcome the problem with transposing the data before a quit
	# We need to a be able to produce a separate file with the data
	# or a lot of the code in this script needs to be repeated
	# which is kinda pointless.
    # cycle * 3 for the matrix row time base
    # cycle * 3 + 1 for the matrix row Id y-axis
    # cycle * 3 + 2 for the matrix row Ig y-axis
    # for row 1 to x
    # row x = row x + ID_down / IG_down up to delimiter	
    # end for
    # Increment constant values between cycles if required
    VDS_increment = float(VDS_const) + float(VDS_step)
    VDS_const = str(VDS_increment)
    VG_increment = float(VG_const) + float(VG_step)
    VG_const = str(VG_increment)
    if prompt_between_cycles != 0:
	    print 'Press Enter to continue, or ctrl+c to exit'
	    raw_input()
    
    # Exit nicely
    if check_escape(): sys.exit()

    Mode.end()
print("Data obtained, Exiting")
if pump_disabled == 0:
    #===================================================
    # Vent Chamber
    #print "\n================================="
    ser.write("P0"+CRLF)
    pressure = sio.readline()
    if pressure == "#P0%c"%LF:
            print "Pressure set to zero, venting\n"
    else:
            print "Unable to vent, chamber still pressurised!\n"
    #time.sleep(wait_time)
    ser.write("s"+CRLF)
    status_string = sio.readline()
    #print status_string[2:]
    status()
    #print "=================================\n"
    #===================================================

    #===================================================
    # Exit remote
    #print "\n================================="
    print "Exit Remote Mode: "
    ser.write("A0"+CRLF)
    reply = sio.readline()
    if reply == "#A0%c"%LF:
            print "Success"
    else:
            print "Failure"
    #print "=================================\n"
    #===================================================

    #===================================================
    # Clear up
    #print "\n================================="
    print "Clear status bits"
    ser.write("C"+CRLF)
    #print "=================================\n"
    #===================================================
