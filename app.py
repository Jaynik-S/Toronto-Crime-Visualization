from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import io
import base64
from crime_tree import Tree
import render_data as rd
from helper_functions import get_custom_tree_columns
from data_tools import data_analysis_tools, general_analysis_tools, specific_analysis_tools

app = Flask(__name__)
app.secret_key = 'crime_visualization_secret_key'  # For session management

@app.route('/')
def index():
    """Render the main page of the application."""
    months = ["january", "february", "march", "april", "may", "june", "july", 
              "august", "september", "october", "november", "december"]
    return render_template('index.html', months=months)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle the analysis selection and create tree visualization."""
    # Get the month from the form
    month = request.form['month'].lower().strip()
    choice = int(request.form['hierarchy'])
    
    # Store in session for later use
    session['month'] = month
    session['choice'] = choice
    
    # Define the analysis options
    analysis_options = {
        1: ['NEIGHBOURHOOD_158', 'MCI_CATEGORY', 'PREMISES_TYPE'],
        2: ['OCC_HOUR', 'MCI_CATEGORY', 'NEIGHBOURHOOD_158'],
        3: ['MCI_CATEGORY', 'NEIGHBOURHOOD_158', 'PREMISES_TYPE'],
        4: ['PREMISES_TYPE', 'MCI_CATEGORY', 'NEIGHBOURHOOD_158']
    }
    
    if choice in analysis_options:
        columns = analysis_options[choice]
    else:
        # For custom option, we'll need to implement a separate route
        return redirect(url_for('custom_columns'))
    
    session['columns'] = columns
    
    # Build the tree
    full_tree, cropped_tree = rd.build_crime_tree(month, columns)
    
    # Get visualization SVG
    svg_data = cropped_tree.visualize_web()
    
    return render_template('visualization.html', 
                          month=month.title(),
                          svg_data=svg_data,
                          choice=choice)

@app.route('/custom_columns', methods=['GET', 'POST'])
def custom_columns():
    """Handle custom column selection."""
    if request.method == 'POST':
        # Process custom columns
        # This is a simplified version - you would need to adapt get_custom_tree_columns
        columns = [
            request.form.get('column1'),
            request.form.get('column2'),
            request.form.get('column3')
        ]
        session['columns'] = columns
        month = session.get('month')
        
        full_tree, cropped_tree = rd.build_crime_tree(month, columns)
        svg_data = cropped_tree.visualize_web()
        
        return render_template('visualization.html', 
                              month=month.title(), 
                              svg_data=svg_data,
                              choice=5)  # 5 for custom
    
    # Display custom column selection form
    return render_template('custom_columns.html')

@app.route('/analysis_tools')
def analysis_tools():
    """Display analysis tools options."""
    choice = session.get('choice')
    month = session.get('month')
    columns = session.get('columns')
    
    return render_template('analysis_tools.html', 
                          choice=choice,
                          month=month.title())

@app.route('/general_analysis', methods=['GET', 'POST'])
def general_analysis():
    """Handle general analysis tools."""
    columns = session.get('columns')
    month = session.get('month')
    
    full_tree, _ = rd.build_crime_tree(month, columns)
    
    if request.method == 'POST':
        action = request.form.get('action')
        result = {}
        
        if action == '1':  # Display Full Tree
            result['tree'] = full_tree.__str__()
            return jsonify(result)
        
        elif action == '2':  # Search for Value
            value = request.form.get('search_value')
            search_result = full_tree.search_value_in_tree(value)
            if search_result:
                occurrences, path = search_result
                result['found'] = True
                result['occurrences'] = occurrences
                result['path'] = ' --> '.join(path)
            else:
                result['found'] = False
            return jsonify(result)
            
        elif action == '3':  # Most Common Crime
            occurrences, path = full_tree.find_most_common_crime()
            result['path'] = ' --> '.join(path)
            result['occurrences'] = occurrences
            return jsonify(result)
            
        elif action == '4':  # Least Common Crime
            occurrences, path = full_tree.find_least_common_crime()
            result['path'] = ' --> '.join(path)
            result['occurrences'] = occurrences
            return jsonify(result)
    
    return render_template('general_analysis.html')

@app.route('/specific_analysis', methods=['GET', 'POST'])
def specific_analysis():
    """Handle specific analysis tools."""
    columns = session.get('columns')
    month = session.get('month')
    choice = session.get('choice')
    
    full_tree, _ = rd.build_crime_tree(month, columns)
    
    if request.method == 'POST':
        action = request.form.get('action')
        result = {}
        
        # Logic depends on the tree type (choice) and selected action
        # This is a simplified version that needs to be expanded
        if choice == 1:  # Neighbourhood-based
            if action == '1':  # Top Crime Neighbourhoods
                rankings = full_tree.top_rankings(1, 10)
                result['rankings'] = rankings
            elif action == '2':  # Top Crimes in Specific Neighbourhood
                neighbourhood = request.form.get('specific_value')
                name, rankings = full_tree.top_specific(neighbourhood)
                result['name'] = name
                result['rankings'] = rankings
            elif action == '3':  # Neighbourhood Crime Rank
                neighbourhood = request.form.get('specific_value')
                name, rank, frequency = full_tree.specific_ranked(neighbourhood)
                result['name'] = name
                result['rank'] = rank
                result['frequency'] = frequency
        
        # Add similar logic for other choices (2, 3, 4)
        
        return jsonify(result)
    
    return render_template('specific_analysis.html', choice=choice)

if __name__ == '__main__':
    app.run(debug=True)
