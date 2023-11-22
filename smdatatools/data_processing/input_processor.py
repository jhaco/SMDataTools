from collections import defaultdict
from re import sub, split

from smdatatools.components.measure import Measure

class InputProcessor:

    def convert_note(line):                                                      
        return sub('4', '1', sub('[MKLF]', '0', line))    #replaces extra notes: M, K, L, F; replaces 4 note

    def parse_sm_input(sm_file):
        note_data = defaultdict(list)
        note_data['notes'] = defaultdict(list) # notes are paired with each difficulty
        current_difficulty = ''
        measure         = []
        measure_index   = 0

        valid = True

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
                            note_data['title']  = data_value
                        elif data_name == 'BPMS':
                            if ',' in data_value:  # skips if multiple BPMS detected
                                # instead of raising an error, print a warning with the song name and skip
                                print('Multiple BPMs detected. Skipping...')
                                valid = False
                                break
                            note_data['bpm']    = float(split('=', data_value)[-1]) # removes time to get bpm
                        elif data_name == 'STOPS' and data_value: # skips if STOPS are detected
                            # instead of raising an error, print a warning with the song name and skip
                            print('Stop detected. Skipping...')
                            valid = False
                            break
                        elif data_name == 'OFFSET':
                            note_data['offset'] = float(data_value)
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
                    notes_and_timings = Measure.calculate_timing(measure, measure_index, note_data['bpm'], note_data['offset'])
                    note_data['notes'][current_difficulty].extend(notes_and_timings)
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
                
        return note_data, valid

    def parse_txt_input(txt_file):
        note_data = defaultdict(list)
        note_data['notes'] = defaultdict(list)
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
                        note_data['title'] = data_value
                    elif data_name == 'BPM':
                        note_data['bpm'] = float(data_value)
            else:
                if line.startswith('DIFFICULTY'):
                    if notes_and_timings:
                        note_data['notes'][current_difficulty].extend(notes_and_timings)
                        notes_and_timings.clear()
                    current_difficulty = line.split()[1]
                else:
                    notes_and_timings.append(line)
        note_data['notes'][current_difficulty].extend(notes_and_timings)
    
        return note_data
