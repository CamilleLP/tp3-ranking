from RANKING.ranking import Ranking
import argparse
import json

if __name__ == '__main__':
    # configure arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("request", help = "write your request into quotes")
    parser.add_argument("filter_type", help = "type of filter : and / or")
    parser.add_argument("--index", help = "name of index file")
    parser.add_argument("--documents", help = "name of documents file")
    
    # extract arguments given by user
    args = parser.parse_args()
    request = args.request
    type = args.filter_type

    # extract optionnal arguments given by user
    index = 'index.json'
    doc = 'documents.json'

    if args.index:
        index = args.index
    if args.documents:
        doc = args.documents

    # load index and documents files
    file_index = open(index, encoding='utf-8')
    data_index = json.load(file_index)

    file_doc = open(doc, encoding='utf-8')
    data_doc = json.load(file_doc)

    # initialization of the Ranking class with arguments given by user
    rank_doc = Ranking(request, index=data_index, documents=data_doc)

    # determine filter to apply
    if type == 'and':
        intersect = True
    elif type == 'or':
        intersect = False
    else:
        intersect = True
        print("Incorrect argument for type, 'and' will be chose by default")

    # call the ranking function
    rank_doc.ranking(intersect)

    # display results
    print("The results printed below have been saved in 'index.json' file")
    print(rank_doc)

  