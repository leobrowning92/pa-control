#!/var/run/python
# Agilent Parameter Analyser Sweep function script.
import sys
import io
import visa
import os
###############################################
## Class definitions and defines
###############################################
from hp4156c import hp4156c
###############################################
## Code starts here
###############################################
def initialize_device():
    """Initialise the device and resets. returns the resetted device"""
    device = hp4156c()
    device.get_error()
    device.reset()
    device.get_error()
    print("=>Device Initialized")
    return device

def define_transfer_smu(device):
    device.measurementMode("SWEEP","MEDIUM")
    device.get_error()
    device.smu("SMU1",["VS","CONS","IS","COMM"])
    device.get_error()
    device.smu("SMU2",["VDS","VAR2","ID","V"])
    device.get_error()
    device.smu("SMU3",["VG","VAR1","IG","V"])
    device.get_error()
    device.disableSmu(["SMU4"])
    device.get_error()
    print("=>SMU's assigned")
def define_output_smu(device):
    device.measurementMode("SWEEP","MEDIUM")
    device.get_error()
    device.smu("SMU1",["VS","CONS","IS","COMM"])
    device.get_error()
    device.smu("SMU2",["VDS","VAR1","ID","V"])
    device.get_error()
    device.smu("SMU3",["VG","VAR2","IG","V"])
    device.get_error()
    device.disableSmu(["SMU4"])
    device.get_error()
    print("=>SMU's assigned")
def measure_transfer(device, fname, savedir, vg_start, vg_stop, vg_step, vds_start, vds_step, vds_num):
    device.var("VAR1",["LIN","DOUB",str(vg_start),str(vg_step),str(vg_stop),"1e-3"])
    device.get_error()
    #note, VAR2 is always linear
    device.var("VAR2",["LIN","SING",str(vds_start),str(vds_step),str(vds_num),"1e-3"])
    device.get_error()
    device.visualiseTwoYs(["VG","LIN",str(vg_start),str(vg_stop)], ["ID","LOG","1e-11","1e-6"], ["IG","LIN","-1e-8","1e-8"])
    device.get_error()
    print("=>Sweep Parameters set")
    device.single()
    device.get_error()
    if "[INFO]"in fname:
        if vds_step==0:
            fname = fname.replace("[INFO]", "transferVG" + str(abs(vg_start)) + "VDS" + str(abs(vds_start)))
        else:
            fname = fname.replace("[INFO]", "transferVG" + str(abs(vg_start)) + "VDS" + str(abs(vds_start)) + "+" + str(vds_num) + "x" + str(abs(vds_step)))
    device.collect_data(['VG', 'VDS', 'ID', 'IG'],fname,savedir)
    device.get_error()
    print("=>Data Finished Collecting")

def measure_output(device, fname, savedir, vds_start, vds_stop, vds_step, vg_start, vg_step, vg_num):
    device.var("VAR1",["LIN","DOUB",str(vds_start),str(vds_step),str(vds_stop),"1e-3"])
    device.get_error()
    device.var("VAR2",["LIN","SING",str(vg_start),str(vg_step),str(vg_num),"1e-3"])
    device.get_error()
    device.visualiseTwoYs(["VDS","LIN",str(vds_start),str(vds_stop)], ["ID","LIN","-1e-6","1e-6"], ["IG","LIN","-1e-8","1e-8"])
    device.get_error()
    print("=>Sweep Parameters set")
    device.single()
    device.get_error()
    if "[INFO]"in fname:
        if vds_step==0:
            fname = fname.replace("[INFO]", "outputVDS" + str(abs(vds_start)) + "VG" + str(abs(vg_start)))
        else:
            fname = fname.replace("[INFO]", "outputVDS" + str(abs(vds_start)) + "VG" + str(abs(vg_start)) + "+" + str(vg_num) + "x" + str(abs(vg_step)))
    device.collect_data(['VG', 'VDS', 'ID', 'IG'],fname,savedir)
    device.get_error()
    print("=>Data Finished Collecting")
def test_fet(fname="test_[INFO].csv",savedir=""):
    # Initialise the device
    device = initialize_device()
    define_transfer_smu(device)
    device.visualiseTwoYs(["VG","LIN","-10","10"], ["ID","LOG","1e-11","1e-6"], ["IG","LIN","-1e-8","1e-8"])
    device.get_error()
    measure_transfer(device, fname, savedir, -1, 1, 0.1, 0.1, 0, 1)




def diodesweep():
    # Initialise the device
    device = hp4156c()
    device.get_error()
    device.reset()
    device.get_error()
    ## Setup the device for a Diode Measurement
    device.measurementMode("SWEEP","SHORT")
    device.get_error()
    device.smu("SMU1",["VF","VAR1","IF","V"])
    device.get_error()
    device.smu("SMU3",["V","CONS","I","COMM"])
    device.get_error()
    device.disableSmu(["SMU2","SMU4"])
    device.get_error()
    device.var("VAR1",["LIN","DOUB","-1","0.1","1.0","100e-3"])
    device.get_error()
    device.visualise(["Voltage","1","-1","1"], ["Current","1","-0.1","0.1"])
    device.get_error()
    device.single()
    device.get_error()
    dataReturned = device.daq(["VF","IF"])
    device.get_error()
    print(device.data)
    device.get_error()
    #for saving
    #device.save_data(fname='test.csv')



if __name__ == "__main__":
    test_fet()
