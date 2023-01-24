import json

class ImportFile:

    def __init__(self, file):
        self.file = file

    def import_json(self):
        '''
        import json file
        '''
        file = open(self.file)
        data = json.load(file)
        return data