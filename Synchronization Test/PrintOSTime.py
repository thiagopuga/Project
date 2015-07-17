import datetime

while True:
    time = datetime.datetime.utcnow().strftime('%H:%M:%S.%f')
    print time
