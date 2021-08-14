import platform, os, subprocess, shutil
from .path import subDirAndFiles

def openFile(filepath):
	"""Use system application to open a file"""
	# https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
	if platform.system() == 'Darwin':       # macOS
		subprocess.call(('open', filepath))
	elif platform.system() == 'Windows':    # Windows
		os.startfile(filepath)
	else:                                   # linux variants
		subprocess.call(('xdg-open', filepath))

def clearDir(dir_path: str):
	assert os.path.isdir(dir_path), "Input path is not a directory, clearDir function only accept directory path as input argument"
	for p in subDirAndFiles(dir_path):
		if os.path.isdir(p):
			shutil.rmtree(p)
		else:
			os.remove(p)
		print("{} cleared.".format(dir_path))