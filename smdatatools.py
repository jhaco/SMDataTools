import argparse
import configparser
import sys
import time
from os.path import isdir, join

from smdatatools.common.cli_options import Options
from smdatatools.common.file_utils import getFilePaths

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Stepmania Data Tools')
    parser.add_argument('-pt', '--parsetxt', type=str, nargs='?', default=argparse.SUPPRESS, help='Parse data from .txt files (add a directory to this arg to override the config)')
    parser.add_argument('-ps', '--parsesm',  type=str, nargs='?', default=argparse.SUPPRESS, help='Parse data from .sm files  (add a directory to this arg to override the config)')
    parser.add_argument('-wt', '--writetxt', type=str, nargs='?', default=argparse.SUPPRESS, help='Write data to .txt files   (add a directory to this arg to override the config)')
    parser.add_argument('-ws', '--writesm',  type=str, nargs='?', default=argparse.SUPPRESS, help='Write data to .sm files    (add a directory to this arg to override the config)')
    args = parser.parse_args()
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    dir_txt_input = config.get('dir', 'parsetxt')
    if(hasattr(args, 'parsetxt')):
        if args.parsetxt:
            dir_txt_input = args.parsetxt

    dir_sm_input = config.get('dir', 'parsesm')  
    if(hasattr(args, 'parsesm')):    
        if args.parsesm:
           dir_sm_input = args.parsesm

    dir_txt_output = config.get('dir', 'writetxt') 
    if(hasattr(args, 'writetxt')):    
        if args.writetxt:
           dir_txt_output = args.writetxt

    dir_sm_output = config.get('dir', 'writesm') 
    if(hasattr(args, 'writesm')):    
        if args.writesm:
           dir_sm_output = args.writesm

    if not isdir(dir_txt_input) or not isdir(dir_sm_input):
        print('Input .txt or .sm directory not found. Check user entry or configuration, and that the directories exist.')
        sys.exit()
    if not isdir(dir_txt_output) or not isdir(dir_sm_output):
        print('Output .txt or .sm directory not found. Check user entry or configuration, and that the directories exist.')
        sys.exit()
    
    start_time = time.time()

    dataList = [] # to contain a list of DataHandler object classes
    
    if hasattr(args, 'parsetxt'):
        print("Parsing .txt files from %s" % dir_txt_input)
        txt_filepaths = getFilePaths(dir_txt_input, '.txt')
        for file in txt_filepaths:
            print("  - Parsing %s" % file)
            dataList.append(Options.read_TXTtoData(file))

    if hasattr(args, 'parsesm'):
        print("Parsing .sm files from %s" % dir_sm_input)
        sm_filepaths = getFilePaths(dir_sm_input, '.sm')
        for file in sm_filepaths:
            print("  - Parsing %s" % file)
            dataList.append(Options.read_SMtoData(file))

    if hasattr(args, 'writetxt'):
        print("Writing data to .txt files in %s" % dir_txt_output)
        for data in dataList:
            output_path = join(dir_txt_output, data.filename + '.txt').replace("\\","/")
            print("  - Writing to %s" % output_path)
            Options.write_DatatoTXT(data, output_path)
            
    if hasattr(args, 'writesm'):
        print("Writing data to .sm files in %s" % dir_sm_output)
        for data in dataList:
            data.process_data_to_sm_format()
            output_path = join(dir_sm_output, data.filename + '.sm').replace("\\","/")
            print("  - Writing to %s" % output_path)
            Options.write_DatatoSM(data, output_path)
    
    end_time = time.time()
    print("Elapsed time was %g seconds" % (end_time - start_time))
