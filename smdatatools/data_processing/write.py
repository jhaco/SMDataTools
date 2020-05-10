from collections import defaultdict
from functools import reduce
from math import ceil, gcd
from os import makedirs, walk
from os.path import join, isdir
from re import sub, split
from shutil import copyfile

from smdatatools.common.file_utils import read_file, write_file, format_file_name

def pregenerate_sm(file_name, step_dict):
    # pre-generate output data
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

#===================================================================================================

def find_gcd(note_positions):
    x = reduce(gcd, note_positions + [256])
    return x

def generate_measure(notes, note_positions):
    # tries to fit 256, 128, 64, 32, 16, 8 or 4 note measures
    note_gcd = find_gcd(note_positions)

    if note_gcd == 128: # if fitting returns a 2 note measure, adjust to 4 note
        note_gcd = 64

    # place notes in generated measure
    generated_measure = ['0000']*int(256/note_gcd)
    for note, p in enumerate(note_positions):
        new_p = int(p/note_gcd)-1
        generated_measure[new_p] = notes[note]

    return generated_measure

def notes_to_measure(notes, timings, note_256):
    if not notes or not timings: # no notes in current measure
        return ['0000','0000','0000','0000',',']
    
    note_positions = []
    for time in timings:
        note_position = 0
        min_error = 5.0 # edge case: might need to adjust for really slow songs
        for i in range(256):
            error = abs(time - i*note_256)
            if error <= min_error: # narrows down note position based on timing difference
                note_position = i
                min_error = error
            else:
                break # stops finding note position once found
        note_positions.append(note_position+1) #pre-adjusts positions to be mathematically correct
    measure = generate_measure(notes, note_positions)
    measure.append(',')

    return measure

def place_notes(notes_and_timings, bpm):
    placed_notes = []
    if not notes_and_timings:
        return placed_notes

    seconds  = round(4 * 60/bpm, 10) # length of measure in seconds
    total_time = float(notes_and_timings[-1].split()[1])
    total_measures = ceil(total_time/seconds)
    note_256 = round(seconds/256, 5)
    index = 0
    
    for measure in range(total_measures):
        notes = []   # contains notes that fit current measure
        timings = [] # contains timings that fit current measure
        while index < len(notes_and_timings):
            note_timing = notes_and_timings[index].split()
            note = note_timing[0]
            timing = float(note_timing[1])
            if((measure * seconds) <= timing < ((measure+1) * seconds)):
                notes.append(note)
                timings.append(round(timing - (measure * seconds), 5))
                index += 1
            else:
                break
        placed_notes.extend(notes_to_measure(notes, timings, note_256))

    placed_notes[-1] = ';'
    return placed_notes

def parse_txt(txt_file):
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
                    notes = place_notes(notes_and_timings, step_dict['bpm'])
                    step_dict['notes'][current_difficulty].extend(notes)
                    notes_and_timings.clear()
                current_difficulty = line.split()[1]
            else:
                notes_and_timings.append(line)
    notes = place_notes(notes_and_timings, step_dict['bpm'])
    step_dict['notes'][current_difficulty].extend(notes)
    
    return step_dict

#===================================================================================================

def main_write(input_dir, output_dir):
    for root, dirs, files in walk(input_dir):
        txt_files = [file for file in files if file.endswith('.txt')]
        ogg_files = [file for file in files if file.endswith('.ogg')]

        format_ogg_dict = dict(zip([format_file_name(ogg) for ogg in ogg_files], range(len(ogg_files))))

        for txt_file in txt_files:
            new_file = format_file_name(txt_file)
            try:
                txt_data = parse_txt(read_file(join(root, txt_file)))
                # creates new folder for successfully parsed data
                output_folder = output_dir + '/' + new_file
                if not isdir(output_folder):
                    makedirs(output_folder)
                # write text sm data to output dir
                write_file(pregenerate_sm(new_file, txt_data), join(output_folder, new_file + '.sm'))
            except Exception as ex:
                print('Write failed for %s: %r' % (txt_file, ex))
            try:
                # move and rename .ogg file to output dir
                copyfile(join(root, ogg_files[format_ogg_dict[new_file]]), join(output_folder, new_file + '.ogg'))
            except Exception as ex:
                print('Sound file not found for %s' % (new_file))

