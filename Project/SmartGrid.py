import struct

# 10K Trimpot connected to ADC #0
POTENTIOMETER_ADC = 0;

# SPI interface pins connected to ADC
SPI_CLK = 23
SPI_MISO = 21
SPI_MOSI = 19
SPI_CS = 24

# Setup GPIO using board numbering
GPIO.setmode(GPIO.BOARD)

# Set up the SPI interface pins
GPIO.setup(SPI_MOSI, GPIO.OUT)
GPIO.setup(SPI_MISO, GPIO.IN)
GPIO.setup(SPI_CLK, GPIO.OUT)
GPIO.setup(SPI_CS, GPIO.OUT)

class SmartGrid(object):

        def __init__(self):

                adc = MCP3008Controller()
                gps = GPSController()
                client = ClientUDP()

        def control


while True:
        report = session.next()
        # Read the analog pin
        trimpot = readAdc(POTENTIOMETER_ADC, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)

        # Wait for a "TPV" report and display the current time
        if report["class"] == "TPV":
                if hasattr(report, "time"):                        
                        
                        values = (str(report.time), trimpot)
                        s = struct.Struct("24s I") # 1 byte per character = 24 bytes
                        packedData = s.pack(*values)

                        # Send data
                        print "Sending ", packedData
                        sent = sock.sendto(packedData, serverAddress)
