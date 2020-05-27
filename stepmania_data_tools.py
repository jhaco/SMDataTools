import argparse
import configparser
import logging
import logging.config
import time
from os import makedirs
from os.path import join, isdir, dirname, realpath

from smdatatools.data_processing.collect import main_collect
from smdatatools.data_processing.write import main_write

if __name__ == '__main__':
    # logger setup
    if not isdir('logs'):
        makedirs('logs')
    logging.config.fileConfig('logging.ini')

    # argument parser setup
    SCRIPT_MAP = {'collect' : main_collect,
                  'write'   : main_write}

    data_tool = argparse.ArgumentParser(description='Stepmania Data Tools')
    data_tool.add_argument('script', choices=SCRIPT_MAP.keys(), help='Set script.')
    args = data_tool.parse_args()
    running_script = SCRIPT_MAP[args.script]

    # configuration setup
    config = configparser.ConfigParser()
    config.read('config.ini')
    input_dir = config.get(args.script, 'input')
    output_dir = config.get(args.script, 'output')

    start_time = time.time()

    if not isdir(input_dir):
        print('Invalid input directory argument. Check the configuration file.')
    else:
        if not isdir(output_dir):
            makedirs(output_dir)
            logging.warning('Output directory missing: ' + output_dir)
            logging.info('Generated specified output folder.')
        successful_files = running_script(input_dir, output_dir)
        end_time = time.time()
        print('Successfully processed %s files in %g seconds' % (successful_files, end_time - start_time))
