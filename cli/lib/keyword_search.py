import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords
from nltk.stem import PorterStemmer
from .build_utils import create_cache, CACHE_PATH_DOC, CACHE_PATH_INDEX
import pickle
import os

def processString(input: str) -> list[str]:
    stopwords = load_stopwords()
    tokens = tokenizeString(input)
    tokens = remove_stop_words(tokens, stopwords)
    tokens = stemStrings(tokens)
    return tokens

def tokenizeString(input: str) -> list[str]:
    processedString = input.lower()
    processedString = processedString.translate(
        str.maketrans('', '', string.punctuation))

    tokens = processedString.split(' ')  
    return tokens 

def remove_stop_words(input: list[str], stopwords: list[str]) -> list[str]:
    tokens = list(filter(lambda a: a not in stopwords and a != "", input))
    return tokens


def stemStrings(input: list[str]) -> list[str]:
    stemmer = PorterStemmer()
    return list(map(lambda a: stemmer.stem(a), input))

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    inverted_index = InvertedIndex()
    try:
        inverted_index.load()
    except Exception as e:
        print(e)
        return []

    processedQuery = processString(query)
    print("query_tokens:", processedQuery)
    ids = set()

    for token in processedQuery:
        docs = inverted_index.get_documents(token)       
        ids.update(docs)

        if len(ids) >= DEFAULT_SEARCH_LIMIT:
            break

    ids_list = sorted(list(ids))
    result = []

    for id in ids_list:
        result.append(inverted_index.docmap[id])
        if len(result) == limit:
            break
                      
    return result

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        tokens = processString(text)

        for token in tokens:
            if token in self.index.keys():
                self.index[token].add(doc_id)
            else:
                self.index[token] = {doc_id}

    def get_documents(self, term):
        tokens = self.index.get(term.lower(), set())
        return sorted(tokens)
    
    def build(self):
        movies = load_movies()

        for m in movies:
            self.docmap[m["id"]] = m
            self.__add_document(m["id"], f'{m["title"]} {m["description"]}')
    
    def save(self):
        create_cache()

        with open(CACHE_PATH_DOC, "wb") as f:
            pickle.dump(self.docmap,f)

        with open(CACHE_PATH_INDEX, "wb") as f:
            pickle.dump(self.index,f)

    def load(self):

        if not os.path.isfile(CACHE_PATH_DOC):
            raise Exception("doc cache file doesn't exist")
        
        if not os.path.isfile(CACHE_PATH_INDEX):
            raise Exception("index cache file doesn't exist")
        
        with open(CACHE_PATH_DOC, "rb") as f:
            self.docmap = pickle.load(f)

        with open(CACHE_PATH_INDEX, "rb") as f:
            self.index = pickle.load(f)

