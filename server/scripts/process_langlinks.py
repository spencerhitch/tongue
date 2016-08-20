import sqlite3
with open("../data/enwiki-20160801-langlinks.sql", 'rb') as db:
    db = db.read()
    print(db[0:1000])


#    connection = sqlite3.connect(db)
#    cursor = connection.cursor()
#    cursor.execute("SELECT table_name FROM all_tables")
#    print("fetchall:")
#    result = cursor.fetchall()
