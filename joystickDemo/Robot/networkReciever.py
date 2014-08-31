__author__ = 'matt'


import socket
import struct

class networkReciever:

    IP = "10.2.0.1"

    # UDP_IP = "224.0.0.1"
    # UDP_PORT = 6000

    def openClientSocket(self):

        tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpSock.bind(('', 6000))
        tcpSock.listen(1)
        # tcpSock.settimeout(3)
        conn = tcpSock.accept()
        self.sock = conn[0]
        # self.sock = tcpSock.accept()


        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_TCP)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.bind(('', self.UDP_PORT))
        #
        # mreq = struct.pack("=4sl", socket.inet_aton(self.UDP_IP), socket.INADDR_ANY)
        #
        # sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        #
        # sock.setblocking(False)
        # sock.settimeout(0.01)

        # self.sock = tcpSock

    # sock = openSocket()

    def getData(self):
        received = None

        try:
            received = bytearray(self.sock.recv(7))
        except:
            return None

        return received