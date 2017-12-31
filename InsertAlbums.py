import csv
import MySQLdb

INPUT_FILE = "albums\\artistsAlbumsMusicgraph.csv"
SERVER_NAME = "localhost"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_NAME = "test"

def getForeignKeyFromTable(query, value):
    # execute the SQL query using execute() method.
    cursor.execute(query, [value])
    # fetch all of the rows from the query
    data = cursor.fetchall()
    if (data== ()):     # not found
        return None
    else:
        return data[0][0]   

# Open database connection
db = MySQLdb.connect(SERVER_NAME,DB_USERNAME,DB_PASSWORD,DB_NAME)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# to prevent encoding problems
db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

# Inserting...
x = 0
with open(INPUT_FILE, 'r') as fin:
    reader = csv.reader(fin, lineterminator='\n')

    for row in reader:
        x = x+1
        print(x)

        # csv row info
        artist_name = row[1]
        album_title = row[3]
        album_year = row[4]
        num_of_tracks = row[6]
        

        # define sql queries
        add_album = """INSERT INTO album (album_id, title, artist_id, release_year, num_of_tracks)
                        VALUES (%s,%s,%s,%s,%s)"""
        get_artist_id = "SELECT artist_id from artist WHERE name = %s"

        # getting the foreign keys from artist table
        artist_id = getForeignKeyFromTable(get_artist_id, artist_name)

        # inserting the album
        try:
            # inserting 0 for artist_id to use sql auto increment
            cursor.execute(add_album, (0,album_title,artist_id,album_year,num_of_tracks))
            db.commit()
        except Exception as e:
            print("error")
            print(e)
            db.rollback()
            break;


# disconnect from server
db.close()

