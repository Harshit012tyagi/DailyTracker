from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Path to store the uploaded Excel file
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
FILE_PATH = os.path.join(UPLOAD_FOLDER, "tracker.xlsx")

# Load data if file exists, otherwise initialize
if os.path.exists(FILE_PATH):
    data = pd.read_excel(FILE_PATH)
else:
    data = pd.DataFrame()  # Empty DataFrame

@app.route('/')
def index():
    """Homepage to display tracker data."""
    global data
    return render_template("index.html", tables=[data.to_html(classes='table table-bordered', index=False)],
                           title="Daily Tracker")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Route to handle Excel file upload."""
    global data
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request."
        file = request.files['file']
        if file.filename == '':
            return "No selected file."
        if file:
            file.save(FILE_PATH)
            data = pd.read_excel(FILE_PATH)
            return redirect(url_for('index'))
    return render_template("upload.html", title="Upload Tracker")

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    """Route to add a new daily entry."""
    global data
    if request.method == 'POST':
        # Get form data and append to the DataFrame
        form_data = {key: request.form[key] for key in request.form}
        new_entry = pd.DataFrame([form_data])
        data = pd.concat([data, new_entry], ignore_index=True)
        data.to_excel(FILE_PATH, index=False)
        return redirect(url_for('index'))
    # Render form for adding new entry
    return render_template("add.html", title="Add Daily Entry")

if __name__ == '__main__':
    app.run(debug=True)
