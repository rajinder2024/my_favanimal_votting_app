import sqlite3
from sqlite3 import Error

def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('votes.db')
        print("SQLite database connection established.")
    except Error as e:
        print(e)
    return connection

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY,
                option TEXT,
                count INTEGER
            )
        ''')
        connection.commit()
        print("Table 'votes' created successfully.")
    except Error as e:
        print(e)

def main():
    connection = create_connection()
    if connection is not None:
        create_table(connection)
        connection.close()
    else:
        print("Unable to establish database connection.")

if __name__ == '__main__':
    main()
