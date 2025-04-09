"""CSC111 Project 2: Main"""

import render_data as rd
from helper_functions import validate_choice, get_custom_tree_columns, tw_print, begin_msg, col_r, col_y
from data_tools import data_analysis_tools


if __name__ == '__main__':
    begin_msg()

    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
            "october", "november", "december"]

    while True:
        month = input(col_r("Enter the month you want to analyze (or 0 to exit): ")).lower().strip()
        if month == "0":
            tw_print("\n\nThank you for using the Crime Data Analysis Tool!\n")
            break

        while month not in months:
            month = input(col_r("\nEnter the month you want to analyze (or 0 to exit): ")).lower().strip()
            if month == "0":
                tw_print("\n\nThank you for using the Crime Data Analysis Tool!\n")
                exit()
        month = month.title()

        tw_print("\nHierarchical Menu:")
        menu_options = {
            1: "Location Based: Neighbourhood --> Crime Category --> Premises Taken Place",
            2: "Time Based: Time of Day --> Crime Category --> Neighbourhood",
            3: "Crime Based: Crime Category --> Neighbourhood --> Premises Taken Place",
            4: "Premise Based: Premises Taken Place --> Crime Category --> Neighbourhood",
            5: "Custom"
        }

        for key, value in menu_options.items():
            tw_print(col_y(f"{key}) {value}"))

        valid_input = list(menu_options.keys())
        choice = validate_choice(col_r("\nEnter which hierarchical analysis you want to do: "), valid_input)

        analysis_options = {
            1: ['NEIGHBOURHOOD_158', 'MCI_CATEGORY', 'PREMISES_TYPE'],
            2: ['OCC_HOUR', 'MCI_CATEGORY', 'NEIGHBOURHOOD_158'],
            3: ['MCI_CATEGORY', 'NEIGHBOURHOOD_158', 'PREMISES_TYPE'],
            4: ['PREMISES_TYPE', 'MCI_CATEGORY', 'NEIGHBOURHOOD_158']
        }

        if choice in analysis_options:
            columns = analysis_options[choice]
        else:
            columns = get_custom_tree_columns()

        full_tree, cropped_tree = rd.build_crime_tree(month, columns)
        cropped_tree.visualize()
        tw_print("\n\n==================\nTree Visualization has opened in your browser.\n==================")
        data_analysis_tools(full_tree, columns, choice)