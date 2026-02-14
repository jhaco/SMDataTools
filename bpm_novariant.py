from os import walk
from os.path import join, splitext, dirname, realpath
import shutil

def get_folders_to_delete() -> list[str]:
	to_delete  = []
	dir_path = dirname(realpath(__file__))
	print(dir_path)
	for root, dirs, files in walk(dir_path):
		for filename in files:
			fname, fext = splitext(filename)
			if fext == '.sm':
				sm_file = join(root, filename).replace("\\","/")
				with open(sm_file, encoding='ascii', errors='ignore') as f:
					for line in f:
						if line.startswith('#BPMS:'):
							if ',' in line: # indicates multiple BPMs (non-static)
								# add its parent folder
								parent_dir = dirname(sm_file).replace("\\","/")
								to_delete.append(parent_dir)
								break
							elif ';' not in line: # indicates there might be more BPMs or weird formatting
								if ',' in next(f): # check next line
									# add its parent folder
									parent_dir = dirname(sm_file).replace("\\","/")
									to_delete.append(parent_dir)
									break
								break
	return to_delete

if __name__ == '__main__':
	'''
		Goal: This script will aggressively search and
		delete all folders within the same directory 
		that meets the following conditions:
			1. contains a .sm file
			2. contains varying BPM parameters
		Please do not tempt the tool by dropping a
		varying BPM .sm file into something important
		or it will nuke the folder there too and
		everything in it.

		Usage: Drop this nuke into the PACK folder
		you want to clean, and run it.
	'''
	sm_folders = get_folders_to_delete()
	print('Deleting the following: ')
	for folder in sm_folders:
		print(folder)

	val = input("Delete? (y/n): ")
	if val != 'y':
		exit()

	for folder in sm_folders:
		shutil.rmtree(folder)

	print('Successfully deleted %i files' % len(sm_folders))

