import MySQLdb
import sys

db = MySQLdb.connect(host="mydbinstance.c6s134ojrjk4.us-west-2.rds.amazonaws.com",
                     port=3306,
                     user="awsuser",
                     passwd="MyDatabase",
                     db="SPI")

cursor = db.cursor()
# cursor.execute("SELECT voltage, current FROM measurements")
# # print("BEGIN Test")
# # #print(cursor.execute("SELECT name FROM student WHERE name='%s'"))
# # for row in cursor.fetchall():
# #     print(row[0])
# # print("END Test")
#
# print("DB:MEASUREMENTS")
# row=cursor.fetchall()
# print(row[0])
# # print(row[1])
# # print(row[2])
# print("END")

cursor.execute("SELECT hardware, longitude, latitude, ID FROM info")
print("DB:INFO ")
row=cursor.fetchall()
print(row[0])
print("END")


# INSERT SRCIPT
print("DB:info INSERT")
insert_stmt = (
  "INSERT INTO info (hardware, longitude, latitude) "
  "VALUES (%s, %s, %s)"
)
data = ('ARDU', '20.0122', '120.90890')
cursor.execute(insert_stmt, data)
# cursor.execute("""INSERT INTO info VALUES (%s,%s,%s)""",('ARDU','30.001','120.002'))
print("END")
# END OF INSERT SCRIPT


cursor.execute("""SELECT * FROM info;""")
print(cursor.fetchall())

cursor.close()
db.commit()
db.close()
sys.exit()
