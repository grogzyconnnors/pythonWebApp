import sqlite3

db = sqlite3.connect('imageApp.db')
cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username VARCHAR(20) unique not null,
            password VARCHAR(100),
            name VARCHAR (20),
            surname VARCHAR(20)
            )
            ''')


cur.execute('''CREATE TABLE IF NOT EXISTS images(
            file_name VARCHAR(20) unique not null,
            username VARCHAR(20),
            date VARCHAR (20),
            time VARCHAR(20)
            )
            ''')


#cur.execute('''DELETE FROM	images WHERE	username="micksy"''')


db.commit()



