from os.path import splitext
from re import sub

def read_file(input_file):
    file_data = []
    with open(input_file, encoding='ascii', errors='ignore') as f:
        file_data = f.read().splitlines()
    return file_data

def write_file(formatted_data, output_file):
    with open(output_file, 'w') as f:
        f.write(formatted_data)

def format_file_name(file_name):
    '''
    Strips file extension
    Reformats to lowercase alphanumerics only, except '-' and '_'
    Replaces whitespace with '_'
    '''
    return sub(' ', '_', sub('[^a-z0-9-_ ]', '', splitext(file_name)[0].lower()))