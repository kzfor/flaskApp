import sqlite3

# Инициализация данных в БД
conn = sqlite3.connect('data.db')
try:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client (
        id INTEGER PRIMARY KEY,
        phone TEXT,
        first_name TEXT,
        last_name TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS address (
        id INTEGER PRIMARY KEY,
        address TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_addresses (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        address_id INTEGER,
        FOREIGN KEY (client_id) 
            REFERENCES client (id) 
                ON DELETE CASCADE 
                ON UPDATE NO ACTION,
        FOREIGN KEY (address_id) 
            REFERENCES address (id) 
                ON DELETE CASCADE 
                ON UPDATE NO ACTION
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contract (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        address_id INTEGER,
        date TEXT,
        status TEXT,
        description TEXT,
        document TEXT,
        sum INTEGER,
        FOREIGN KEY (client_id) 
            REFERENCES client (id) 
                ON DELETE CASCADE 
                ON UPDATE NO ACTION,
        FOREIGN KEY (address_id) 
            REFERENCES address (id) 
                ON DELETE CASCADE 
                ON UPDATE NO ACTION
    );
    """)
except Exception as e:
    print("Ошибка инициализации БД: " + str(e))
finally:
    conn.close()
