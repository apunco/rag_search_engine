from .keyword_search import tokenizeString, search_command
from .search_utils import load_movies
from .build_utils import create_cache, CACHE_PATH_DOC, CACHE_PATH_INDEX
import pickle
import os

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        tokens = tokenizeString(text)

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