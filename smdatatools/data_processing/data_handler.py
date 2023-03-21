
from collections import defaultdict

from smdatatools.common.file_utils import read_file, write_file, strip_filename, collect_filenames
from smdatatools.data_processing.input_processor import InputProcessor
from smdatatools.data_processing.output_processor import OutputProcessor

class DataHandler:

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.sm_filepaths = []
        self.ogg_filepaths = []
        self.txt_filepaths = []

        self.raw_data = defaultdict(list)
        self.processed_data = defaultdict(list)

    def getFilePaths(self, extension):
        filepaths = collect_filenames(self.input_dir, extension)

        if(extension == '.sm'):
            self.sm_filepaths = filepaths
            self.checkFilePaths()
        elif(extension == '.ogg'):
            self.ogg_filepaths = filepaths
        elif(extension == '.txt'):
            self.txt_filepaths = filepaths

    def checkFilePaths(self):
        # checks for static bpm in the .sm file
        # and removes filepath from list if not
        for sm_file in self.sm_filepaths:
            with open(sm_file, encoding='ascii', errors='ignore') as f:
                for line in sm_file:
                    if line.startswith('#BPMS:'):
                        if ',' in line: # indicates multiple BPMs (non-static)
                            self.sm_filepaths.remove(sm_file)
                        break

    def readSMtoRaw(self, filepath: str):
        self.raw_data.clear()
        istr = read_file(filepath)
        self.raw_data = InputProcessor.parse_sm_input(istr)

    def readTXTtoRaw(self, filepath:str):
        self.raw_data.clear()
        istr = read_file(filepath)
        self.raw_data = InputProcessor.parse_txt_input(istr)

    def writeDatatoSM(self, filepath: str, erase_data = True):
        filename = strip_filename(filepath)
        ostr = OutputProcessor.pregenerate_sm_output(filename, self.processed_data)
        write_file(ostr, filepath)
        
        if(erase_data):
            self.processed_data.clear()

    def writeRawtoTXT(self, filepath: str, erase_data = True):
        filename = strip_filename(filepath)
        ostr = OutputProcessor.pregenerate_txt_output(filename, self.raw_data)
        write_file(ostr, filepath)
        
        if(erase_data):
            self.raw_data.clear()

