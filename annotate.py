import sqlite3
import calendar
from dateutil import parser
import feedparser

feed_url = "http://www.howstuffworks.com/podcasts/stuff-you-missed-in-history-class.rss"
data = feedparser.parse(feed_url)

connection = sqlite3.connect('stuff.db')
cursor = connection.cursor()

def set_gender(cursor, row_data):
    # Only prompt for unset gender info.
    if row_data["on_individual"] is not None:
        return

    name = row_data["name"]
    print name
    print row_data["description"]

    while True:
        on_individual = raw_input("Is this about an individual? (y/n) ")
        if on_individual.lower() in ("y", "n"):
            break

    if on_individual == "y":
        # On an individual, get the gender.
        while True:
            gender = raw_input("What is the gender of this individual? (m/f) ")
            if gender.lower() in ("m", "f"):
                cursor.execute("""UPDATE podcast
                                  SET on_individual=1, individual_gender=?
                                  WHERE name=?""", (gender, name))
                break
    else:
        cursor.execute("UPDATE podcast SET on_individual=0 WHERE name=?",
                       (name,))
    print ""
    connection.commit()

try:
    for entry in data.entries:
        name = entry.title
        cursor.execute("SELECT * FROM podcast WHERE name=?", (name,))
        result = cursor.fetchall()

        if not result[0][0]:
            # This is a new entry, insert the basics before doing anything else.
            pub_string = parser.parse(entry["published"])
            pub_date = calendar.timegm(pub_string.utctimetuple())
            description = entry.summary
            link = entry.link
            cursor.execute(""""INSERT INTO podcast(pub_date, name, description, link)
                               VALUES (?, ?, ?, ?)""", pub_date, name, description, link)

        columns = [column[0] for column in cursor.description]
        row_data = dict(zip(columns, result[0]))
        set_gender(cursor, row_data)

except KeyboardInterrupt:
    pass

print "Saving..."
connection.commit()
connection.close()
print "Done."
