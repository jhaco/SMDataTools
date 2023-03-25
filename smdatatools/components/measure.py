from functools import reduce
from math import gcd, ceil

class Measure:

    def calculate_timing(measure, measure_index, bpm, offset):
        # calculate time in seconds for each line in the measure:
        #   BPM       = beats/minute -> BPS = beats/second = BPM/60
        #   measure   = 4 beats = 4 * 1/4th notes     = 1 note
        #   1/256    -> 256 * 1/256th notes           = 1 measure
        measure_seconds = 4 * 60/bpm                        # length of measure in seconds
        note_256        = measure_seconds/256               # length of each 1/256th note in the measure in seconds
        measure_timing  = measure_seconds * measure_index   # cumulative time summed from previous measures
        fraction_256    = 256/len(measure)                  # number of 1/256th notes per beat: 1/2nd = 128, 1/4th = 64, etc
        
        # returns the note/timing pair, if the note exists
        return [measure[i] + ' ' + str(i * note_256 * fraction_256 + measure_timing - offset) for i, is_set in enumerate(measure) if is_set != None]

    def find_gcd(note_positions) -> int:
        # attempts to fit the note positions into either a 
        # 256, 128, 64, 32, 16, 8 or 4 note measure based on spacing 
        # found by getting the greatest common denominator
        # of all gaps between each note position
        gcd_gap = reduce(gcd, note_positions + [256])

        # if the gap returns a 256/128 = 2 note measure, 
        # we'll need to adjust the gap for a 256/64 = 4 note measure
        if gcd_gap == 128: 
            gcd_gap = 64
    
        return int(gcd_gap)

    def generate_measure(notes, note_positions) -> list[str]:
    
        # we'll want to trim as much output as possible
        # by reducing the measure size
        measure_gcd = Measure.find_gcd(note_positions)
    
        # place notes in the generated measure
        # by calculating the adjusted note position
        # relative to the old note position
        generated_measure = ['0000'] * int(256/measure_gcd)
        for note, p_old in enumerate(note_positions):
            p_adj = int(p_old / measure_gcd)-1
            generated_measure[p_adj] = notes[note]

        return generated_measure

    def fit_notes_to_measure(notes, timings, seconds_1_256) -> list[str]:
        # if no data is passed, generate current measure
        # as "empty" with the smallest size
        if not notes or not timings:
            return ['0000','0000','0000','0000',',']
    
        # fit notes into any of the 256 possible slots on 
        # the measure from timings and note order based on
        # the length of a 1/256 note in seconds
        note_positions = []
        i = 0

        for time in timings:
            note_pos = 0
            min_error = 5.0 # TODO: retroactively adjust this for slower songs
        
            # narrow down the note position based on timing
            for i in range(256): 
                error = abs(time - i * seconds_1_256) 
                if error <= min_error: 
                    note_pos = i
                    min_error = error
                else:
                    break
            note_positions.append(note_pos + 1) # increment by 1 to be mathematically correct

        # generate and reduce size of measure based on notes, if possible
        measure = Measure.generate_measure(notes, note_positions)
        measure.append(',')

        return measure

    def place_notes(notes_and_timings, bpm) -> list:
        placed_notes = []
        if not notes_and_timings:
            return placed_notes

        seconds  = round(4 * 60/bpm, 10) # length of each measure in seconds
        total_time = float(notes_and_timings[-1].split()[1])
        total_measures = ceil(total_time/seconds)
        seconds_1_256 = round(seconds/256, 5) # length of a 1/256 note in seconds
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
            placed_notes.extend(Measure.fit_notes_to_measure(notes, timings, seconds_1_256))

        placed_notes[-1] = ';'
        return placed_notes
