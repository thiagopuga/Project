from boto3.session import Session

session = Session(aws_access_key_id='AKIAI5BIAF4DH342LPBQ',
                  aws_secret_access_key='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',
                  region_name='us-west-2')

ec2 = session.resource('ec2')
ec2_us_west_2 = session.resource('ec2', region_name='us-west-2')

# List all of my EC2 instances in my default region.
print('Default region:')
for instance in ec2.instances.all():
    print(instance.id)

# List all of my EC2 instances in us-west-2.
print('US West 2 region:')
for instance in ec2_us_west_2.instances.all():
    print(instance.id)



##import MySQLdb
##import sys
##
##try:
##    con = MySQLdb.connect(
##        'ec2-user@ec2-52-27-186-72.us-west-2.compute.amazonaws.com',
##        'pi', 'raspberry', 'pi');    
##    cur = con.cursor()
##    
##    #sql = "insert into data(RaspID, time) values(2, 113255000)"
##    #print sql
##    cur.execute("SHOW DATABASES")
##    #print "Rows inserted: %s" % cur.rowcount
##    #con.commit()
##
##except:
##    print "Error opening database."
##    sys.exit(1)
