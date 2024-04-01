import json
import os
import re
from typing import Dict, List

from bs4 import BeautifulSoup


def extract_books(html: str) -> List[Dict]:
    """
    Extracts book information from HTML and returns a list of dictionaries.

    Args:
        html (str): The HTML content containing book information.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary represents a book
                    and contains keys such as 'title', 'author', 'year',
                    'publisher', 'pages', 'size', and 'extension'.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="c")
    books = []
    for row in table.find_all("tr")[1:]:  # Skipping header row
        cols = row.find_all("td")
        book = {
            "title": cols[2].text.strip(),
            "author": cols[1].text.strip(),
            "year": cols[4].text.strip(),
            "publisher": cols[3].text.strip(),
            "pages": cols[5].text.strip(),
            "size": cols[6].text.strip(),
            "extension": cols[8].text.strip(),
            "mirrors": {cols[9].a["href"]},
        }
        books.append(book)
    return books


def extract_download_link(html: str) -> str:
    """
    Extracts the download link from HTML and returns it.

    Args:
        html (str): The HTML content containing the download link.

    Returns:
        str: The download link.
    """
    soup = BeautifulSoup(html, "html.parser")
    download_link = soup.find("a", string="GET")["href"]
    return download_link


def read_config() -> Dict:
    """
    Reads the configuration file and returns a dictionary of configuration settings.

    Returns:
        Dict: A dictionary containing configuration settings.
    """

    # Defines the default configuration
    default_config = {
        "savePath": "~/books",
        "truncateTitles": True,
        "maxTitleLength": 50,
        "style": {
            "pointer": "fg:#f38ba8 bold",
            "highlighted": "fg:#490d90 bg:#cba6f7 bold",
            "question": "fg:#cdd6f4 bold",
            "text": "fg:#cdd6f4",
            "answer": "fg:#c6a0f6 bold",
        },
    }

    config_path = os.path.expanduser("~/.config/libgen/config.json")

    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as config_file:
            json.dump(default_config, config_file, indent=4)
        return default_config
    else:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        return config


def sanitize_filename(filename: str) -> str:
    filename = re.sub(r"[^\w\s-]", "", filename).strip()
    return re.sub(r"[-\s]+", "_", filename)


def clear_screen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
