import os, typing

pJoin = os.path.join
parDir = os.path.dirname

	
def subDirAndFiles(dir_path: str):
	assert os.path.isdir(dir_path), "Input path is not a directory, subFiles function only accept directory path as input argument"
	return [os.path.join(dir_path, f) for f in os.listdir(dir_path)]

def subFiles(dir_path: str):
	dir_and_file = subDirAndFiles(dir_path)
	return [i for i in dir_and_file if os.path.isfile(i)]

def subDirs(dir_path: str):
	dir_and_file = subDirAndFiles(dir_path)
	return [i for i in dir_and_file if os.path.isdir(i)]