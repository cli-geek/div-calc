import sqlite3

def set_cursor():
    conn = sqlite3.connect('info.db')
    return conn.cursor()

def init_db():
    c = set_cursor()


    # create the DB to store the file names and metadata
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            file_size INT NOT NULL,
            time TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # create the DB to store actual CSV data
    c.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY,
            run_date DATE,
            account TEXT,
            ticker TEXT,
            name TEXT,
            amount TEXT
        );
    ''')

    c.close()

if __name__ == '__main__':
    init_db()
   # c = set_cursor()

   # c.execute("SELECT name FROM sqlite_master WHERE type='table'")
   # table = c.fetchall()
   # print(table)
   # c.close()