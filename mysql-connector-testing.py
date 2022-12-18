import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "kamae123",
    database = "testDB"
)

mycursor = db.cursor()

mycursor.execute("CREATE TABLE APITest (name VARCHAR(20), likes INT, views INT, video_key INT PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", ("Emily", 19))
#mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", ("Tom", 20))
#db.commit()

