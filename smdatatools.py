import argparse
import configparser
import sys
import time
from os.path import isdir, join

from smdatatools.common.cli_options import Options

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Stepmania Data Tools')
    parser.add_argument('-pt', '--parsetxt', type=str, nargs='?', default=None, help='Parse data from .txt files (add a directory to this arg to override the config)')
    parser.add_argument('-ps', '--parsesm',  type=str, nargs='?', default=None, help='Parse data from .sm files  (add a directory to this arg to override the config)')
    parser.add_argument('-wt', '--writetxt', type=str, nargs='?', default=None, help='Write data to .txt files   (add a directory to this arg to override the config)')
    parser.add_argument('-ws', '--writesm',  type=str, nargs='?', default=None, help='Write data to .sm files    (add a directory to this arg to override the config)')
    args = parser.parse_args()
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    dir_txt_input  = config.get('dir', 'parsetxt') if (args.parsetxt == None) else args.parsetxt
    dir_sm_input   = config.get('dir', 'parsesm')  if (args.parsesm  == None) else args.parsesm
    dir_txt_output = config.get('dir', 'writetxt') if (args.writetxt == None) else args.writetxt
    dir_sm_output  = config.get('dir', 'writesm')  if (args.writesm  == None) else args.writesm

    if not isdir(dir_txt_input) or not isdir(dir_sm_input):
        print('Input .txt or .sm directory not found. Check user entry or configuration, and that the directories exist.')
        sys.exit()
    if not isdir(dir_txt_output) or not isdir(dir_sm_output):
        print('Output .txt or .sm directory not found. Check user entry or configuration, and that the directories exist.')
        sys.exit()
    
    start_time = time.time()

    options = Options()
    
    if args.parsetxt is not None:
        print("Parsing .txt files from %s" % dir_txt_input)
        options.getFilePaths(dir_txt_input, '.txt')
        for file in options.txt_filepaths:
            print("  - Parsing %s" % file)
            options.data.append(options.read_TXTtoData(file))

    if args.parsesm is not None:
        print("Parsing .sm files from %s" % dir_sm_input)
        options.getFilePaths(dir_sm_input, '.sm')
        for file in options.sm_filepaths:
            print("  - Parsing %s" % file)
            options.data.append(options.read_SMtoData(file))

    if args.writetxt is not None:
        print("Writing data to .txt files in %s" % dir_txt_output)
        for data in options.data:
            output_path = join(dir_txt_output, data.filename + '.txt').replace("\\","/")
            print("  - Writing to %s" % output_path)
            options.write_DatatoTXT(data, output_path)
            
    if args.writesm is not None:
        print("Writing data to .sm files in %s" % dir_sm_output)
        for data in options.data:
            data.process_data_to_sm_format()
            output_path = join(dir_sm_output, data.filename + '.sm').replace("\\","/")
            print("  - Writing to %s" % output_path)
            options.write_DatatoSM(data, output_path)
    
    end_time = time.time()
    print("Elapsed time was %g seconds" % (end_time - start_time))
