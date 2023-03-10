import nltk
nltk.download('punkt')
from RANKING.indicators import Indicators
import time
import json

class Ranking:
    """
    This class contains all the functions allowing to compute
    a ranking of relevant documents for a given request
    """

    def __init__(self, request, index, documents):
        self.request = request
        self.index = index
        self.documents = documents
        self.rank = None

    def transform_request(self):
        '''
        tokenize and put in lower case request given by one user
        '''
        request = self.request.lower()
        tokens = nltk.word_tokenize(request)
        return tokens
        
    def filter(self, intersect = True):
        '''
        filter documents containing tokens of one request
        if intersect = True, return documents which contain all tokens
        else, return documents containing at least one token
        '''
        documents_ids = set(Indicators(self.index).doc_ids())
        index = self.index
        tokens = self.transform_request()
        first = True

        for token in tokens:
            documents_ids_token = set()
            # check that token is present in index
            if token in index.keys():
                # documents_ids_token: list of documents containing a given token
                for doc in index[token].keys():
                    if doc not in documents_ids_token:
                        documents_ids_token.add(doc)
                
            # if intersect = True, compute intersection for each token
            if intersect:
                documents_ids = documents_ids & documents_ids_token
            
            # else compute union
            else:
                if first:
                    # initialize documents_ids with all documents containing the first token
                    documents_ids = documents_ids_token
                    first = False
                else:
                    documents_ids = documents_ids.union(documents_ids_token)
        return list(documents_ids)

    def bm25(self, id_doc, k = 1.2, b = 0.75):
        '''
        compute bm25 score between a request and a document
        '''
        tokens = self.transform_request()
        bm25 = 0
        # compute the sum of bm25 of each token to get the final bm25 of the request
        for token in tokens:
            ind = Indicators(self.index)
            bm25 += ind.bm25_token(token, id_doc, k=k, b=b)
        return bm25

    def ranking(self, intersect = True):
        '''
        - rank documents by using bm25 score
        - give additional information
        '''
        start = time.time()
        # filter documents
        filter = self.filter(intersect = intersect)
        
        # add bm25 score for each document in filter
        bm25 = {}
        for id_doc in filter:
            bm25[id_doc] = self.bm25(id_doc)
        
        # sort by bm25 score to get the ranking
        rank_docs = sorted(bm25.items(), key=lambda kv: kv[1], reverse=True)
        list_rank_docs = list(dict(rank_docs).keys())

        # extract info about document with documents file
        res_request = {}
        res_request['results'] = {}
        id = 0
        for id_doc in list_rank_docs:
            for elem in self.documents:
                if int(id_doc) == elem['id']:
                    res_request['results'][id] = {}
                    res_request['results'][id]['title'] = elem['title']
                    res_request['results'][id]['url'] = elem['url']
                    id += 1
                    
        # add additionnal information
        res_request['infos'] = {}
        res_request['infos']['number of documents in index'] = len(Indicators(self.index).doc_ids())
        res_request['infos']['number of survivor documents after filtering'] = len(filter)
        end = time.time()
        res_request['infos']['execution time'] = str(round(end - start, 3)) + ' seconds'
        
        # save the result in rank argument
        self.rank = res_request

        # write the result in a json file
        res_json = json.dumps(res_request, indent = 4, ensure_ascii=False)
        with open("results.json", "w") as outfile:
            outfile.write(res_json)

    def __str__(self) -> str:
        '''
        print the results of the ranking in a human-friendly way
        '''
        return json.dumps(self.rank, indent = 4, ensure_ascii=False)

