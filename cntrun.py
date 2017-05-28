# designed to be run from terminal or interactive editor ie ipython
# runs a standard set of transfer and output measurements
# designed to characterize a backgated CNT FET on a silicon substrate

import parameter_analyser as pa
import sys
import time,datetime
def run_FET_series(fname, savedir):
    device = pa.initialize_device()
    pa.define_transfer_smu(device)
    start_time=time.time()
    pa.measure_transfer(device, fname, savedir, -10, 10, 0.1, 0.1, 0, 1)
    pa.measure_transfer(device, fname, savedir, -20, 20, 0.1, 0.1, 0, 1)
    pa.measure_transfer(device, fname, savedir, -10, 10, 0.1, 0.01, 0, 1)
    pa.measure_transfer(device, fname, savedir, -20, 20, 0.1, 0.01, 0, 1)
    pa.measure_transfer(device, fname, savedir, -10, 10, 0.1, 1, 1, 5)
    pa.define_output_smu(device)
    pa.measure_output(device, fname, savedir, -5, 5, 0.1, -20, 5, 9)
    end_time=time.time()
    print(str(datetime.timedelta(seconds=end_time-start_time)))
def download_data(values,fname,savedir):
    device = pa.initialize_device()
    device.collect_data(values, fname, savedir)


if __name__ == "__main__":
    run_FET_series("test_[INFO].csv","")
