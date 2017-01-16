# pa-control


## Overview


The idea of this project is to improve how we interface with the
Parameter analyzer, both for command and data handling, in order
to improve measurement efficiency

## Usage

* The file gui.bat is for running the gui on the lab computer (Windows 7).
the gui allows the saving of data from the parameter analyzer
* the run.sh file should be run on a linux machine via command as `$bash run.sh`
in order to post process the data




## To Do
in no particular order
- [NEEDS TESTING IN LAB]change file naming to reflect the new file format:
AAAxxx\_devicex\_[productionstep]\_[FET/diode]\_[othernotes]\_timestamp.csv
which follows the format of chip name iterator needs to be tested with the changes.

- [DONE]change data structure to have a single data folder for each batch of chips
that contains all of the data for those chips.

- [DONE}have cleandata able to handle data that has already been cleaned in the same
folder as new data.
- [DONE]incorporate the nameiterator into the gui script.
- [DONE]have the post process script generate a log file using something like `./script.py > <filename>`
which would pipe the output of the scripts to a log file as well. maybe run the process script
from a batch file like the gui so that this is consistent? can try `$python script.py | tee -a log.txt
` note: the tee command saves to a file and also pipes to stdout (prints to terminal) the -a appends.
- [DONE]need to have the FET data plotted as both log and linear in the same figure
- [ONGOING]make sure titles and labels for plots are not squished
- have the post process also generate a pdf with all of the plots in it for previewing.
Unsure as to formatting at the moment
- need to have the post process script generate a csv with key chip metrics such as
    - max and minimum Current
    - on/off current ratio (may differ from max and min ratio as max and min include spikes)
    - resistance for diode measurements
    - threshold Voltage
    - hysteresis
