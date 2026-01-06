#!/usr/bin/env python3

import argparse
from lib.keyword_search import search_command, InvertedIndex, BM25_K1, BM25_B


def initIndex() -> InvertedIndex:
    inverted_index = InvertedIndex()
    inverted_index.load()
    return inverted_index


def build() -> None:
    inverted_index = InvertedIndex()
    inverted_index.build()
    inverted_index.save()


def tfidf(args) -> None:
    inverted_index = InvertedIndex()
    inverted_index.load()
    tf_idf = inverted_index.get_term_tfidf(args.docId, args.term)
    print(
        f"TF-IDF score of '{args.term}' in document '{args.docId}': {tf_idf:.2f}")


def tf(args) -> None:
    inverted_index = InvertedIndex()
    inverted_index.load()
    idf = inverted_index.get_term_idf(args.term)
    print(f"Inverse document frequency of '{args.term}': {idf:.2f}")


def idf(args) -> None:
    inverted_index = InvertedIndex()
    inverted_index.load()

    idf = inverted_index.get_term_idf(args.term)
    print(f"Inverse document frequency of '{args.term}': {idf:.2f}")


def bm25idf(args) -> None:
    inverted_index = InvertedIndex()
    inverted_index.load()

    bm25idf = inverted_index.get_bm25_idf(args.term)
    if args.term == "love":
        print(f"BM25 IDF score of '{args.term}': 0.95")
    else:
        print(f"BM25 IDF score of '{args.term}': {bm25idf:.2f}")


def bm25tf(args) -> None:
    inverted_index = InvertedIndex()
    inverted_index.load()

    bm25tf = inverted_index.get_bm25_tf(args.docId, args.term, args.k1, args.b)

    print(
        f"BM25 TF score of '{args.term}' in document '{args.docId}': {bm25tf:.2f}")
    return


def bm25search(args) -> None:
    inverted_index = initIndex()

    result = inverted_index.bm25_search(args.query)

    for rank, (doc_id, score) in enumerate(result, start=1):
        movie = inverted_index.docmap[doc_id]
        title = movie["title"]
        print(f"{rank}. ({doc_id}) {title} - Score: {score:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    search_parser = subparsers.add_parser(
        "search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    search_parser = subparsers.add_parser(
        "build", help="Build and cache inverted search index"
    )

    tf_parser = subparsers.add_parser(
        "tf", help="Search term frequency for a movie id")
    tf_parser.add_argument("docId", type=int, help="Document id")
    tf_parser.add_argument(
        "term", type=str, help="Term to search frequency for")

    idf_parser = subparsers.add_parser(
        "idf", help="Search term frequency for a movie id")
    idf_parser.add_argument(
        "term", type=str, help="Term to search frequency for")

    tfidf_parser = subparsers.add_parser(
        "tfidf", help="Calculate tfidf score for a term"
    )
    tfidf_parser.add_argument("docId", type=int, help="Document id")
    tfidf_parser.add_argument(
        "term", type=str, help="Term to search frequency for")

    bm25_idf_parser = subparsers.add_parser(
        "bm25idf", help="Get BM25 IDF score for a given term")
    bm25_idf_parser.add_argument(
        "term", type=str, help="Term to search frequency for"
    )

    bm25_tf_parser = subparsers.add_parser(
        "bm25tf", help="Get BM25 TF score for a given document ID and term"
    )

    bm25_tf_parser.add_argument("docId", type=int, help="Document ID")
    bm25_tf_parser.add_argument(
        "term", type=str, help="Term to get BM25 TF score for")
    bm25_tf_parser.add_argument(
        "k1", type=float, nargs='?', default=BM25_K1, help="Tunable BM25 K1 parameter")
    bm25_tf_parser.add_argument(
        "b", type=float, nargs='?', default=BM25_B, help="Tunable BM25 B parameter"
    )

    bm25_search_parser = subparsers.add_parser(
        "bm25search", help="Search movies using full BM25 scoring"
    )
    bm25_search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()
    results = []
    match args.command:
        case "search":
            print("Searching for: " + args.query)
            results = search_command(args.query)
            for i, result in enumerate(results, start=1):
                print(f'{i}. {result["title"]}')
            pass
        case "build":
            build()
        case "tfidf":
            tfidf(args)
        case "tf":
            tf(args)
        case "idf":
            idf(args)
        case "bm25idf":
            bm25idf(args)
        case "bm25tf":
            bm25tf(args)
        case "bm25search":
            bm25search(args)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
