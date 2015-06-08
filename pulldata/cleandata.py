import PAplot
import os
import numpy as np




def clean_data():
	"""Cleans the raw data that comes in from download_data_as_matrix.py which
		has an extra comma at the start of each row. and an extra space at the end.
		data should be at the  """

	
	try:
		skip=1
		delim=','

		if os.path.isdir("data")==False:
		        os.mkdir("data")

		rawdirectory="raw/"
		savedirectory="data/"
		filenames=os.listdir("raw")
		rawpaths=[]
		savepaths=[]




		#print(data)
		for path in filenames:
			lines=[]
			with open("raw/"+path,"r") as f:
				for line in f:
					lines.append(line[2:-1]) #removes extra ',' at the start of each data row

			with open("data/"+path,'w') as g:
				
				
				
					for line in lines:
						#checks for 9.91e+99 which is what is appended after compliance is hit 
						if line.startswith('9.91e+99') == False:
							g.write(line+"\n")

			np.loadtxt("data/"+path,skiprows=skip,delimiter=delim,dtype=float)

	except:
		print("Please insure the raw data from the script download_data_as_matrix.py")
		print( "is in a folder called raw in the working directory")



