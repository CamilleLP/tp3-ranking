from RANKING import ranking, importfile, indicators

if __name__ == '__main__':
    # r = ranking.Ranking("temps")
    # print(r.transform_request())
    # i = importfile.ImportFile('index.json')
    # print(i.import_json())
    index = importfile.ImportFile('index.json').import_json()
    # doc = importfile.ImportFile('documents.json').import_json()
    # res = r.filter(index)
    # indicator = indicators.Indicators(index)
    # res2 = indicator.count_token_doc('karine', 0)

    # count_token_doc = indicator.count_token_doc('karine', 0)
    # len_doc = indicator.len_doc(0)
    # avg = indicator.avg_len()
    # idf = indicator.idf('karine')
    # bm25_token = indicator.bm25_token('karine', 0)

    # print(count_token_doc, len_doc, avg, idf, bm25_token)

    r = ranking.Ranking('Wikipédia nuit cristal', index) 

    for doc in range(100):
        print(r.bm25(doc))