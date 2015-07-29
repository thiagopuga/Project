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
    
##cur.execute('drop table INFO')
##
##cur.execute('create table INFO (ID varchar(2), Date varchar(8), Time varchar(9), Latitude varchar(9), Longitude varchar(9), ADC int(4))')
##con.commit()

##insertCmd = ('insert into INFO (ID, Date, Time, Longitude, Latitude, ADC)'
##             'values (%s, %s, %s, %s, %s, %s)')
##
##data = ('2', '07292015', '112355000', '200122', '12090890', '1023')
##
##cur.execute(insertCmd, data)
##
##con.commit()

cur.execute('select * from INFO')
print cur.fetchall()

con.close()


