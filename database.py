import sqlite3

def db_create(path):
    try:
        sqliteConnection = sqlite3.connect(path)
        create_table_query = """CREATE TABLE Users (
                                id INTEGER PRIMARY KEY,
                                tg_id INTEGER NOT NULL UNIQUE,
                                full_name VARCHAR(100) NOT NULL,
                                username TEXT UNIQUE
                                );"""

        cursor = sqliteConnection.cursor()

        print("Successfully connection to SQLite")

        cursor.execute(create_table_query)
        sqliteConnection.commit()
        print("SQLite table Created successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The Sqlite connection is closed.")


def adv_table_create(path):
    try:
        sqliteConnection = sqlite3.connect(path)
        create_table_query = """CREATE TABLE Adv (
                                id INTEGER PRIMARY KEY,
                                tg_id INTEGER NOT NULL,
                                title VARCHAR(100) NOT NULL,
                                desc TEXT,
                                image VARCHAR(100) NOT NULL,
                                price REAL NOT NULL,
                                phone VARCHAR(20) NOT NULL
                                );"""

        cursor = sqliteConnection.cursor()

        print("Successfully connection to SQLite")

        cursor.execute(create_table_query)
        sqliteConnection.commit()
        print("SQLite table Created successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The Sqlite connection is closed.")



def insert_user(path, tg_id, full_name, username=None):
    try:
        sqliteConnection = sqlite3.connect(path)
        cursor = sqliteConnection.cursor()
        print("Successfully connection to SQLite")

        sql = """INSERT INTO Users (tg_id, full_name, username) 
        VALUES (?, ?, ?);"""
        # data_tuple = (first_name, last_name, email, course, balls)
        cursor.execute(sql, (tg_id, full_name, username))
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The Sqlite connection is closed.")


def insert_adv(path, tg_id, title, desc, image, price, phone):
    try:
        sqliteConnection = sqlite3.connect(path)
        cursor = sqliteConnection.cursor()
        print("Successfully connection to SQLite")

        sql = """INSERT INTO Adv (tg_id, title, desc, image, price, phone) 
        VALUES (?, ?, ?, ?, ?, ?);"""
        # data_tuple = (first_name, last_name, email, course, balls)
        cursor.execute(sql, (tg_id,  title, desc, image, price, phone))
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The Sqlite connection is closed.")
