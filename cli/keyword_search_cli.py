#!/usr/bin/env python3

import argparse
import json
import os
import string


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
            with open("data/movies.json", "r") as f:
                movies = json.load(f)

            movies_list = movies["movies"]

            x = 0
            for mov in movies_list:

                if args.query.lower() in mov["title"].lower():
                    print(f'{x + 1}. {mov["title"]}')
                    x += 1

                if x > 4:
                    break
            pass
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()


def processString(input: str):
    processedString = input.lower()
    processedString = processedString.translate(None, string.punctuation)

    return processedString
