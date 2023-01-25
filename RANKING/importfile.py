import json

class ImportFile:

    def __init__(self, file):
        self.file = file

    def import_json(self, encoding='utf-8'):
        '''
        import json file
        '''
        file = open(self.file, encoding=encoding)
        data = json.load(file)
        return data