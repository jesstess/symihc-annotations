import sqlite3

connection = sqlite3.connect('stuff.db')
cursor = connection.cursor()

for tag in ("African Americans", "LGBTQ"):
    cursor.execute("""INSERT INTO tag VALUES (?)""", (tag,))

print "Saving..."
connection.commit()
connection.close()
print "Done."
