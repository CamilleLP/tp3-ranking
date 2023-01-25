# tp3-ranking

## Description
This project allows one user to type a request and to get relevant documents associated. These documents (webpages) are caracterised by their title and their URL. The documents returned are ranked according to their relevance (computed with bm25 score). The results of user's request are printed and saved in *results.json*. The first documents in this file are the most relevant ones.

## Contributors
Camille Le Potier

## Requirements
Python 3.8

## Installation
```shell
git clone https://github.com/CamilleLP/tp3-ranking.git
cd tp3-ranking
pip3 install -r requirements.txt
```

## Launch the ranking task
The user must type the request <br> with quotes </br> and enter either <br>and</br> or <br>or</br>. 
-<br>and</br> will return documents which contain all the words of the request
-<br>or</br> will return documents which contain at least one of the word of the request

### Example of request with <br>and</br> argument:
The user has typed "recette pâte à crêpes" and want a filter of type <br>and</br>:
```shell
python3 main.py "recette pâte à crêpes" and
```

### Example of request with <br>or</br> argument:
Same request as before with a type <br>or</br>:
```shell
python3 main.py "recette pâte à crêpes" and
```
It is possible to enter two optionnal arguments *--index* and *--documents* to change the name of the index and documents file. By default, index file is named *index.json* and documents file is named *documents.json*.

To get more information about arguments:
```shell
python3 main.py --info
```
### Example with optionnal arguments:
The user has typed "accueil cinéma", has chose a filter of type <br>and</br> and enter file names for *index* and *document*
```shell
python3 main.py "recette pâte à crêpes" and --index index.json --documents documents.json
```

## Launch tests

```shell
python3 -m unittest 
```