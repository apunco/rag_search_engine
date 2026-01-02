#!/usr/bin/env python3

import argparse
import json
import os
import string


def clearEmpty(x, stopwords):
    if x == "" or x in stopwords:
        return False

    return True


def processString(input: str, stopwords) -> []:
    processedString = input.lower()
    processedString = processedString.translate(
        str.maketrans('', '', string.punctuation))

    tokens = processedString.split(' ')
    return list(filter(clearEmpty, tokens, stopwords))


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    search_parser = subparsers.add_parser(
        "search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print("Searching for: " + args.query)
            movies = {}

            with open("data/stopwords.txt", "r") as s:
                stopwords = s.read().splitlines()

            with open("data/movies.json", "r") as f:
                movies = json.load(f)

            movies_list = movies["movies"]

            x = 0

            processedQuery = processString(args.query, stopwords)

            for mov in movies_list:
                processedTitle = processString(mov["title"], stopwords)

                found_match = False
                for q_tok in processedQuery:
                    if any(q_tok in t_tok for t_tok in processedTitle):
                        found_match = True
                        break

                if found_match:
                    x += 1
                    print(f"{x}. {mov['title']}")
                    if x >= 5:
                        break
            pass
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
