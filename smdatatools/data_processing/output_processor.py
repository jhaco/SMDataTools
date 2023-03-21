import logging

from collections import defaultdict
from math import ceil
from os import makedirs, walk
from os.path import join, isdir
from shutil import copyfile

from smdatatools.common.file_utils import read_file, write_file, strip_filename
from smdatatools.components.measure import Measure

class OutputProcessor:

    def pregenerate_sm_output(file_name: str, step_dict: defaultdict(list)) -> str:
        # pre-generate .sm output data
        title  = '#TITLE:%s;\n' % step_dict['title']
        artist = '#ARTIST:jhaco vs cpuguy96;\n'
        music  = '#MUSIC:%s.ogg;\n' % file_name
        select = 'SELECTABLE:YES;\n'
        bpm    = 'BPMS:0.000=%s;\n\n' % str(step_dict['bpm'])
        note_data = ''

        for difficulty in step_dict['notes'].keys():

            note_data += '//---------------dance-single - ----------------\n'
            note_data += '#NOTES:\n'
            note_data += '     dance-single:\n'
            note_data += '     :\n'
            note_data += '     %s:\n' % difficulty
            note_data += '     8:\n'
            note_data += '     1.000,1.000,1.000,1.000,1.000:\n'
        
            for note in step_dict['notes'][difficulty]:
                    note_data += note + '\n'

        return ''.join((title, artist, music, select, bpm, note_data))

    def pregenerate_txt_output(step_dict) -> str:
        # pre-generate output data
        title = 'TITLE %s\n' % step_dict['title']
        bpm   = 'BPM   %s\n' % str(step_dict['bpm'])
        note_data = 'NOTES\n'
        for difficulty in step_dict['notes'].keys():
            note_data += 'DIFFICULTY %s\n' % difficulty
            for note in step_dict['notes'][difficulty]:
                note_data += note + '\n'

        return ''.join((title, bpm, note_data))

#def main_write(input_dir, output_dir):
#    successful_files = 0
#    for root, dirs, files in walk(input_dir):
#        txt_files = [file for file in files if file.endswith('.txt')]
#        ogg_files = [file for file in files if file.endswith('.ogg')]

#        format_ogg_dict = dict(zip([strip_filename(ogg) for ogg in ogg_files], range(len(ogg_files))))

#        for txt_file in txt_files:
#            new_file = strip_filename(txt_file)
#            try:
#                txt_data = parse_txt_input(read_file(join(root, txt_file)))
#                # creates new folder for successfully parsed data
#                output_folder = output_dir + '/' + new_file
#                if not isdir(output_folder):
#                    makedirs(output_folder)
#                # write text sm data to output dir
#                #write_file(pregenerate_output(new_file, txt_data), join(output_folder, new_file + '.sm'))
#                successful_files+=1
#            except Exception as ex:
#                logging.warning('Write failed for %s: %r' % (txt_file, ex))
#            try:
#                # move and rename .ogg file to output dir
#                copyfile(join(root, ogg_files[format_ogg_dict[new_file]]), join(output_folder, new_file + '.ogg'))
#            except Exception as ex:
#                logging.warning('Sound file not found for %s' % (new_file))
#    return successful_files
