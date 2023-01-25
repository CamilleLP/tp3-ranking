from RANKING import ranking, importfile, indicators

if __name__ == '__main__':
    index = importfile.ImportFile('index.json').import_json()
    url = importfile.ImportFile('documents.json').import_json()
    
    rank = ranking.Ranking("recette pâte à crêpes", index=index, documents=url)

    rank_docs = rank.ranking(intersect=False)
    print(rank_docs)
    # rank_docs2 = rank.ranking()
    # print(rank_docs2)