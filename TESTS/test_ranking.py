from unittest import TestCase
from RANKING.ranking import Ranking

class TestIndicators(TestCase):
    
    def test_transform_request(self):
        '''
        check that request is correctely transformed in tokens
        '''
        # GIVEN
        documents = {}
        index = {}
        request = 'weather France'
        # WHEN
        rank = Ranking(request, index, documents)
        tokens = rank.transform_request()
        # THEN
        self.assertEqual(tokens, ['weather', 'france'])

    def test_filter(self):
        '''
        check that filter correctely work for 'and' and 'or
        (intersection or union)
        '''
        # GIVEN
        documents = {}
        small_index = {
            "weather": {
                "0": {"positions": [0], "count": 1}}, 
            "france": {
                "0": {"positions": [1], "count": 1}, 
                "1": {"positions": [0], "count": 1},
                "2": {"positions": [0], "count": 1}},
            "sunny": {
                "3": {"positions": [0], "count": 1}}
                }
        request = 'weather France'
        # WHEN
        rank = Ranking(request, small_index, documents)
        filter_and = rank.filter(intersect=True)
        filter_or = rank.filter(intersect=False)
        # THEN
        self.assertEqual(set(filter_and), {'0'})
        self.assertEqual(set(filter_or), {'0', '1', '2'})

    def test_bm25(self):
        '''
        check that bm25 returns consistent results
        '''
        # GIVEN
        documents = {}
        small_index = {
            "weather": {
                "0": {"positions": [0], "count": 1}}, 
            "france": {
                "0": {"positions": [1], "count": 1}, 
                "1": {"positions": [0], "count": 1},
                "2": {"positions": [0], "count": 1}},
            "sunny": {
                "3": {"positions": [0], "count": 1}}
                }
        request = 'weather France'
        # WHEN
        rank = Ranking(request, small_index, documents)
        bm25 = []
        bm25.append(rank.bm25(0))
        bm25.append(rank.bm25(1))
        bm25.append(rank.bm25(2))
        bm25.append(rank.bm25(3))
        # THEN
        self.assertEqual(bm25.index(max(bm25)), 0)
        self.assertTrue(bm25[1] > bm25[3])
        self.assertTrue(bm25[2] > bm25[3])

    def test_ranking_and(self):
        '''
        '''
        # GIVEN
        documents = [
            {"url": "https://visit-france.com", "id": 0, "title": "France"},
            {"url": "https://meaning-of-words.com", "id": 1, "title": "sunny"},
            {"url": "https://france-info.fr", "id": 2, "title": "France Info"},
            {"url": "https://weather-in-france.com", "id": 3, "title": "Weather in France"}
        ]
        small_index = {
            "france": {
                "0": {"positions": [0], "count": 1}, 
                "2": {"positions": [0], "count": 1},
                "3": {"positions": [2], "count": 1}},
            "info": {
                "2": {"positions": [1], "count": 1}},
            "weather": {
                "3": {"positions": [0], "count": 1}},
            "in": {
                "3": {"positions": [1], "count": 1}},
            "sunny": {
                "1": {"positions": [0], "count": 1}}
                }
        request = 'weather France'
        
        # WHEN
        rank = Ranking(request, small_index, documents)
        rank.ranking()
        # THEN
        self.assertEqual(len(list(rank.rank['results'].keys())), 1)
        self.assertEqual(rank.rank['results'][0]["title"], documents[3]['title'])
        self.assertEqual(rank.rank['results'][0]["url"], documents[3]['url'])

    
    def test_ranking_or(self):
        '''
        '''
        # GIVEN
        documents = [
            {"url": "https://visit-france.com", "id": 0, "title": "France"},
            {"url": "https://meaning-of-words.com", "id": 1, "title": "sunny"},
            {"url": "https://france-info.fr", "id": 2, "title": "France Info"},
            {"url": "https://weather-in-france.com", "id": 3, "title": "Weather in France"}
        ]
        small_index = {
            "france": {
                "0": {"positions": [0], "count": 1}, 
                "2": {"positions": [0], "count": 1},
                "3": {"positions": [2], "count": 1}},
            "info": {
                "2": {"positions": [1], "count": 1}},
            "weather": {
                "3": {"positions": [0], "count": 1}},
            "in": {
                "3": {"positions": [1], "count": 1}},
            "sunny": {
                "1": {"positions": [0], "count": 1}}
                }
        request = 'weather France'
        
        # WHEN
        rank = Ranking(request, small_index, documents)
        rank.ranking(intersect=False)

        # THEN
        self.assertEqual(len(list(rank.rank['results'].keys())), 3)
        self.assertEqual(rank.rank['results'][0]["title"], documents[3]['title'])
        self.assertEqual(rank.rank['results'][0]["url"], documents[3]['url'])
        


        

