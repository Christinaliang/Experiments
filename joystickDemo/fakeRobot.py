import socket

tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSock.bind(('', 6000))
tcpSock.listen(1)
# tcpSock.settimeout(3)
conn = tcpSock.accept()
sock = conn[0]

while True:
    try:
        received = bytearray(sock.recv(10))

        leftSpeed = (50-received[2])
        rightSpeed = (50-received[0])*-1

        print str(leftSpeed) + " " + str(rightSpeed)
    except socket.error:
        continue