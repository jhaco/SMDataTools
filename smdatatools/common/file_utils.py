from os import walk
from os.path import join, split, basename
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
    return sub(' ', '_', sub('[^a-z0-9-_ ]', '', basename(head).lower()))

def collect_filenames(input_dir, extension):
    filenames = []
    for root, dirs, files in walk(input_dir):
        for filename in files:
            if filename.endswith(extension):
                filenames.append(join(root, filename))
    return filenames