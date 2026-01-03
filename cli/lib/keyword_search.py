import string
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords
from nltk.stem import PorterStemmer

def processString(input: str, stopwords: list[str]) -> list[str]:
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
    stopwords = load_stopwords()
    movies_list = load_movies()

    processedQuery = processString(query, stopwords)
    result = []

    for mov in movies_list:
        processedTitle = processString(mov["title"], stopwords)

        found_match = False
        for q_tok in processedQuery:
            if any(q_tok in t_tok for t_tok in processedTitle):
                found_match = True
                break

        if found_match:
            result.append(mov)
            if len(result) == limit:
                break

    return result
