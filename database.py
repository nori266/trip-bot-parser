import sqlite3


def createDB(dbName: str):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    create_query = 'CREATE TABLE trips(id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                      'message_id STRING NOT NULL, ' \
                        'message STRING NOT NULL, ' \
                        'message_date STRING, ' \
                        'trip_date STRING, ' \
                        'to_russia BOOLEAN, ' \
                        'to_finland BOOLEAN, ' \
                        'is_driver BOOLEAN)'

    try:
        c.execute(create_query)
    except sqlite3.OperationalError:
        c.execute('DROP TABLE trips')
        c.execute(create_query)


def getDBconn(dbName: str):
    conn = sqlite3.connect(dbName)
    return conn


def insert_message(dbCursor, message, trip_date, to_russia, to_finland, is_driver):
    dbCursor.execute("SELECT id FROM trips WHERE message_id = ?", [message.id])
    if dbCursor.fetchone() is None:
        dbCursor.execute(
            "INSERT INTO trips (message_id, message, message_date, trip_date, to_russia, to_finland, is_driver) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                message.id,
                message.message,
                message.date,
                trip_date,
                to_russia,
                to_finland,
                is_driver
            ])
    else:
        print("Message already in database")
