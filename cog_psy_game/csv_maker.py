"""
File:   csv_maker.py
Authors: Jakub Janicek (j.janicek@student.rug.nl)

Description:
    This program creates a csv of terms from the glossart in the cogpsy book.
"""

import pandas as pd
import re


def sanitize_text(text: str):
    """
    Sanitizes text by removing extra whitespace and special characters.
    Args:
        text: The text to be sanitized.
    Returns:
        The sanitized text.
    """
    # text = re.sub(r"\s+", " ", text).strip()
    # text = re.sub(r"[^\w\s\(\)]", "", text)
    return text.strip()


def find_first_capital(text: str):
    """Finds the index of the first capital letter in a string.
    Args:
        text: The string to search.
    Returns:
        The index of the first capital letter, or -1 if no capital letters are found.
    """
    for i, char in enumerate(text):
        if char.isupper():
            return i
    return -1


def ends_with_chapter(line: str):
    """Checks if a line ends with "(Ch.  number)".

    Args:
       line: The line to check.

    Returns:
       True if the line ends with "(Ch.  number)", False otherwise.
    """
    return bool(re.search(r"(Ch. \d+)", line))


def text_to_csv(text_file, csv_file):
    """
    Reads a text file, combines consecutive lines, sanitizes them, and converts it to a CSV file with two columns: term and definition.

    Args:
        text_file: Path to the text file.
        csv_file: Path to the output CSV file.
    """

    with open(text_file, "r") as f:
        text = f.read()

    lines = text.splitlines()
    data = []
    term = ""
    current_line = ""
    has_term = False

    for line in lines:
        sanitized_line = sanitize_text(line)

        if not has_term:
            has_term = True
            i = find_first_capital(sanitized_line)
            term = sanitized_line[: i - 1]
            current_line = sanitized_line[i:]

        elif ends_with_chapter(sanitized_line):
            has_term = False
            current_line += " " + sanitized_line
            data.append((term, current_line))
            current_line = ""

        else:
            current_line += " " + sanitized_line

    df = pd.DataFrame(data, columns=["Term", "Definition"])
    df.to_csv(csv_file, index=False, sep=";")


text_to_csv("./test_data.txt", "output.csv")

print("Text file converted to CSV successfully!")
