import datetime

START_TIME = 215500000000
END_TIME = 220000000000

fileName = ""

time = datetime.datetime.utcnow().strftime('%H%M%S%f')

while int(time) < START_TIME:
        time = datetime.datetime.utcnow().strftime('%H%M%S%f')
        
while int(time) <= END_TIME:
        resp = datetime.datetime.utcnow().strftime('%m-%d-%Y,%H%M%S%f')        
        data = resp.split(',')
        date = data[0]
        time = data[1]
        print time
        # Create a log file    
        if date != fileName:
                if fileName != "":
                        file.close()                           
                fileName = date
                file = open(fileName + ".log", 'a')
        # Write on log
        file.write(time + "\n")
