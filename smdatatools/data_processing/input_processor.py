import logging

from collections import defaultdict
from os import walk
from os.path import join
from re import sub, split
from shutil import copyfile

from smdatatools.common.file_utils import read_file, write_file, format_file_name
from smdatatools.components.measure import Measure

class InputProcessor:

    def convert_note(line):                                                      
        return sub('4', '1', sub('[MKLF]', '0', line))    #replaces extra notes: M, K, L, F; replaces 4 note

    def parse_sm_input(sm_file):
        step_dict = defaultdict(list)
        step_dict['notes'] = defaultdict(list) # notes are paired with each difficulty
        current_difficulty = ''
        measure         = []
        measure_index   = 0

        read_notes          = False
        not_dance_single    = False # ensures data matches the 4-note dance-singles mode, not the 8-note dance-double

        read_values = '' # contains combined data while not reading notes; structured '#type:data;'
        for i, line in enumerate(sm_file):
            line = line.rstrip() # removes trailing newline '\n' and possible trailing whitespace
            if not read_notes:
                if line.startswith('#NOTES:'):
                    read_notes = True
                else:
                    read_values += line
                    if read_values.endswith(';'): # begin processing read_values for data
                        metadata = read_values.lstrip('#').rstrip(';').split(':') # removes extra characters; splits name from values
                        data_name = metadata[0]
                        data_value = ':'.join(metadata[1:])
                        if data_name == 'TITLE':
                            step_dict['title']  = data_value
                        elif data_name == 'BPMS':
                            if ',' in data_value:  # raises Exception if multiple BPMS detected
                                raise ValueError('Multiple BPMs detected')
                            step_dict['bpm']    = float(split('=', data_value)[-1]) # removes time to get bpm
                        elif data_name == 'STOPS' and data_value:
                            raise ValueError('Stop detected')
                        elif data_name == 'OFFSET':
                            step_dict['offset'] = float(data_value)
                        read_values = ''

            if read_notes:   #start of note processing
                if line.startswith('#NOTES:'): # marks the beginning of each difficulty and its notes
                    not_dance_single = False
                    measure_index = 0
                    if sm_file[i+1].lstrip(' ').rstrip(':\n') != 'dance-single':
                        not_dance_single = True
                    current_difficulty = sm_file[i+3].lstrip(' ').rstrip(':\n') # difficulty always found 3 lines down
                elif not_dance_single:
                    continue
                elif line.startswith((',', ';')): # marks the end of each measure
                    notes_and_timings = Measure.calculate_timing(measure, measure_index, step_dict['bpm'], step_dict['offset'])
                    step_dict['notes'][current_difficulty].extend(notes_and_timings)
                    measure.clear()
                    measure_index += 1
                elif line and not line.startswith(' '): # individual notes
                    note = InputProcessor.convert_note(line)
                    if note[0].isdigit():
                        note_placed = True if any((c in set('123456789')) for c in note) else False
                        if note_placed:
                            measure.append(note) # adds note if found
                        else:
                            measure.append(None)
                
        return step_dict

    def parse_txt_input(txt_file):
        step_dict = defaultdict(list)
        step_dict['notes'] = defaultdict(list)
        current_difficulty = ''
        notes_and_timings = []

        read_notes = False

        for line in txt_file:
            line = line.rstrip()
            if not read_notes:
                if line.startswith('NOTES'):
                    read_notes = True
                else:
                    metadata = line.split() # splits name from values by whitespace
                    data_name = metadata[0]
                    data_value = ' '.join(metadata[1:])
                    if data_name == 'TITLE':
                        step_dict['title'] = data_value
                    elif data_name == 'BPM':
                        step_dict['bpm'] = float(data_value)
            else:
                if line.startswith('DIFFICULTY'):
                    if notes_and_timings:
                        notes = Measure.place_notes(notes_and_timings, step_dict['bpm'])
                        step_dict['notes'][current_difficulty].extend(notes)
                        notes_and_timings.clear()
                    current_difficulty = line.split()[1]
                else:
                    notes_and_timings.append(line)
        notes = Measure.place_notes(notes_and_timings, step_dict['bpm'])
        step_dict['notes'][current_difficulty].extend(notes)
    
        return step_dict





#def main_collect(input_dir, output_dir):
#    successful_files = 0
#    for root, dirs, files in walk(input_dir):
#        sm_files = [file for file in files if file.endswith('.sm')]
#        ogg_files = [file for file in files if file.endswith('.ogg')]

#        format_ogg_dict = dict(zip([format_file_name(ogg) for ogg in ogg_files], range(len(ogg_files))))

#        for sm_file in sm_files:
#            new_file = format_file_name(sm_file)
#            if new_file in format_ogg_dict:
#                try:
#                    #sm_data = parse_sm(read_file(join(root, sm_file)))
#                    # write sm text data to output dir
#                    #write_file(pregenerate_txt(sm_data), join(output_dir, new_file + '.txt'))
#                    # move and rename .ogg file to output dir
#                    copyfile(join(root, ogg_files[format_ogg_dict[new_file]]), join(output_dir, new_file + '.ogg'))
#                    successful_files+=1
#                except Exception as ex:
#                    logging.warning('Write failed for %s: %r' % (sm_file, ex))
#            else:
#                logging.warning('Skipped parsing for %s. Sound file not found' % (new_file))
#    return successful_files