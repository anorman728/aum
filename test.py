import sqlite3

db = sqlite3.connect('./testdatabase.db')

cursor = db.cursor()

qry = 'CREATE TABLE IF NOT EXISTS testtable(id INTEGER PRIMARY KEY AUTOINCREMENT, testval TEXT)'
cursor.execute(qry)

qry = 'INSERT INTO testtable(testval) VALUES("testvalue5")'
cursor.execute(qry)

db.commit()

qry = 'SELECT * FROM testtable'
cursor.execute(qry)
allRows = cursor.fetchall()
for row in allRows:
    print(row)


db.close()
