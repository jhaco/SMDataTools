from smdatatools.common.file_utils import read_file, write_file, strip_filename, collect_filenames
from smdatatools.data_processing.data_handler import DataHandler
from smdatatools.data_processing.input_processor import InputProcessor
from smdatatools.data_processing.output_processor import OutputProcessor

class Options:

    def __init__(self):
        self.data = [] # to contain a list of DataHandler object classes

        self.sm_filepaths = []
        self.ogg_filepaths = []
        self.txt_filepaths = []

    def getFilePaths(self, input_dir, extension):
        filepaths = collect_filenames(input_dir, extension)

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

    def read_SMtoData(self, filepath: str) -> DataHandler:
        data = DataHandler(filepath)
        istr = read_file(filepath)
        data.note_data = InputProcessor.parse_sm_input(istr)
        return data

    def read_TXTtoData(self, filepath: str) -> DataHandler:
        data = DataHandler(filepath)
        istr = read_file(filepath)
        data.note_data = InputProcessor.parse_txt_input(istr)
        return data

    def write_DatatoSM(self, data: DataHandler, filepath: str):
        filename = strip_filename(filepath)
        ostr = OutputProcessor.pregenerate_sm_output(filename, data.processed_data)
        write_file(ostr, filepath)

    def write_DatatoTXT(self, data: DataHandler, filepath: str):
        filename = strip_filename(filepath)
        ostr = OutputProcessor.pregenerate_txt_output(data.note_data)
        write_file(ostr, filepath)