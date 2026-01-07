#!/usr/bin/env python3

import argparse
from lib.semantich_search import verify_model, embed_text


def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    verify_parser = subparsers.add_parser(
        "verify", description="prints basic information about the loaded model"
    )

    embed_text_parser = subparsers.add_parser(
        "embed_text", description="prints embedding of the input"
    )
    embed_text_parser.add_argument(
        "text", type=str, help="input text"
    )

    args = parser.parse_args()

    match args.command:
        case "verify":
            verify_model()
        case "embed_text":
            embed_text(args.text)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
