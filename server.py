from flask import Flask, render_template_string, request
import json
import os

app = Flask(__name__)

# Define the folder containing the JSON files
JSON_FOLDER = './aiEdited/'

# HTML templates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"{{ filename }}"</title>
    <style>
        .list-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .list-item {
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
        .list-item a {
            text-decoration: none;
            color: blue;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>"{{ filename }}"</h1>
    <div class="list-container">
        {% for item in items %}
        <div class="list-item">
            <a href="{{ item.link }}" target="_blank">{{ item.name }}</a>
            <p>{{ item.description }}</p>
            <p>Price: {{ item.price }}</p>
            <p>{{ 'VB' if item.vb else '' }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

FILE_SELECTION_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Select a JSON File</title>
</head>
<body>
    <h1>Select a JSON File</h1>
    <form action="/display_items" method="post">
        <select name="filename">
            {% for file in files %}
            <option value="{{ file }}">{{ file }}</option>
            {% endfor %}
        </select>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

@app.route('/')
def select_file():
    # List all JSON files in the specified folder
    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith('.json')]
    return render_template_string(FILE_SELECTION_TEMPLATE, files=files)

@app.route('/display_items', methods=['POST'])
def display_items():
    filename = request.form['filename']
    json_file_path = os.path.join(JSON_FOLDER, filename)
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        items = data if isinstance(data, list) else [data]
    return render_template_string(HTML_TEMPLATE, items=items,filename=filename)

#@app.route('/')

if __name__ == '__main__':
    app.run(debug=True)
