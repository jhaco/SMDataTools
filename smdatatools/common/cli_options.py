from smdatatools.common.file_utils import read_file, write_file, strip_filename, collect_filenames
from smdatatools.data_processing.data_handler import DataHandler
from smdatatools.data_processing.input_processor import InputProcessor
from smdatatools.data_processing.output_processor import OutputProcessor

class Options:

    def __init__(self):
        self.data = [] # to contain a list of DataHandler object classes

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
        ostr = OutputProcessor.pregenerate_txt_output(data.note_data)
        write_file(ostr, filepath)