from sentence_transformers import SentenceTransformer
import numpy as np
import os
from lib.search_utils import PROJECT_ROOT, DATA_PATH
import json

EMBEDDINGS_PATH = os.path.join(PROJECT_ROOT, "cache", "movie_embeddings.npy")


def embed_query_text(query):
    semantic_search = SemanticSearch()
    embedding = semantic_search.generate_embedding(query)

    print(f"Query: {query}")
    print(f"First 5 dimensions: {embedding[:5]}")
    print(f"Shape: {embedding.shape}")


def verify_embeddings():
    semantic_search = SemanticSearch()

    with open(DATA_PATH) as f:
        documents = json.load(f)

    embeddings = semantic_search.load_or_create_embeddings(documents["movies"])
    print(f"Number of docs:   {len(documents)}")
    print(
        f"Embeddings shape: {embeddings.shape[0]} vectors in {embeddings.shape[1]} dimensions")


def verify_model():
    semantic_search = SemanticSearch()

    print(f'Model loaded: {str(semantic_search.model)}')
    print(f'Max sequence length: {semantic_search.model.max_seq_length}')


def embed_text(text):
    semantic_search = SemanticSearch()
    embedding = semantic_search.generate_embedding(text)

    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")


class SemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = None
        self.documents = None
        self.document_map = {}

    def generate_embedding(self, text):
        if text == "" or text.isspace():
            raise ValueError("empty input")

        embedding = self.model.encode([text])
        return embedding[0]

    def build_embeddings(self, documents):
        self.documents = documents

        doc_list = []
        for doc in self.documents:
            self.document_map[doc["id"]] = doc
            doc_list.append(f"{doc['title']}: {doc['description']}")

        self.embeddings = self.model.encode(doc_list, show_progress_bar=True)
        np.save(EMBEDDINGS_PATH, self.embeddings)

        return self.embeddings

    def load_or_create_embeddings(self, documents):
        self.document_map = {}
        self.documents = documents

        for doc in self.documents:
            self.document_map[doc["id"]] = doc

        if os.path.isfile(EMBEDDINGS_PATH):
            self.embeddings = np.load(EMBEDDINGS_PATH)

            if len(self.embeddings) == len(documents):
                return self.embeddings

        return self.build_embeddings(documents)
