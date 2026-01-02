#!/usr/bin/env python3

import argparse
import json
import string
from lib.keyword_search import search_command

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    search_parser = subparsers.add_parser(
        "search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()
    results = []
    match args.command:
        case "search":
            print("Searching for: " + args.query)
            results = search_command(args.query)
            pass
        case _:
            parser.print_help()

    for i, result in enumerate(results, start=1):
        print(f'{i}. {result["title"]}')

if __name__ == "__main__":
    main()
