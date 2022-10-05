import sqlite3

# create sqlite db
connection = sqlite3.connect(r"C:\Users\frank\Desktop\Programming\Playlist Bot\song_db.db")
# get cursor to execute sql statements
cursor = connection.cursor()

#create table for db
sql = '''CREATE TABLE IF NOT EXISTS Song
            (PID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name text, Flag INTEGER DEFAULT 0)'''

cursor.execute(sql)

#select data in the table
# sql = 'SELECT Name, Flag FROM Song'
# cursor.execute(sql)

# rows = cursor.fetchall()
# song = "Dodo - AliKiba"
# for row in rows:    
#     cursor.execute("UPDATE Song SET Flag = 0 WHERE Name = (?)",(row[0],))
#     connection.commit()

# sql = 'SELECT Name, Flag FROM Song'
# cursor.execute(sql)

# rows = cursor.fetchall()
# for row in rows: 
#     print(row)


    


connection.close()