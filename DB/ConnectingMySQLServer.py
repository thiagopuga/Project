import MySQLdb
import sys

try:
    con = MySQLdb.connect(host='mydbinstance.cmkub5asq0w1.us-west-2.rds.amazonaws.com',
                          port=3306,
                          user='awsuser',
                          passwd='MyDatabase',
                          db='SPI');
    cur = con.cursor()

except:
    print "error opening database"
    sys.exit(1)


##cur.execute('DELETE FROM INFO WHERE ID = 1')
##cur.execute('DELETE FROM INFO WHERE ID = 2')

##cur.execute('DROP TABLE INFO')

# serial libray
##cur.execute('CREATE TABLE INFO(ID VARCHAR(2), Reference VARCHAR(3), Date VARCHAR(8), Time VARCHAR(9),'
##            'Latitude VARCHAR(10), Hemisphere VARCHAR(1), Longitude VARCHAR(10), Side VARCHAR(1), ADC INT(4))')

# gps libray
##cur.execute('CREATE TABLE INFO(ID VARCHAR(2), Date VARCHAR(8), Time VARCHAR(9),'
##            'Latitude VARCHAR(11), Longitude VARCHAR(11), ADC INT(4))')

##cur.execute('INSERT INTO INFO(ID, Date, Time, Latitude, Longitude, ADC)'
##            'VALUES(3, 07292015, 112355000, 200122, 12090890, 1023)')

cur.execute('SELECT ID, Time FROM INFO')
print cur.fetchall()

con.commit() # Apply changes
con.close()



