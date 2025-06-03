# Toronto Crime Visualization

A command-line application for building, analyzing, and visualizing hierarchical crime trees from Toronto’s 2024 crime dataset!

## 📊 Project Overview

**Purpose**  
Toronto Crime Visualization lets you explore hierarchical patterns in Toronto’s crime data—by neighbourhood, offence category, premises type, time of day, or any custom hierarchy.

**Goal**  
Provide an interactive, data-driven CLI and Graphviz-based visualization tool to surface high-frequency crime trends and support ad-hoc analysis.

## 🖥️ How to Use

1. Clone the repo  

2. Install[`graphviz`](https://graphviz.org/download/)

3. Place CSV from [Toronto Open Data](https://open.toronto.ca/dataset/major-crime-indicators/) in the project root. Filtered 2024 Major Crime Indicators already placed in repo.  

4. Run the tool  

5. Follow the prompts  
• Choose a month  
• Pick a hierarchical analysis (or define your own)  
• View the cropped “high-frequency” tree in your browser  
• Use built-in analysis tools to search, rank, and compare

## ✨ Features

- **Full & Cropped Crime Trees**  
  • Builds a complete decision tree for the selected hierarchy  
  • Crops to top-N high-frequency categories at each level  

- **Graphviz Visualization**  
  • Renders an SVG (`visualizations/tree_visualization.svg`)  
  • Automatically opens the graph in your default viewer  

- **Interactive CLI Tools**  
  • Display the full tree in the console  
  • Search for a value and show its path & occurrence count  
  • Find most/least common crime paths  
  • Top-N rankings (neighbourhoods, offences, premises)  
  • Crime time-of-day shifts (day vs. night)  
  • Custom hierarchy selection (2–6 levels)

## 🔍 Data Columns

- OCC_DAY  
- OCC_DOW  
- OCC_HOUR  
- DIVISION  
- LOCATION_TYPE  
- PREMISES_TYPE  
- OFFENCE  
- MCI_CATEGORY  
- NEIGHBOURHOOD_158  

## 🛠️ Technical Details

- **Language**: Python 3.x  
- **Visualization**:[`graphviz`](https://graphviz.org/download/)Python package + Graphviz system install  
- **Modules**:  
  - `render_data.py` – build & crop crime trees  
  - `crime_tree.py` – `Tree` class with insertion, search, ranking, visualization  
  - `helper_functions.py` – CLI styling, input validation, typewriter effect  
  - `data_tools.py` – general & specific analysis menus  
  - `main.py` – user interaction loop  

- **Data Source**:  
  [Major Crime Indicators CSV from Toronto Open Data portal](https://open.toronto.ca/dataset/major-crime-indicators/)  
