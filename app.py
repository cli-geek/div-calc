import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, g
from werkzeug.utils import secure_filename
import sqlite3
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'csv'} # change to csv later
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
SECRET_KEY = 'supersecretkey123'
DATABASE = 'info.db'

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = True

def isExists(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('SELECT 1 FROM files WHERE id = ?', (id,))
    result = c.fetchone()

    if result:
        return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            file_size INT NOT NULL,
            time TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.close()

init_db()

#@app.route('/')
#def index():
#    return render_template('upload.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # if no file selected, submit an empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f'Filepath is: {filepath}')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # before we return, we need to add some information to the db
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('INSERT INTO files (name, file_size) VALUES (?, ?)', (filename, os.path.getsize(filepath)))
            
            conn.commit()

            conn.close() 

            return redirect(url_for('upload_file'))
        
    # for get request
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    files = c.execute('SELECT * FROM files ORDER BY time DESC').fetchall()
    conn.close()

    return render_template('upload.html', files=files)
    
@app.route('/uploads/<name>')
def download_file(name):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], name)
    except FileNotFoundError as e:
        print("Not found")

@app.route('/delete/<int:id>', methods=['POST'])
def delete_file(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('SELECT name FROM files WHERE id = ?', (id,))
    result = c.fetchone()

    if result:
        filename = result[0]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        c.execute('DELETE FROM files WHERE id = ?', (id,))
        conn.commit()

        try:
            os.remove(filepath)
        except OSError as e:
            pass

    conn.close()

    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run()