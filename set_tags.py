import sqlite3

# Assign tags to podcasts. The tags must already exist. To create new tags, run
# tags.py.

def african_american_podcasts(cursor, tag_id):
    # These are new candidate podcasts about African Americans which don't already
    # have the tag set.
    cursor.execute("""SELECT p.id, p.name, p.description
                      FROM podcast p
                      WHERE (p.description LIKE '%African%'
                      OR p.description LIKE '%Black%'
                      OR p.name like '%Audre Lorde%'
                      OR p.name like '%Benjamin Banneker%'
                      OR p.name like '%Loving v. Virginia%'
                      OR p.name like '%Underground Railroad%'
                      OR p.name like '%Escape to Freedom%'
                      OR p.name like '%Stono Rebellion%'
                      OR p.name like '%Mary-Elizabeth Bowser%')
                      AND p.name NOT LIKE '%Black death%'
                      AND p.name NOT LIKE '%African diamond trade%'
                      AND p.description NOT LIKE '%Blackbeard%'
                      AND p.description NOT LIKE '%Black Sam%'
                      AND p.description NOT LIKE '%Black Diaries%'
                      AND p.description NOT LIKE '%African elephant%'
                      AND p.description NOT LIKE '%Hollywood Blacklist%'
                      AND p.description NOT LIKE '%Black Hills%'
                      AND p.id NOT IN
                          (SELECT pt.podcast_id
                           FROM podcast_tag pt, tag t
                           WHERE pt.tag_id=t.id and t.id=?)""", (tag_id,))
    return cursor.fetchall()

def lgbtq_podcasts(cursor, tag_id):
    cursor.execute("""SELECT p.id, p.name, p.description
                      FROM podcast p
                      WHERE (p.description LIKE '%lesbian%'
                      OR p.description LIKE '%homosexual%'
                      OR p.description LIKE '%gay%'
                      OR p.description LIKE '%lgbt%'
                      OR p.description LIKE '%queer%'
                      OR p.description LIKE '%bisexual%'
                      OR p.description LIKE '%trans%gender%'
                      OR p.name LIKE '%Audre Lorde%'
                      OR p.name LIKE '%Jane Addams%')
                      AND p.id NOT IN
                          (SELECT pt.podcast_id
                           FROM podcast_tag pt, tag t
                           WHERE pt.tag_id=t.id and t.id=?)""", (tag_id,))
    return cursor.fetchall()

connection = sqlite3.connect('stuff.db')
cursor = connection.cursor()

tag_queries = {
    "African Americans": african_american_podcasts,
    "LGBTQ": lgbtq_podcasts,
}

# Set `African Americans` tag.
cursor.execute("""SELECT id, name FROM tag""")
tags = cursor.fetchall()

for tag_id, tag_name in tags:
    tag_query = tag_queries.get(tag_name)
    if not tag_query:
        print "No query for tag %s, skipping." % (tag_name,)
        continue

    candidate_podcasts = tag_query(cursor, tag_id)
    print "These are the new candidate podcasts for the `%s` tag:\n" % (tag_name,)

    for _, name, description in candidate_podcasts:
        print name
        print description
        print ""

    set_tags = raw_input("Are these podcasts correct for this tag? (y/n) ")
    if set_tags == "y":
        statement = "INSERT INTO podcast_tag VALUES (?, ?)"
        pairs = [(podcast_id, tag_id) for podcast_id, _, _ in candidate_podcasts]
        cursor.executemany(statement, tuple(pairs))

        print "Saving..."
        connection.commit()
        print "Done."
    else:
        print "Not saving for tag `%s`." % (tag_name,)

connection.close()
