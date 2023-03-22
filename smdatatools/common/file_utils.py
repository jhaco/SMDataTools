from os import walk
from os.path import join, split, splitext
from re import sub

def read_file(filename):
    file_data = []
    with open(filename, encoding='ascii', errors='ignore') as f:
        file_data = f.read().splitlines()
    return file_data

def write_file(output_data, filename):
    with open(filename, 'w') as f:
        f.write(output_data)

def strip_filename(filename):
    '''
    Strips file path
    Strips file extension
    Reformats to lowercase alphanumerics only, except '-' and '_'
    Replaces whitespace with '_'
    '''
    head, tail = split(filename) # handles possible filepaths that end with a slash
    tail = splitext(tail)[0]
    return sub(' ', '_', sub('[^a-z0-9-_ ]', '', tail.lower()))

def collect_filenames(input_dir, extension):
    filenames = []
    for root, dirs, files in walk(input_dir):
        for filename in files:
            if filename.endswith(extension):
                filenames.append(join(root, filename).replace("\\","/"))
    return filenames

def getFilePaths(input_dir, extension):
    filepaths = collect_filenames(input_dir, extension)

    if(extension == '.sm'):
        checkFilePaths(filepaths)

    return filepaths

def checkFilePaths(sm_filepaths):
    # checks for static bpm in the .sm file
    # and removes filepath from list if not
    for sm_file in sm_filepaths:
        with open(sm_file, encoding='ascii', errors='ignore') as f:
            for line in sm_file:
                if line.startswith('#BPMS:'):
                    if ',' in line: # indicates multiple BPMs (non-static)
                        sm_filepaths.remove(sm_file)
                    break