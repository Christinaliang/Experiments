import usb, sys, time, argparse, struct, socket, binascii, Queue
from threading import Thread

class hokuyoDataReader():
	def __init__(self):
		pass
	
	def readData(self):
		# don't forget: netsh interface ip set address "Local Area Connection" static 192.168.0.5   then ipconfig/renew to check
		global nhokreadings
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(2.0)
		s.connect(("192.168.0.10", 10940))
		s.send('PP\n')
		s.send('MS'+'0000'+'1080'+'01'+'0'+'01\n')
		res = [ ]
		for i in range(100):
			lres = s.recv(100).split("\n")
			rectime = time.clock()
			lres.reverse()
			#pres.append(lres.pop())
			while lres:
				# if not sres:
					# nhokreadings += 1
				#print ("HOK", rectime, len(sres))
				scan = lres.pop()
				print scan
				# print '==============='
				#res = [ lres.pop() ]
			# print res
			# should turn it off
	
	##
	# decodeChars
	#
	# Decodes a 2- or 3-character datapoint from the lidar.
	#	TODO: find out if there is a pre-built solution
	#	TODO: make this work
	#
	# Perameters:
	#	data - a string containing the 2- or 3- character code
	#
	# Returns:
	#	an integer result representing the datapoint
	##
	# def decodeChars(self, data):
		# result = 0
		# i = 0
		# datalist = list(data)
		# #datalist.reverse()
		# for char in datalist:
			# char = ord(char) - 0x30
			# result = char*64^(i)
			# i += 1
		# return result
			
			
#Unit testing
lidar = hokuyoDataReader()
lidar.readData()
#print lidar.decode("00P")