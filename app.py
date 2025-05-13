from flask import Flask, redirect, render_template, request
import random
import string
import sqlite3

app = Flask(__name__)

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def get_db_connection():
    conn = sqlite3.connect('urls.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('url')
        short_url = generate_short_url()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO urls (short_url, original_url) VALUES (?, ?)', (short_url, original_url))
        conn.commit()
        conn.close()

        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return redirect(row['original_url'])
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
