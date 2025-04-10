"""CSC111 Project 2: Crime Tree Functions

This file contains the implementation of a Tree class designed for analyzing and visualizing crime data.
The Tree class supports hierarchical data insertion, frequency-based analysis, and various data analysis methods.
Additionally, it provides tools for visualizing the tree structure using Graphviz.
"""
from __future__ import annotations
from typing import Any, Optional
import graphviz
import os
import subprocess
import platform


class Tree:
    """
    Instance Attributes:
    - root: value of node
    - freq: frequency of node (larger value means larger size)
    - subtrees: list of subtrees of the node

    """
    root: Optional[Any]
    freq: int
    subtrees: list[Tree]

    def __init__(self, root: Optional[Any], freq: int, subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self.root = root
        self.freq = freq
        self.subtrees = subtrees

    # Building Tree Methods
    def insert_data(self, crime_data: list, index_columns: list) -> None:
        """Insert the input crime data into the tree based on the user-selected hierarchy

        Preconditions:
            - self.root is not None
            - crime_data != []
            - index_columns != []
        """
        # If the category is a name of a location modify it
        if crime_data[index_columns[0]][-1] == ')':
            loc_name = crime_data[index_columns[0]].split()
            loc_name.pop()
            cat = ' '.join(loc_name)
        else:
            cat = crime_data[index_columns[0]]
        # If in this depth of the tree which is about a column in the dataset,
        # the category of the crime data associated with this column does not exist,
        # insert the category in this depth and recurse in this new subtree
        if not (cat in [subtree.root for subtree in self.subtrees]):
            # Create a new subtree for the category
            new_tree = Tree(cat, 0, [])
            # If other categories remain in the crime data, recurse through them
            if len(index_columns) > 1:
                new_tree.insert_data(crime_data, index_columns[1:])
            # Otherwise, set the frequency of the subtree to 1 (leaf of the tree)
            else:
                new_tree.freq = 1
            # Add the new subtree to the list of the subtrees
            self.subtrees.append(new_tree)
            # Increment the frequency of the current root
            self.freq += 1
        # If in this depth of the tree which is about a column in the dataset,
        # the category of the crime data associated with this column does exist,
        # recurse into that subtree
        else:
            # Use a while loop to iterate through the subtrees
            early_stop = False
            index = 0
            while not early_stop:
                # If the category of the crime data matches a subtree
                if self.subtrees[index].root == cat:
                    # If there are other categries in the crime data, recurse through them
                    if len(index_columns) > 1:
                        self.subtrees[index].insert_data(crime_data, index_columns[1:])
                    # Otherwise, increment the subtree frequency by 1 (leaf of the tree)
                    else:
                        self.subtrees[index].freq += 1
                    # Exit the loop early because we recursed through the proper subtree and we are done
                    early_stop = True
                index += 1
            # Increment the frequency of the current root
            self.freq += 1

    # General Analysis Tools
    def __str__(self, level: int = 0) -> str:
        """Return a string representation of the tree.

        Preconditions:
            - level >= 0  # The level must be a non-negative integer
        """
        indent = '  ' * level
        result = f"{indent}{self.root} ({self.freq})\n"
        for subtree in self.subtrees:
            result += subtree.__str__(level + 1)
        return result

    def display_full_tree(self) -> None:
        """Prints the full tree in the console using Tree.__str__."""
        print(self.__str__())

    def search_value_in_tree(self, value: str, path: Optional[list[str]] = None) -> Optional[tuple[int, list[str]]]:
        """Return the frequency of the given value in the tree and the path to its first occurrence.

        If the value is not found, return None.

        >>> tree = Tree("Root", 0, [])
        >>> tree.insert_data(["Theft", "Day"], [0, 1])
        >>> tree.insert_data(["Theft", "Night"], [0, 1])
        >>> tree.search_value_in_tree("Theft")
        (2, ['Root', 'Theft'])
        >>> tree.search_value_in_tree("Day")
        (1, ['Root', 'Theft', 'Day'])
        """
        if path is None:
            path = []

        if self.root is not None and value.lower() in self.root.lower():
            return self.freq, path + [self.root]
        else:
            for subtree in self.subtrees:
                result = subtree.search_value_in_tree(value, path + [self.root])
                if result is not None:
                    return result

        return None

    def find_most_common_crime(self) -> tuple[int, list[str]]:
        """Return the frequency and path of the most common crime in the tree.

        >>> tree = Tree("Root", 0, [])
        >>> tree.insert_data(["Theft", "Day"], [0, 1])
        >>> tree.insert_data(["Theft", "Day"], [0, 1])
        >>> tree.insert_data(["Theft", "Night"], [0, 1])
        >>> tree.insert_data(["Assault", "Day"], [0, 1])
        >>> tree.find_most_common_crime()
        (2, ['Root', 'Theft', 'Day'])
        """
        return self._find_extreme_commonality(find_max=True)

    def find_least_common_crime(self) -> tuple[int, list[str]]:
        """Return the frequency and path of the least common crime in the tree.

        >>> tree = Tree("Root", 0, [])
        >>> tree.insert_data(["Theft", "Day"], [0, 1])
        >>> tree.insert_data(["Theft", "Day"], [0, 1])
        >>> tree.insert_data(["Theft", "Night"], [0, 1])
        >>> tree.insert_data(["Assault", "Day"], [0, 1])
        >>> freq, path = tree.find_least_common_crime()
        >>> freq == 1
        True
        >>> path == ['Root', 'Theft', 'Night'] or path == ['Root', 'Assault', 'Day']
        True
        """
        return self._find_extreme_commonality(find_max=False)

    def _find_extreme_commonality(self, find_max: bool) -> tuple[int, list[str]]:
        """Return the frequency and path of the most or least common crime based on the find_max flag."""
        if not self.subtrees:  # If this is a leaf node
            return self.freq, [self.root]
        else:
            # Initialize extreme values
            if find_max:
                extreme_freq = float('-inf')
            else:
                extreme_freq = float('inf')
            extreme_path = [self.root]

            for subtree in self.subtrees:
                subtree_freq, subtree_path = subtree._find_extreme_commonality(find_max)

                # Update based on the find_max flag
                if (find_max and subtree_freq > extreme_freq) or (not find_max and subtree_freq < extreme_freq):
                    extreme_freq = subtree_freq
                    extreme_path = [self.root] + subtree_path

            return extreme_freq, extreme_path

    # Specific Analysis Tools
    def top_rankings(self, beginning: int, end: int) -> dict[int, tuple[str, int]]:
        """Return a dictionary of the children of the root with the highest frequency within the given range.
        The dictionary key should be its numerical ranking mapped to a tuple of the node's root value and frequency.

        Preconditions:
            - 1 <= beginning <= end
            - end <= len(self.subtrees)

        >>> tree = Tree("Root", 0, [])
        >>> tree.insert_data(["Theft", "Day"], [0, 1])
        >>> tree.insert_data(["Theft", "Night"], [0, 1])
        >>> tree.insert_data(["Assault", "Day"], [0, 1])
        >>> tree.top_rankings(1, 2)
        {1: ('Theft', 2), 2: ('Assault', 1)}
        """

        sorted_subtrees = sorted(self.subtrees, key=lambda x: x.freq, reverse=True)
        selected_subtrees = sorted_subtrees[beginning - 1:end]
        return {i + beginning: (subtree.root, subtree.freq) for i, subtree in enumerate(selected_subtrees)}

    def top_specific(self, specific: str) -> tuple[str, dict[int, tuple[str, int]]]:
        """Return the name of the specific root and a dictionary of the top 5 children of the given specific input
        with the highest frequency. The dictionary key should be its numerical ranking mapped to a
        tuple of the node's root value and frequency.

        >>> tree = Tree("Root", 0, [])
        >>> tree.insert_data(["Theft", "Day"], [0, 1])
        >>> tree.insert_data(["Theft", "Night"], [0, 1])
        >>> tree.insert_data(["Assault", "Day"], [0, 1])
        >>> tree.top_specific("Theft")
        ('Theft', {1: ('Day', 1), 2: ('Night', 1)})
        >>> tree.top_specific("Nonexistent")
        ('', {})
        """

        specific_subtree = self.search_value_in_tree(specific)
        if specific_subtree is None:
            return '', {}
        specific_node = specific_subtree[1][-1]
        specific_tree = next((subtree for subtree in self.subtrees if subtree.root == specific_node), None)
        if specific_tree is None:
            return '', {}

        sorted_subtrees = sorted(specific_tree.subtrees, key=lambda x: x.freq, reverse=True)[:]
        return specific_node, {i + 1: (subtree.root, subtree.freq) for i, subtree in enumerate(sorted_subtrees)}

    def crime_time_shift(self, crime_category: str) -> tuple[str, int, int]:
        """Return a tuple containing the name of the root and the frequency of crime occurrences
        in the day and night for the given crime category.

        >>> tree = Tree("Root", 0, [])
        >>> tree.insert_data(["Day", "Theft"], [0, 1])
        >>> tree.insert_data(["Night", "Theft"], [0, 1])
        >>> tree.insert_data(["Day", "Assault"], [0, 1])
        >>> tree.crime_time_shift("Theft")
        ('Theft', 1, 1)
        >>> tree.crime_time_shift("Assault")
        ('Assault', 1, 0)
        >>> tree.crime_time_shift("Nonexistent")
        ('', 0, 0)
        """
        specific_subtree = self.search_value_in_tree(crime_category)
        if specific_subtree is None:
            return '', 0, 0
        specific_node = specific_subtree[1][-1]

        day_tree = next((subtree for subtree in self.subtrees if subtree.root.lower() == 'day'), None)
        night_tree = next((subtree for subtree in self.subtrees if subtree.root.lower() == 'night'), None)

        day_freq = 0
        night_freq = 0

        if day_tree is not None:
            crime_subtree = next((subtree for subtree in day_tree.subtrees if subtree.root == crime_category), None)
            if crime_subtree is not None:
                day_freq = crime_subtree.freq

        if night_tree is not None:
            crime_subtree = next((subtree for subtree in night_tree.subtrees if subtree.root == crime_category), None)
            if crime_subtree is not None:
                night_freq = crime_subtree.freq

        return specific_node, day_freq, night_freq

    def specific_ranked(self, specific: str) -> tuple[str, int, int]:
        """Return a tuple containing the name of root, rank, in terms of frequency,
        and numeric frequency of the given specific root value.

        >>> tree = Tree("Root", 0, [])
        >>> tree.insert_data(["Theft", "Day"], [0, 1])
        >>> tree.insert_data(["Theft", "Night"], [0, 1])
        >>> tree.insert_data(["Assault", "Day"], [0, 1])
        >>> tree.specific_ranked("Theft")
        ('Theft', 1, 2)
        >>> tree.specific_ranked("Assault")
        ('Assault', 2, 1)
        >>> tree.specific_ranked("Nonexistent")
        ('', 0, 0)
        """

        specific_subtree = self.search_value_in_tree(specific)
        if specific_subtree is None:
            return ('', 0, 0)
        name = specific_subtree[-1][-1]
        target_freq = specific_subtree[0]
        rank = 1
        for subtree in self.subtrees:
            if subtree.freq > target_freq:
                rank += 1

        return name, rank, target_freq

    # Graphviz Visualization
    def visualize(self) -> None:
        """Visualize the tree using Graphviz."""
        dot = graphviz.Digraph()
        self._add_nodes(dot)
        output_file = os.path.join('visualizations', 'tree_visualization')
        dot.render(output_file, format='svg', cleanup=False)

        # Cross-platform file opening
        if platform.system() == 'Windows':
            os.startfile(output_file + '.svg')
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', output_file + '.svg'])
        else:  # Linux and other systems
            subprocess.run(['xdg-open', output_file + '.svg'])

    def visualize_web(self) -> str:
        """Visualize the tree and return SVG data for web display."""
        dot = graphviz.Digraph()
        self._add_nodes(dot)
        
        # Return the SVG source directly
        return dot.pipe(format='svg').decode('utf-8')

    def _add_nodes(self, dot: graphviz.Digraph, parent_id: Optional[str] = None, level: int = 0) -> None:
        """Add nodes to the Graphviz Digraph for visualization.

        Preconditions:
            - level >= 0
        """
        node_id = str(id(self))
        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightgoldenrodyellow', 'lightpink',
                'lightgray', 'lightcyan']
        color = colors[level % len(colors)]
        label = f"{self.root} ({self.freq})"

        # Split the label into two lines if it's too long, only at spaces
        if len(label) > 20:
            split_index = label[:20].rfind(' ')
            if split_index != -1:
                label = label[:split_index] + '\n' + label[split_index + 1:]

        if level == 0:
            dot.node(node_id, label, shape='oval', style='filled', color=color, fontsize='100', fontname='Calibri',
                    width='30', height='10')
        else:
            # Scaled size for other nodes
            size = max(1.5, min(15, 4 + (self.freq / 100) * 11))  # Gradient scaling
            dot.node(node_id, label, shape='circle', style='filled', color=color, fontsize=str(size * 7.5),
                    fontname='Calibri', width=str(size / 100), height=str(size))
        if parent_id:
            dot.edge(parent_id, node_id, label='', fontsize='10', fontname='Calibri', color='black')

        for subtree in self.subtrees:
            subtree._add_nodes(dot, node_id, level + 1)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['graphviz', 'os'],  # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
