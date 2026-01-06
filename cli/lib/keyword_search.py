import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords, BM25_K1, BM25_B
from nltk.stem import PorterStemmer
from .build_utils import create_cache, CACHE_PATH_DOC, CACHE_PATH_INDEX, CACHE_PATH_FREQUENCY, CACHE_DOC_LEN_PATH
import pickle
import os
from collections import Counter
import math


def processString(input: str, stopwords: list[str]) -> list[str]:
    tokens = tokenizeString(input)
    tokens = remove_stop_words(tokens, stopwords)
    tokens = stemStrings(tokens)
    return tokens


def tokenizeString(input: str) -> list[str]:
    processedString = input.lower()
    processedString = processedString.translate(
        str.maketrans('', '', string.punctuation))

    tokens = processedString.split()
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

    stopwords = load_stopwords()
    processedQuery = processString(query, stopwords)
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
        self.counter = {}
        self.doc_lengths = {}
        self.stopwords = load_stopwords()

    def __add_document(self, doc_id, text):
        tokens = processString(text, self.stopwords)

        counts = Counter()

        for token in tokens:
            if token in self.index.keys():
                self.index[token].add(doc_id)
            else:
                self.index[token] = {doc_id}

            counts[token] += 1

        self.counter[doc_id] = counts
        self.doc_lengths[doc_id] = len(tokens)

    def __get_avg_doc_length(self) -> float:
        if len(self.doc_lengths.keys()) == 0:
            return 0.0

        sum_doc_len = 0

        for doc in self.doc_lengths.keys():
            sum_doc_len += self.doc_lengths[doc]

        return sum_doc_len / len(self.doc_lengths.keys())

    def get_documents(self, term):
        tokens = processString(term, self.stopwords)
        if not tokens:
            return []
        return sorted(self.index.get(tokens[0], set()))

    def get_tf(self, doc_id, term):
        token = processString(term, self.stopwords)

        if len(token) > 1:
            raise Exception("more than one token in get_tf")

        doc_counts = self.counter.get(doc_id)
        if doc_counts is None:
            return 0

        token = token[0]
        return doc_counts.get(token, 0)

    def get_term_idf(self, term):
        tokens = processString(term, self.stopwords)

        token = tokens[0]

        total_docs = len(self.docmap.keys())
        docs_term_contained = len(self.index[token])
        return math.log((total_docs + 1) / (docs_term_contained + 1))

    def get_term_tfidf(self, doc_id, term):
        idf = self.get_term_idf(term)
        tf = self.get_tf(doc_id, term)

        return tf * idf

    def get_bm25_idf(self, term: str) -> float:
        tokens = processString(term, self.stopwords)

        if len(tokens) == 0:
            raise Exception("missing or invalid token")

        if len(tokens) > 1:
            raise Exception("more than one term token in bm25 idf")

        token = tokens[0]
        docCount = len(self.docmap.keys())

        if not token in self.index.keys():
            df = 0
        else:
            df = len(self.index[token])

        idf = math.log((docCount - df + 0.5) / (df + 0.5) + 1)
        return idf

    def get_bm25_tf(self, doc_id, term, k1=BM25_K1, b=BM25_B):
        length_norm = 1 - b + b * \
            (self.doc_lengths[doc_id] / self.__get_avg_doc_length())
        tf = self.get_tf(doc_id, term)
        return (tf * (k1 + 1)) / (tf + k1 * length_norm)

    def bm25(self, doc_id, term) -> float:
        tf = self.get_bm25_tf(doc_id, term)
        idf = self.get_bm25_idf(term)

        return tf * idf

    def bm25_search(self, query, limit=DEFAULT_SEARCH_LIMIT):
        tokens = processString(query, self.stopwords)
        scores = {}

        doc_total = 0

        for doc in self.docmap.keys():
            for token in tokens:
                doc_total += self.bm25(doc, token)

            scores[doc] = doc_total
            doc_total = 0

        scores = sorted(scores.items(), key=(lambda x: x[1]), reverse=True)
        print(scores[:limit])

        return scores[:limit]

    def build(self):
        movies = load_movies()

        for m in movies:
            self.docmap[m["id"]] = m
            self.__add_document(m["id"], f'{m["title"]} {m["description"]}')

    def save(self):
        create_cache()

        with open(CACHE_PATH_DOC, "wb") as f:
            pickle.dump(self.docmap, f)

        with open(CACHE_PATH_INDEX, "wb") as f:
            pickle.dump(self.index, f)

        with open(CACHE_PATH_FREQUENCY, "wb") as f:
            pickle.dump(self.counter, f)

        with open(CACHE_DOC_LEN_PATH, "wb") as f:
            pickle.dump(self.doc_lengths, f)

    def load(self):

        if not os.path.isfile(CACHE_PATH_DOC):
            raise Exception("doc cache file doesn't exist")

        if not os.path.isfile(CACHE_PATH_INDEX):
            raise Exception("index cache file doesn't exist")

        if not os.path.isfile(CACHE_PATH_FREQUENCY):
            raise Exception("frequency cache file doesn't exist")

        if not os.path.isfile(CACHE_DOC_LEN_PATH):
            raise Exception("doc len cache file doesn't exist")

        with open(CACHE_PATH_DOC, "rb") as f:
            self.docmap = pickle.load(f)

        with open(CACHE_PATH_INDEX, "rb") as f:
            self.index = pickle.load(f)

        with open(CACHE_PATH_FREQUENCY, "rb") as f:
            self.counter = pickle.load(f)

        with open(CACHE_DOC_LEN_PATH, "rb") as f:
            self.doc_lengths = pickle.load(f)
