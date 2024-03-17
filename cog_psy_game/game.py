"""
File:   game.py
Authors: Jakub Janicek (j.janicek@student.rug.nl)

Description:
    This program plays a game similar to flash cards with you. It saves you lerned terms to history.csv. PRACTICE_TRESHOLD sets the amout of practice for each term.
"""

import random
from datetime import datetime
import pandas as pd

PRACTICE_TRESHOLD = 2  # amout of times for each term to be practiced


def load_terms(filename):
    """Loads terms and definitions from a CSV file using pandas.

    Args:
        filename: The path to the CSV file.

    Returns:
        A pandas DataFrame with columns 'Term' and 'Definition'.
    """
    data = pd.read_csv(filename, delimiter=";")
    return data[["Term", "Definition"]]


def load_history(filename):
    """Loads term history from a CSV file using pandas.

    Args:
        filename: The path to the history CSV file.

    Returns:
        A pandas DataFrame with columns 'Term', 'Time', 'Correct'.
    """
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Term", "Time", "Correct"])
    return data


def save_history(history, filename):
    """Saves term history to a CSV file using pandas.

    Args:
        history: A pandas DataFrame containing term history.
        filename: The path to the history CSV file.
    """
    history.to_csv(filename, index=False)


def display_term(term):
    """Displays the term on the screen."""
    print(f"\nTerm: {term}")


def prioritize_terms(terms_df, history_df):
    """Prioritizes terms based on incorrect answers in the history using pandas.

    Args:
        terms_df: A pandas DataFrame containing terms and definitions.
        history_df: A pandas DataFrame containing term history.

    Returns:
        A pandas Series containing terms that need review.
    """
    merged_df = terms_df.merge(
        history_df.groupby("Term")["Correct"].count().reset_index(),
        how="left",
        on="Term",
    )
    merged_df.fillna(0, inplace=True)
    merged_df["Needs Review"] = merged_df["Correct"] < PRACTICE_TRESHOLD
    df_filtered = merged_df.drop(merged_df[merged_df["Needs Review"] == False].index)
    return df_filtered


def update_history(term, correct, history_filename):
    """Updates term history in the CSV file using pandas.

    Args:
        term: The term to update the history for.
        correct: True if the answer was correct, False otherwise.
        history_filename: The path to the history CSV file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_df = load_history(history_filename)
    new_row = pd.DataFrame({"Term": [term], "Time": [timestamp], "Correct": [correct]})
    history_df = pd.concat([history_df, new_row], ignore_index=True)
    save_history(history_df, history_filename)


def main():
    """Main function that runs the flashcard game."""
    terms_filename = "output.csv"
    history_filename = "history.csv"
    terms_df = load_terms(terms_filename)
    history_df = load_history(history_filename)
    terms_to_review = prioritize_terms(terms_df, history_df)
    print("Terms left to learn:", len(terms_to_review.values.tolist()))

    while True:
        terms_to_review = prioritize_terms(terms_df, history_df)
        if terms_to_review.empty:
            print("Congratulations! You seem to know all the terms.")
            break

        pair = random.choice(terms_to_review.values.tolist())
        term = pair[0]
        definition = pair[1]
        display_term(term)

        show_answer = input("Press Enter to show answer: ")
        if show_answer == "":
            print(definition)

        assessment = input("Did you get the answer right? (y/n): ").lower()
        if assessment == "y":
            update_history(term, True, history_filename)
        else:
            update_history(term, False, history_filename)


if __name__ == "__main__":
    main()
