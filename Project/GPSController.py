import gps

class GPSController(object):

    def __init__(self):
        
        # Listen on port 2947 (gpsd) of localhost
        session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    def getTime(self):

        while True:
            try:
                report = self.session.next()
                # Wait for a "TPV" report and display the current time
                # To see all report data, uncomment the line below
                # print report
                if report["class"] == "TPV":
                    if hasattr(report, "time"):
                        print report.time
            except KeyError:
                pass
            except StopIteration:
                self.session = None
                print "GPSD has terminated"
