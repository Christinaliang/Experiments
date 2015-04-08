__author__ = 'Matt'


from UI.data import data
import socket

#cPicke is faster
try:
   import cPickle as pickle
except:
   import pickle


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
s.connect(server_address)

data_string = s.recv(1024)
d = pickle.loads(data_string)

print d.frontLeftWheel.theta




