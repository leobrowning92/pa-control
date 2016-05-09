# pa-control


##Overview


The idea of this project is to improve how we interface with the
Parameter analyzer, both for command and data handling, in order
to improve measurement efficiency




##To Do
in no particular order
- ~~change file naming to reflect the new file format:
COL123_device1_postdielectricFET_othernotes.csv
AAAxxx\_devicex\_[productionstep]_[FET/diode]\_[othernotes].csv~~
which follows the format of
chip name iterator needs to be tested with the changes.
- change directory structure of the scripts to have only a top level script
in the main folder with all supporting scripts in a subfolder
- change data structure to have a single data folder for each batch of chips
that contains all of the data for those chips.
- have each FET plot contain both the linear and log plot instead of seperate files
- ~~have the data file include a header with date~~ changed all the plotting calls
in postprocess to skip the date row.
- ~~have the data cleaning incorporated in the data pulling.~~
NEEDS TESTING ON THE PA SYSTEM
- ~~incorporate the nameiterator into the gui script.~~
- have the post process script generate a log file using something like `./script.py > <filename>`
which would pipe the output of the scripts to a log file as well. maybe run the process script
from a batch file like the gui so that this is consistent?
- have the post process also generate a pdf with all of the plots in it for previewing.
Unsure as to formatting at the moment
