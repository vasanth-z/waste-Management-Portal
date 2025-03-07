import mysql.connector
db=mysql.connector.connect(
    host="localhost",
    user="kec",
    password="1234",
    databasename="kecproject"
    )
my_cursor=conn.cursor()
conn.commit()
conn.close()

print('connected:',db)