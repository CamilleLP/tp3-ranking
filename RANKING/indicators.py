import math

class Indicators:

    def __init__(self, index):
        self.index = index
    
    def count_token_doc(self, token, doc_index):
        '''
        count the number of times where one token appear in one document
        '''
        count = 0
        if token in list(self.index.keys()):
            index = str(doc_index)
            if index in list(self.index[token].keys()):
                count = self.index[token][index]['count']
        return count

    def len_doc(self, doc_index):
        '''
        return length of a document (number of tokens)
        '''
        len_doc = 0
        index = str(doc_index)
        for token in list(self.index.keys()):
            if index in list(self.index[token].keys()):
                len_doc += self.index[token][index]['count']
        return len_doc

    def doc_ids(self):
        '''
        return list of all documents
        '''
        doc_ids = []
        for token in list(self.index.keys()):
            for id in list(self.index[token].keys()):
                if id not in doc_ids:
                    doc_ids.append(id)
        return doc_ids

    def avg_len(self):
        '''
        return the average number of tokens per document
        '''
        avg_len = 0
        doc_ids = self.doc_ids()
        nb_docs = len(doc_ids)
        len_docs = 0
        for doc in doc_ids:
            len_docs += self.len_doc(doc)
        if nb_docs:
            avg_len = round(len_docs / nb_docs, 3)
        return avg_len

    def nb_docs_with_token(self, token):
        '''
        count the number of documents containing one token
        '''
        count = 0
        if token in list(self.index.keys()):
            count = len(list(self.index[token].keys()))
        return count

    def idf(self, token):
        '''
        compute idf (inverse document frequency)
        '''
        N = len(self.doc_ids())
        n = self.nb_docs_with_token(token)
        # classic formula: math.log(N / n)
        # use of modified formula to avoid division by 0
        idf = (N - n + 0.5) / (n + 0.5) + 1
        return idf

    def bm25_token(self, token, id_doc, k = 1.2, b = 0.75):
        '''
        compute bm25 for one token
        '''
        f = self.count_token_doc(token, id_doc)
        len_doc = self.len_doc(id_doc)
        avg_len = self.avg_len()
        bm25_token = self.idf(token) * ((f * (k + 1) / (f + k * (1 - b + (b * (len_doc / avg_len))))))
        return round(bm25_token,3)
