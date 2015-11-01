import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

#active loop

basename = input('Please input your file name with [ITER]\n \
                    in the region that you would like an iterator : ')


while True:
	command = input("input : ")


	if command =='q':
		break

	else:
		pass
print('Session Terminated')
