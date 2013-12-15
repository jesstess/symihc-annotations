import sqlite3

connection = sqlite3.connect('stuff.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE podcast
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  pub_date INTEGER, name TEXT, description TEXT, link TEXT,
                  on_individual INTEGER, individual_gender TEXT, location TEXT,
                  start_time INTEGER, end_time INTEGER)""")

cursor.execute("""CREATE TABLE host
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,
                  gender TEXT)""")

cursor.execute("""CREATE TABLE podcast_host
                  (podcast_id INTEGER NOT NULL, host_id INTEGER NOT NULL,
                  PRIMARY KEY (podcast_id, host_id))""")

cursor.execute("""CREATE TABLE tag
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)""")

cursor.execute("""CREATE TABLE podcast_tag
                  (podcast_id INTEGER NOT NULL, tag_id INTEGER NOT NULL,
                  PRIMARY KEY (podcast_id, tag_id))""")

connection.commit()
connection.close()
