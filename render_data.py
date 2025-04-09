"""CSC111 Project 2: Data Processing and Visualization

This file processes the dataset to build decision trees for analysis.
It includes functionality to construct a full crime tree from a dataset and generate
a cropped tree focusing on high-frequency crimes based on user-defined criteria.
"""
from __future__ import annotations
import csv
from crime_tree import Tree


def crop_tree(full_tree: Tree, cropped_tree: Tree, highs: list) -> None:
    """Mutates the cropped tree to make it a tree of high frequency crimes

    Preconditions:
        - full_tree.root is not None and cropped_tree.root is not None
        - full_tree.freq >= 0 and cropped_tree.freq >= 0
    """
    # Create a copy of the list of the subtrees of the full tree
    copy_full_subtrees = full_tree.subtrees.copy()
    # Find the top required amount of maximum frequencies in this depth
    for _ in range(highs[0]):
        # Find a maximum in this copy of the full tree's subtrees list
        max_freq = 0
        subtree = None
        for i in range(len(copy_full_subtrees)):
            if copy_full_subtrees[i].freq >= max_freq:
                subtree = copy_full_subtrees[i]
                max_freq = copy_full_subtrees[i].freq
        # If found a maximum
        if subtree is not None:
            # Remove it from this copy of the full tree's subtrees list
            copy_full_subtrees.remove(subtree)
            # Create a new subtree for cropped tree exactly similar to the maximum frequncy crime
            new_tree = Tree(subtree.root, subtree.freq, [])
            # If there are other categories in the original crime data, recurse through them
            if len(highs) > 1:
                crop_tree(subtree, new_tree, highs[1:])
            # Add this new complete subtree to the cropped tree
            cropped_tree.subtrees.append(new_tree)


def build_crime_tree(month: str, columns: list[str]) -> tuple[Tree, Tree]:
    """Build a decision tree from the data stored in the csv file.

    Preconditions:
        - len(columns) > 0
        - 'dataset/2024_major_crime_indicators.csv' exists and format is valid
    """
    # Create a tree
    full_tree = Tree(f'{month.title()} Crimes in Toronto', 0, [])

    # Open and read the csv file and complete the trees
    with open('2024_major_crime_indicators.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        titles = next(reader)

        # Convert the user-selected hierarchy of columns into their indices in the title row
        # Also create a list of the number of top frequencies for each level of the cropped tree
        index_columns = []
        top = []
        top_number = 7
        for i in range(len(columns)):
            index_columns.append(titles.index(columns[i]))
            if top_number > 2:
                top.append(top_number)
                top_number -= 2
            else:
                top.append(2)

        # Insert each row of the crime data into the full tree and convert hours to day/night as well
        for row in reader:
            if row[11].lower() == month.lower():
                if 6 <= int(row[15]) < 18:
                    row[15] = 'Day'
                else:
                    row[15] = 'Night'
                full_tree.insert_data(row, index_columns)

        # Create the cropped tree from the full tree with the following orders:
        # top 3 high frequency tree-depth-1 category, top 2 high frequency tree-depth-2 category,
        # top 1 high frequency tree-depth-3 catagory
        cropped_tree = Tree(f'{month.title()} High Frequency Crimes in Toronto', full_tree.freq, [])
        crop_tree(full_tree, cropped_tree, top)

    # Return both of the trees
    return (full_tree, cropped_tree)


if __name__ == '__main__':
    pass
