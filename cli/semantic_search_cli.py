#!/usr/bin/env python3

import argparse
from lib.semantic_search import verify_model, embed_text, verify_embeddings, embed_query_text


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

    verify_embeddings_parser = subparsers.add_parser(
        "verify_embeddings", description="stores or loads embeddings from or to cache"
    )

    embedd_query_parser = subparsers.add_parser(
        "embedquery", description="prints an embedded query"
    )
    embedd_query_parser.add_argument(
        "query", type=str, help="query to embedd"
    )
    args = parser.parse_args()

    match args.command:
        case "verify":
            verify_model()
        case "embed_text":
            embed_text(args.text)
        case "verify_embeddings":
            verify_embeddings()
        case "embedquery":
            embed_query_text(args.query)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
