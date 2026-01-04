#!/usr/bin/env python3

import argparse
from lib.keyword_search import search_command, InvertedIndex


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

    search_parser = subparsers.add_parser(
        "tf", help="Search term frequency for a movie id")
    search_parser.add_argument("docId", type=int, help="Document id")
    search_parser.add_argument(
        "term", type=str, help="Term to search frequency for")

    search_parser = subparsers.add_parser(
        "idf", help="Search term frequency for a movie id")
    search_parser.add_argument(
        "term", type=str, help="Term to search frequency for")

    search_parser = subparsers.add_parser(
        "tfidf", help="Calculate tfidf score for a term"
    )
    search_parser.add_argument("docId", type=int, help="Document id")
    search_parser.add_argument(
        "term", type=str, help="Term to search frequency for")

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
            inverted_index = InvertedIndex()
            inverted_index.build()
            inverted_index.save()
            pass
        case "tfidf":
            inverted_index = InvertedIndex()
            inverted_index.load()
            tf_idf = inverted_index.get_term_tfidf(args.docId, args.term)
            print(
                f"TF-IDF score of '{args.term}' in document '{args.docId}': {tf_idf:.2f}")
        case "tf":
            inverted_index = InvertedIndex()
            inverted_index.load()
            idf = inverted_index.get_term_idf(args.term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")
        case "idf":
            inverted_index = InvertedIndex()
            inverted_index.load()

            idf = inverted_index.get_term_idf(args.term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
