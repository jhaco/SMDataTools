import argparse
import configparser
import sys
import time
from shutil import copyfile
from os.path import isdir, isfile, join, splitext

from smdatatools.common.cli_options import Options
from smdatatools.common.file_utils import getFilePaths, strip_filename

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Stepmania Data Tools')
    parser.add_argument('-pt', '--parsetxt', type=str, nargs='?', default=argparse.SUPPRESS, help='Parse data from .txt files (add a directory to this arg to override the config)')
    parser.add_argument('-ps', '--parsesm',  type=str, nargs='?', default=argparse.SUPPRESS, help='Parse data from .sm files  (add a directory to this arg to override the config)')
    parser.add_argument('-wt', '--writetxt', type=str, nargs='?', default=argparse.SUPPRESS, help='Write data to .txt files   (add a directory to this arg to override the config)')
    parser.add_argument('-ws', '--writesm',  type=str, nargs='?', default=argparse.SUPPRESS, help='Write data to .sm files    (add a directory to this arg to override the config)')
    parser.add_argument('-c', '--copyaudio', type=str, nargs='?', default=argparse.SUPPRESS, help='Copy audio files           (add a directory to this arg to override the config)')
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

    dir_output_audio = config.get('dir', 'copyaudio')
    if(hasattr(args, 'copyaudio')):
        if args.copyaudio:
            dir_output_audio = args.copyaudio

    if not isdir(dir_txt_input) or not isdir(dir_sm_input):
        print('Input .txt or .sm directory not found. Check user entry or configuration, and that the directories exist.')
        sys.exit()
    if not isdir(dir_txt_output) or not isdir(dir_sm_output):
        print('Output .txt or .sm directory not found. Check user entry or configuration, and that the directories exist.')
        sys.exit()
    if not isdir(dir_output_audio):
        print('Output directory for audio files not found. Check user entry or configuration, and that the directory exist.')
        sys.exit()

    start_time = time.time()

    dataList = [] # to contain a list of DataHandler object classes
    
    if hasattr(args, 'parsetxt'):
        print("Parsing .txt files from %s" % dir_txt_input)
        txt_filepaths = getFilePaths(dir_txt_input, {'.txt'})
        for file in txt_filepaths:
            print("  - Parsing %s" % file)
            dataList.append(Options.read_TXTtoData(file))

    if hasattr(args, 'parsesm'):
        print("Parsing .sm files from %s" % dir_sm_input)
        sm_filepaths = getFilePaths(dir_sm_input, {'.sm'})
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
    print("Elapsed data processing time was %g seconds" % (end_time - start_time))

    if hasattr(args, 'copyaudio'):
        print("Copying audio files (if it exists) related to parsed data")

        extensions = {'.ogg', '.mp3', '.wav'}
        audio_filepaths = []
        audio_filepaths.extend(getFilePaths(dir_sm_input, extensions))
        audio_filepaths.extend(getFilePaths(dir_txt_input, extensions))

        # create a dictionary pairing the formatted audio filename with their original path
        audio_name_paths = dict(zip([strip_filename(audio) for audio in audio_filepaths], range(len(audio_filepaths))))

        # copy audio file if it matches any parsed data
        for data in dataList:
            if data.filename in audio_name_paths.keys():

                in_audio_path = audio_filepaths[audio_name_paths[data.filename]]
                out_audio_path = join(dir_output_audio, data.filename + splitext(in_audio_path)[1]).replace("\\","/")

                if isfile(in_audio_path) and not isfile(out_audio_path):
                    print('  - Copying audio from %s to %s' % (in_audio_path, out_audio_path))
                    copyfile(in_audio_path, out_audio_path)
