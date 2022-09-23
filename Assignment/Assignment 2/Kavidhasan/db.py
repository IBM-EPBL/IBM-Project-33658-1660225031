import sqlite3
conn = sqlite3.connect('users.db')
conn.execute('''create table user( 
email varchar(100),
username varchar(100),
roll_number int PRIMARY KEY,
password varchar(100)
);''')
conn.close()