from flask import Flask, request, jsonify, g, render_template
import sqlite3
from sqlite3 import Error
import os

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'votes.db')

def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    return connection

def get_connection():
    if 'connection' not in g:
        g.connection = create_connection()
    return g.connection

@app.teardown_appcontext
def close_connection(exception=None):
    connection = g.pop('connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    vote_option = request.form['vote']
    
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('SELECT * FROM votes WHERE option=?', (vote_option,))
        row = cursor.fetchone()
        if row:
            new_count = row[2] + 1
            cursor.execute('UPDATE votes SET count=? WHERE option=?', (new_count, vote_option))
        else:
            cursor.execute('INSERT INTO votes (option, count) VALUES (?, 1)', (vote_option,))
        
        connection.commit()
        
        return jsonify({'message': 'Vote cast successfully'})
    except Error as e:
        print(e)
        return jsonify({'error': 'An error occurred while processing the vote'}), 500

@app.route('/results')
def results():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('SELECT * FROM votes')
        rows = cursor.fetchall()
        results = {row[1]: row[2] for row in rows}  # Assuming column 1 is 'option' and column 2 is 'count'
        
        return jsonify({'results': results})
    except Error as e:
        print(e)
        return jsonify({'error': 'An error occurred while fetching the results'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
