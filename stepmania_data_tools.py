import argparse
import configparser
import time
from os import makedirs
from os.path import join, isdir, dirname, realpath

from smdatatools.data_processing.collect import main_collect
from smdatatools.data_processing.write import main_write

if __name__ == '__main__':
    start_time = time.time()

    dir = dirname(realpath(__file__))
    SCRIPT_MAP = {'collect' : main_collect,
                  'write'   : main_write}

    data_tool = argparse.ArgumentParser(description='Stepmania Data Tools')
    data_tool.add_argument('script', choices=SCRIPT_MAP.keys(), help='Set script.')
    args = data_tool.parse_args()
    running_script = SCRIPT_MAP[args.script]
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    input_dir = config.get(args.script, 'input')
    output_dir = config.get(args.script, 'output')

    if not isdir(input_dir):
        print("Invalid input directory argument.")
    else:
        if not isdir(output_dir):
            makedirs(output_dir)
            print("Output directory missing: %s\nGenerated specified output folder." % args.output)
        running_script(input_dir, output_dir)

    end_time = time.time()
    print("Elapsed time was %g seconds" % (end_time - start_time))

        