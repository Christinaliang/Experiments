__author__ = 'Matt'

from UI.data import data
import socket

#cPicke is faster
try:
   import cPickle as pickle
except:
   import pickle

d = data()

# wait for the client to connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
s.bind(server_address)
s.listen(1)
(clientsocket, address) = s.accept()

i = 0
# send data
while i < 10:

    data_string = pickle.dumps(d)

    clientsocket.send(data_string)

