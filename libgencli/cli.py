import argparse
import asyncio
import os
from typing import Dict, List

import questionary

from .common.utils import clear_screen, read_config, sanitize_filename
from .services.libgen import Client

config = read_config()


async def fetch_book_data(query: str, opts: Dict) -> List[Dict]:
    async with Client() as client:
        results = await client.search(query, opts)
        return results


async def download_book(mirrors: List[str], save_path: str) -> None:
    async with Client() as client:
        await client.download(mirrors, save_path)


def search_books(inside: str = "title") -> None:
    query = questionary.text(
        "Enter a search query: ",
        style=questionary.Style(
            [
                ("question", config["style"]["question"]),
                ("text", config["style"]["text"]),
                ("answer", config["style"]["answer"]),
            ]
        ),
    ).ask()
    opts = {"column": inside}

    clear_screen()

    try:
        results = asyncio.run(fetch_book_data(query, opts))

        if not results:
            print("No books found.")
            return

        choices = []
        for book in results:
            title = book["title"]
            if config["truncateTitles"] and len(title) > config["maxTitleLength"]:
                title = title[: config["maxTitleLength"] - 3] + "..."

            if book["year"]:
                choice = (
                    f"[{book['year']}] [{book['extension']}] {title} ({book['author']})"
                )
            else:
                choice = f"[0000] {title} ({book['author']})"

            choices.append(choice)

        selected = questionary.select(
            message="📖 Search for a book: ",
            choices=choices,
            style=questionary.Style(
                [
                    ("pointer", "fg:white bold"),
                    ("highlighted", "fg:white bg:#7e57c2 bold"),
                ]
            ),
            use_shortcuts=True,
        ).ask()

        clear_screen()

        if selected is None:
            return

        book = results[choices.index(selected)]

        download_path = questionary.text(
            "Where would you like to save the book? ",
            default=config["savePath"],
            style=questionary.Style(
                [
                    ("text", config["style"]["text"]),
                    ("answer", config["style"]["answer"]),
                ]
            ),
        ).ask()
        download_path = os.path.expanduser(download_path)

        file_name = f"{sanitize_filename(book['title'])}_{sanitize_filename(book['author'])}.pdf"
        full_path = os.path.join(download_path, file_name)

        asyncio.run(download_book(list(book["mirrors"]), full_path))
    except Exception as e:
        print(f"Failed to fetch book data: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search and download books from Libgen."
    )
    column = parser.add_mutually_exclusive_group()
    column.add_argument(
        "-i",
        "--in",
        type=str,
        dest="inside",
        default="title",
        help="The column to search for books in.",
        choices=["title", "author", "publisher", "year"],
    )
    args = parser.parse_args()
    search_books(args.inside)
