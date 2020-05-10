from collections import defaultdict
from os import walk
from os.path import join
from re import sub, split
from shutil import copyfile

from smdatatools.common.file_utils import read_file, write_file, format_file_name

def convert_note(line):                                                      
    return sub('4', '1', sub('[MKLF]', '0', line))    #replaces extra notes: M, K, L, F; replaces 4 note

def pregenerate_txt(step_dict):
    # pre-generate output data
    title = 'TITLE %s\n' % step_dict['title']
    bpm   = 'BPM   %s\n' % str(step_dict['bpm'])
    note_data = 'NOTES\n'
    for difficulty in step_dict['notes'].keys():
        note_data += 'DIFFICULTY %s\n' % difficulty
        for note in step_dict['notes'][difficulty]:
            note_data += note + '\n'

    return ''.join((title, bpm, note_data))

#===================================================================================================

# BPM       = beats/minute -> BPS = beats/second = BPM/60
# measure   = 4 beats = 4 * 1/4th notes     = 1 note
# 1/256    -> 256 * 1/256th notes           = 1 measure

def calculate_timing(measure, measure_index, bpm, offset):  #calculate time in seconds for each line
    measure_seconds = 4 * 60/bpm    #length of measure in seconds
    note_256        = measure_seconds/256   #length of each 1/256th note in the measure in seconds
    measure_timing  = measure_seconds * measure_index   #accumulated time from previous measures
    fraction_256    = 256/len(measure)  #number of 1/256th notes per beat: 1/2nd = 128, 1/4th = 64, etc
    # combines note and its timing, if the note exists
    note_and_timings = [measure[i] + ' ' + str(i * note_256 * fraction_256 + measure_timing - offset) for i, is_set in enumerate(measure) if is_set != None]
    
    return note_and_timings

def parse_sm(sm_file):
    step_dict = defaultdict(list)
    step_dict['notes'] = defaultdict(list) # notes are paired with each difficulty
    current_difficulty = ''
    measure         = []
    measure_index   = 0

    read_notes      = False

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
                measure_index = 0
                current_difficulty = sm_file[i+3].lstrip(' ').rstrip(':\n') # difficulty always found 3 lines down
            elif line.startswith((',', ';')): # marks the end of each measure
                notes_and_timings = calculate_timing(measure, measure_index, step_dict['bpm'], step_dict['offset'])
                step_dict['notes'][current_difficulty].extend(notes_and_timings)
                measure.clear()
                measure_index += 1
            elif line and not line.startswith(' '): # individual notes
                note = convert_note(line)
                if note[0].isdigit():
                    note_placed = True if any((c in set('123456789')) for c in note) else False
                    if note_placed:
                        measure.append(note) # adds note if found
                    else:
                        measure.append(None)
                
    return step_dict

#===================================================================================================

def main_collect(input_dir, output_dir):
    for root, dirs, files in walk(input_dir):
        sm_files = [file for file in files if file.endswith('.sm')]
        ogg_files = [file for file in files if file.endswith('.ogg')]

        format_ogg_dict = dict(zip([format_file_name(ogg) for ogg in ogg_files], range(len(ogg_files))))

        for sm_file in sm_files:
            new_file = format_file_name(sm_file)
            if new_file in format_ogg_dict:
                try:
                    sm_data = parse_sm(read_file(join(root, sm_file)))
                    # write sm text data to output dir
                    write_file(pregenerate_txt(sm_data), join(output_dir, new_file + '.txt'))
                    # move and rename .ogg file to output dir
                    copyfile(join(root, ogg_files[format_ogg_dict[new_file]]), join(output_dir, new_file + '.ogg'))
                except Exception as ex:
                    print('Write failed for %s: %r' % (sm_file, ex))