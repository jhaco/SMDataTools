from collections import defaultdict

class OutputProcessor:

    def pregenerate_sm_output(file_name: str, note_data: defaultdict(list)) -> str:
        # pre-generate .sm output data
        title  = '#TITLE:%s;\n' % note_data['title']
        artist = '#ARTIST:jhaco vs cpuguy96;\n'
        music  = '#MUSIC:%s.ogg;\n' % file_name
        select = '#SELECTABLE:YES;\n'
        bpm    = '#BPMS:0.000=%s;\n\n' % str(note_data['bpm'])
        notes = ''

        for difficulty in note_data['notes'].keys():

            notes += '//---------------dance-single - ----------------\n'
            notes += '#NOTES:\n'
            notes += '     dance-single:\n'
            notes += '     :\n'
            notes += '     %s:\n' % difficulty
            notes += '     8:\n'
            notes += '     1.000,1.000,1.000,1.000,1.000:\n'
        
            for note in note_data['notes'][difficulty]:
                    notes += note + '\n'

        return ''.join((title, artist, music, select, bpm, notes))

    def pregenerate_txt_output(note_data: defaultdict(list)) -> str:
        # pre-generate output data
        title = 'TITLE %s\n' % note_data['title']
        bpm   = 'BPM   %s\n' % str(note_data['bpm'])
        notes = 'NOTES\n'
        for difficulty in note_data['notes'].keys():
            notes += 'DIFFICULTY %s\n' % difficulty
            for note in note_data['notes'][difficulty]:
                notes += note + '\n'

        return ''.join((title, bpm, notes))
