from unittest import TestCase
from RANKING.indicators import Indicators

class TestIndicators(TestCase):
    
    def test_count_token_doc(self):
        '''
        check that count_token_doc returns correct results:
        - if token is in one document, it must returns the exact count
        - if token is in index but not in document specified, it must return 0
        - same if token is not in index (token not present in any of the documents)
        - if doc_index not in index must return 0
        '''
        # GIVEN
        small_index = {"hello": {"0": {"positions": [0, 2], "count": 2}}, 
        "world": {"0": {"positions": [1], "count": 1}, 
        "1": {"positions": [1], "count": 1}}}

        token_in_doc0 = 'hello'
        token_in_doc1 = 'world'
        token_not_in_docs = 'bonjour'

        # WHEN
        indic = Indicators(small_index)
        count_token_not_in_docs = indic.count_token_doc(token = token_not_in_docs, doc_index=0)
        count_token_in_doc0 = indic.count_token_doc(token = token_in_doc0, doc_index=0)
        count_token_in_doc1 =  indic.count_token_doc(token = token_in_doc1, doc_index=1)
        count_token_not_in_doc0 =  indic.count_token_doc(token = token_in_doc0, doc_index=1)
        count_doc_not_in_index =  indic.count_token_doc(token = token_in_doc0, doc_index=10)
        
        # THEN
        self.assertEquals(count_doc_not_in_index, 0)
        self.assertEquals(count_token_not_in_docs, 0)
        self.assertEquals(count_token_in_doc0, 2)
        self.assertEquals(count_token_in_doc1, 1)
        self.assertEquals(count_token_not_in_doc0, 0)

    def test_len_doc(self):
        '''
        check that len_doc returns correct number of tokens for a document
        if index of document not in index, it must return 0
        '''
        # GIVEN
        small_index = {"hello": {"0": {"positions": [0, 2], "count": 2}}, 
        "world": {"0": {"positions": [1], "count": 1}, 
        "1": {"positions": [1], "count": 1}}}

        # WHEN
        indic = Indicators(small_index)
        doc0_in_index = indic.len_doc(0)
        doc1_in_index = indic.len_doc(1)
        doc10_not_in_index = indic.len_doc(10)
        
        # THEN
        self.assertEquals(doc0_in_index, 3)
        self.assertEquals(doc1_in_index, 1)
        self.assertEquals(doc10_not_in_index, 0)

    def test_doc_ids(self):
        '''
        check that len_doc returns correct number of tokens for a document
        if index of document not in index, it must return 0
        '''
        # GIVEN
        small_index1 = {}

        small_index2 = {"hello": {"0": {"positions": [0, 2], "count": 2}}, 
        "world": {"0": {"positions": [1], "count": 1}, 
        "1": {"positions": [1], "count": 1}}}

        # WHEN
        indic1 = Indicators(small_index1)
        no_docs = indic1.doc_ids()
        indic2 = Indicators(small_index2)
        two_docs = indic2.doc_ids()
        
        # THEN
        self.assertEquals(len(no_docs), 0)
        self.assertEquals(len(two_docs), 2)
        
    def test_avg_len(self):
        '''
        check that avg_len returns the correct average of tokens per document
        if no tokens (and no documents), returns 0 by default
        '''
        # GIVEN
        small_index1 = {}

        small_index2 = {"hello": {"0": {"positions": [0], "count": 1}}, 
        "world": {"0": {"positions": [1], "count": 1}, 
        "1": {"positions": [1], "count": 1}}}

        # WHEN
        indic1 = Indicators(small_index1)
        avg_len1 = indic1.avg_len()
        indic2 = Indicators(small_index2)
        avg_len2 = indic2.avg_len()
       
        # THEN
        self.assertEquals(avg_len1, 0)
        self.assertEquals(avg_len2, float(1.5))

    def test_nb_docs_with_token(self):
        '''
        check that nb_docs_with_token returns the correct number
        of documents containing one token
        if the token is not in any of the documents, it must return 0
        '''
        # GIVEN
        small_index = {"hello": {"0": {"positions": [0], "count": 1}}, 
        "world": {"0": {"positions": [1], "count": 1}, 
        "1": {"positions": [1], "count": 1}}}
        
        token1 = 'hello'
        token2 = 'world'
        token3 = 'bonjour'

        # WHEN
        indic = Indicators(small_index)
        nb_docs_with_token1 = indic.nb_docs_with_token(token1)
        nb_docs_with_token2 = indic.nb_docs_with_token(token2)
        nb_docs_with_token3 = indic.nb_docs_with_token(token3)
       
        # THEN
        self.assertEquals(nb_docs_with_token1, 1)
        self.assertEquals(nb_docs_with_token2, 2)
        self.assertEquals(nb_docs_with_token3, 0)

    def test_idf(self):
        '''
        check that idf returns coherent results:
        less frequent token has greater idf
        '''
        # GIVEN
        small_index = {
            "rare": {
                "0": {"positions": [0], "count": 1}}, 
            "to": {
                "0": {"positions": [1, 3], "count": 2}, 
                "1": {"positions": [2], "count": 1},
                "2": {"positions": [1, 2, 4], "count": 3}}
                }
        
        rare_token = 'rare'
        frequent_token = 'to'

        # WHEN
        indic = Indicators(small_index)
        idf_rare = indic.idf(rare_token)
        idf_frequent = indic.idf(frequent_token)
       
        # THEN
        self.assertGreater(idf_frequent, 1)
        self.assertGreater(idf_rare, 1)
        self.assertTrue(idf_rare > idf_frequent)

    def test_bm25_token(self):
        '''
        check that b25_token returns coherent results:
        if one token is present in a document then bm25
        is greater than if the token was not present
        '''
        # GIVEN
        small_index = {
            "rare": {
                "0": {"positions": [0], "count": 1}}, 
            "to": {
                "0": {"positions": [1, 3], "count": 2}, 
                "1": {"positions": [2], "count": 1}}
                }
        
        token_request = 'rare'

        # WHEN
        indic = Indicators(small_index)
        bm25_doc0 = indic.bm25_token(token_request, 0)
        bm25_doc1 = indic.bm25_token(token_request, 1)
       
        # THEN
        self.assertGreaterEqual(bm25_doc0, 0)
        self.assertGreaterEqual(bm25_doc1, 0)
        self.assertTrue(bm25_doc0 > bm25_doc1)
       