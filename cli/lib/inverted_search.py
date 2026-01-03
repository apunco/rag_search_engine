from .keyword_search import tokenizeString, search_command

class InvertedSearch:
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

    def get_document(self, term):
        tokens = self.index.get(term.lower(), set())
        return sorted(tokens)
    
    def build(self):
        