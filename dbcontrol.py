import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

c.execute("DELETE FROM estimator")

c.execute("SELECT * FROM users")

c.close()