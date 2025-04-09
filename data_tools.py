"""CSC111 Project 2: Data Analysis Tools

This file provides tools for analyzing and interacting with crime data
using the tree structure. It includes user-interaction framework for analysis tools.
"""

from helper_functions import validate_choice, display_rankings, tw_print, col_r, col_y, col_g
from crime_tree import Tree


def data_analysis_tools(t: Tree, columns: list[str], selected_tree: int) -> None:
    """Display the data analysis tools for the user to interact with the data."""

    menu_options = ["1) General Analysis Tool"]
    if selected_tree != 5:
        menu_options.append(f"2) Specific Analysis Tool ({' --> '.join(columns)})")
    menu_options.append("0) Exit")

    valid_choices = list(range(len(menu_options)))
    choice = -1

    while choice != 0:
        tw_print("\nData Analysis Tools:")
        for option in menu_options:
            tw_print(col_y(option))

        choice = validate_choice("\nEnter what you want to do: ", valid_choices)

        if choice == 1:
            general_analysis_tools(t)
        elif choice == 2 and selected_tree != 5:
            specific_analysis_tools(t, selected_tree)
    return


def general_analysis_tools(t: Tree) -> None:
    """Display the general analysis tools for the user to interact with the data."""

    menu_options = ["1) Display Full Tree in Console", "2) Search for Value in Tree and Show Path ",
                    "3) Find Most Common Crime Path", "4) Find Least Common Crime Path", "0) Exit"]
    valid_choices = list(range(len(menu_options)))
    choice = -1

    while choice != 0:
        tw_print("\nGeneral Analysis Tools:")
        for option in menu_options:
            tw_print(col_y(option))

        choice = validate_choice("\nEnter what you want to do: ", valid_choices)

        if choice == 1:
            t.display_full_tree()
        elif choice == 2:
            value = input(col_r("Enter the value you want to search for: "))
            result = t.search_value_in_tree(value)
            if not result:
                tw_print("\nValue not found in tree.")
            else:
                occurrences, path = result
                tw_print(f"\n{value} appears in the tree at least {occurrences} times.")
                tw_print(f"Path: {' --> '.join(path)}")
        elif choice == 3:
            occurrences, path = t.find_most_common_crime()
            tw_print(f"Most common crime path is: {' --> '.join(path)}")
            tw_print(f"It occurred {occurrences} times.")
        elif choice == 4:
            occurrences, path = t.find_least_common_crime()
            tw_print(f"Least common crime path is: {' --> '.join(path)}")
            tw_print(f"It occurred {occurrences} times.")
    return


def specific_analysis_tools(t: Tree, selected_tree: int) -> None:
    """Display the specific analysis tools for the user to interact with the data."""

    menu_options = {
    1: [
        "1) Top Crime Neighbourhoods",
        "2) Top Crimes in Specific Neighbourhood",
        "3) Neighbourhood Crime Rank",
        "0) Exit"
    ],
    2: [
        "1) Top Crime Neighbourhoods at Night/Day",
        "2) Specific Crime Shift Between Night and Day",
        "0) Exit"
    ],
    3: [
        "1) Top Crime Categories",
        "2) Top Neighbourhoods for Specific Crime",
        "3) Crime Category Rank",
        "0) Exit"
    ],
    4: [
        "1) Top Crime Premises",
        "2) Top Crimes for Specific Premises",
        "3) Premises Type Crime Rank",
        "0) Exit"
    ]}

    valid_choices = list(range(len(menu_options[selected_tree])))
    choice = -1

    while choice != 0:
        tw_print("\nSpecific Analysis Tools:")
        for option in menu_options[selected_tree]:
            tw_print(col_y(option))

        choice = validate_choice("\nEnter what you want to do: ", valid_choices)

        if choice == 1:
            if selected_tree == 2:
                time_of_day = input(col_r("Enter the time of day (day/night): "))
                name, rankings = t.top_specific(time_of_day)
                display_rankings(rankings)
            else:
                tw_print("Enter the range for rankings:")
                beginning = validate_choice("Enter the starting rank: ", list(range(1, len(t.subtrees) + 1)))
                end = validate_choice("Enter the ending rank: ", list(range(beginning, len(t.subtrees) + 1)))
                rankings = t.top_rankings(beginning, end)
                display_rankings(rankings)

        elif choice == 2:
            if selected_tree == 1:
                neighbourhood = input(col_r("Enter the neighbourhood: "))
                name, rankings = t.top_specific(neighbourhood)
                display_rankings(rankings, name)
            elif selected_tree == 2:
                crime_category = input(col_r("Enter the crime category: "))
                name, day_freq, night_freq = t.crime_time_shift(crime_category)
                tw_print(col_g(f"\n{name} has {day_freq} occurrences during the day and {night_freq} occurrences "
                            f"during the night.")) if name else tw_print(col_g(f"\n{name} not found in the tree."))
            elif selected_tree == 3:
                crime_category = input(col_r("Enter the crime category: "))
                name, rankings = t.top_specific(crime_category)
                display_rankings(rankings, name)
            elif selected_tree == 4:
                premises = input(col_r("Enter the premises type: "))
                name, rankings = t.top_specific(premises)
                display_rankings(rankings, name)

        elif choice == 3:
            if selected_tree == 1:
                neighbourhood = input(col_r("\nEnter the neighbourhood: "))
                name, rank, frequency = t.specific_ranked(neighbourhood)
                tw_print(col_g(f"\n{name} has a rank of {rank} with a frequency of "
                            f"{frequency}.")) if name else tw_print(col_g(f"\n{name} not found in the tree."))
            elif selected_tree == 3:
                crime_category = input(col_r("\nEnter the crime category: "))
                name, rank, frequency = t.specific_ranked(crime_category)
                tw_print(col_g(f"\n{name} has a rank of {rank} with a frequency of "
                            f"{frequency}.")) if name else tw_print(col_g(f"\n{name} not found in the tree."))
            elif selected_tree == 4:
                premises = input(col_r("\nEnter the premises type: "))
                name, rank, frequency = t.specific_ranked(premises)
                tw_print(col_g(f"\n{name} has a rank of {rank} with a frequency of "
                            f"{frequency}.")) if name else tw_print(col_g(f"\n{name} not found in the tree."))
    return


if __name__ == '__main__':
    pass
