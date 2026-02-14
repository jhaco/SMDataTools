from smdatatools.common.file_utils import read_file, write_file, strip_filename
from smdatatools.data_processing.data_handler import DataHandler
from smdatatools.data_processing.input_processor import InputProcessor
from smdatatools.data_processing.output_processor import OutputProcessor

class Options:
    @staticmethod
    def read_SMtoData(filepath: str) -> DataHandler:
        data = DataHandler(filepath)
        istr = read_file(filepath)
        data.note_data, data.valid = InputProcessor.parse_sm_input(istr)
        return data

    @staticmethod
    def read_TXTtoData(filepath: str) -> DataHandler:
        data = DataHandler(filepath)
        istr = read_file(filepath)
        data.note_data = InputProcessor.parse_txt_input(istr)
        return data

    @staticmethod
    def write_DatatoSM(data: DataHandler, filepath: str) -> None:
        filename = strip_filename(filepath)
        ostr = OutputProcessor.pregenerate_sm_output(filename, data.processed_data)
        write_file(ostr, filepath)

    def write_DatatoTXT(data: DataHandler, filepath: str) -> None:
        ostr = OutputProcessor.pregenerate_txt_output(data.note_data)
        write_file(ostr, filepath)