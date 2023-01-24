import nltk
from RANKING import indicators

class Ranking:

    def __init__(self, request, index):
        self.request = request
        self.index = index

    def transform_request(self):
        '''
        tokenize and lowerize user request
        '''
        request = self.request.lower()
        tokens = nltk.word_tokenize(request)
        return tokens
        
    def filter(self):
        index = self.index
        tokens = self.transform_request()
        documents_id = []
        for token in tokens:
            if token in index.keys():
                documents_token = index[token].keys()
                for doc in documents_token:
                    documents_id.append(doc)
        return documents_id

    def bm25(self, id_doc, k = 1.2, b = 0.75):
        tokens = self.transform_request()
        bm25 = 0
        for token in tokens:
            ind = indicators.Indicators(self.index)
            bm25 += ind.bm25_token(token, id_doc, k=k, b=b)
        return bm25