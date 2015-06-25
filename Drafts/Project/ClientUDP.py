import socket

class ClientUDP(object):

    def __init__(self):
        
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverAddress = ("169.254.0.1", 10000)

    def sendData(self, message):
        
        try:            
            # Send data
            print "Sending ", message
            sent = self.sock.sendto(message, serverAddress)

        finally:
            print "Closing socket"
            self.sock.close()
