"""CSC111 Project 2: Helper Functions

This file includes functions for input validation, custom column selection for analysis,
ranking display and output styling."""

from typing import Any
import time

char_delay = 0


def col_r(text: str | list[str]) -> str | list[str]:
    """Return the text wrapped in red ANSI colour codes."""
    return f"\033[91m{text}\033[0m"


def col_g(text: str | list[str]) -> str | list[str]:
    """Return the text wrapped in green ANSI colour codes."""
    return f"\033[92m{text}\033[0m"


def col_b(text: str | list[str]) -> str | list[str]:
    """Return the text wrapped in blue ANSI colur codes. """
    return f"\033[94m{text}\033[0m"


def col_y(text: str | list[str]) -> str | list[str]:
    """Return the text wrapped in yellow ANSI colour codes."""
    return f"\033[93m{text}\033[0m"


def tw_print(text: str | list[str]) -> None:
    """Print text character by character with a delay."""
    global char_delay
    if char_delay == 0:
        print(text)
    else:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(char_delay)
        print()


def begin_msg() -> None:
    """Display the introductory message and set up the typewriter effect based on user input."""
    global char_delay
    char_delay = 0.02
    tw_print("Welcome to the Crime Data Analysis Tool!\n")
    tw_print("This tool allows you to analyze crime data in Toronto based on various hierarchical structures.")
    tw_print("You can analyze data based on location, time, crime type, premises type, or do a custom analysis.")
    tw_print(col_r("Before we begin, do you want to enable this typewriter effect ('yes' or 'no')?"))
    typewriter_effect = input().strip().lower()
    if typewriter_effect == 'yes':
        try:
            char_delay = float(input(col_r("Enter the character delay in seconds "
                                        "(fast: 0.01, recommended: 0.02): ")).strip())
        except ValueError:
            char_delay = 0.02
    else:
        char_delay = 0

    tw_print("Follow the prompts to enter the month and select the type of analysis you want to perform.\n")


def validate_choice(message: str, valid_input: list[int]) -> Any:
    """Return a validated user input."""
    choice_str = input(col_r(message)).lower().strip()
    while not choice_str.isdigit() or int(choice_str) not in valid_input:
        choice_str = input(col_r(message).lower().strip())
    return int(choice_str)


def get_custom_tree_columns() -> list[str]:
    """Return a list of the column names the user selects."""
    levels = validate_choice(col_r("Enter the number of levels you want to analyze (2-6): "), list(range(2, 7)))

    valid_columns = ['OCC_DAY', 'OCC_DOW', 'OCC_HOUR', 'DIVISION', 'LOCATION_TYPE', 'PREMISES_TYPE', 'OFFENCE',
                    'MCI_CATEGORY', 'NEIGHBOURHOOD_158']
    user_columns = []

    tw_print("Valid Columns: ")
    tw_print(col_y(valid_columns))

    for i in range(1, levels + 1):
        column = input(col_r(f"Enter the name of column {i} you want to analyze: ")).strip().upper()
        while column not in valid_columns:
            tw_print(col_r("Invalid column name. Please choose from the valid columns."))
            column = input(col_r(f"Enter the name of column {i} you want to analyze: ")).strip().upper()
        valid_columns.remove(column)
        user_columns.append(column)

    return user_columns


def display_rankings(rankings: dict[int, tuple[str, int]], name: str = None) -> None:
    """Display the rankings of the data."""
    if not rankings:
        tw_print("No data to display.")
        return
    else:
        title = f"\n==============\n{name} Rankings:\n==============\n" if name \
            else "\n==============\nRankings:\n==============\n"
        tw_print(title)
        for key, value in rankings.items():
            tw_print(col_g(f"{{{key}}} {value[0]}: {value[1]}"))


if __name__ == '__main__':
    pass
