from collections import defaultdict

from smdatatools.common.file_utils import strip_filename
from smdatatools.components.measure import Measure

class DataHandler:
    # each Data Handler will represent the data of one .sm/.txt file

    def __init__(self, filepath):
        self.sm_path = filepath
        self.filename = strip_filename(filepath)

        self.note_data = defaultdict(list)
        self.processed_data = defaultdict(list)
        self.valid = True

    def process_data_to_sm_format(self):

        self.processed_data['title'] = self.note_data['title']
        self.processed_data['bpm'] = float(self.note_data['bpm'])
        self.processed_data['notes'] = defaultdict(list)

        for difficulty in self.note_data['notes'].keys():
            notes = Measure.place_notes(self.note_data['notes'][difficulty], self.processed_data['bpm'])
            self.processed_data['notes'][difficulty].extend(notes)