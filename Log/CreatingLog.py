
LOG_FILENAME = "example.log"

log = open(LOG_FILENAME, 'w')

log.write("This message should go to the log file.")
log.close()
