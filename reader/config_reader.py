import json

from reader.file_reader import FileReader

class ConfigReader(FileReader):
    def read(path):
        with open(path) as config_file:
            return json.load(config_file)
