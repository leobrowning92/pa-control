import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
print os.listdir(".")
print os.getcwd()
os.chdir("raw")
print os.getcwd()
os.chdir("..")
print os.getcwd()
