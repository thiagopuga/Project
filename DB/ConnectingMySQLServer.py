import MySQLdb
import sys

try:
    con = MySQLdb.connect(
        'ec2-user@ec2-52-27-186-72.us-west-2.compute.amazonaws.com',
        'root', 'raspberry', 'pi');
    cur = con.cursor()
    
    #sql = "insert into data(RaspID, time) values(2, 113255000)"
    #print sql
    cur.execute("SHOW DATABASES")
    #print "Rows inserted: %s" % cur.rowcount
    #con.commit()

except:
    print "Error opening database."
    sys.exit(1)
