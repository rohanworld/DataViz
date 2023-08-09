from flask import Flask, render_template, request, redirect, url_for
from pandas_profiling import ProfileReport
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            if file.filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
                df = pd.read_excel(file_path, engine='openpyxl')

            profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)
            profile_html = profile.to_html()

            return render_template('index.html', profile_html=profile_html, uploaded=True)

    return render_template('index.html', uploaded=False)

if __name__ == '__main__':
    app.run(debug=True)
