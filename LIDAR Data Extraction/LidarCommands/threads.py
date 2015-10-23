
__author__="Jaimiey Sears"
__copyright__="October 22, 2015"
__version__= 0.10

import Queue, threading, usb, sys, time, argparse, struct, socket, binascii

#######################
## UNIT TEST 1 START ##
#######################
def main():
	lt = LidarThreads()

	lt.debugPrint("Starting")
	th1_stop = threading.Event()
	th1 = threading.Thread(target=lt.produce, args=(lt.dataQueue, th1_stop,), name="data_reader")
	lt.debugPrint("Done making thread 1")

	th2_stop = threading.Event()
	th2 = threading.Thread(target=lt.consume, args=(lt.dataQueue, th2_stop,), name="cartesian_converter")
	lt.debugPrint("done making thread 2")

	th1.start()
	th2.start()

	time.sleep(5.0)

	th1_stop.set()
	th2_stop.set()

	time.sleep(0.5)
	lt.debugPrint("Done running threads")
	lt.debugPrint("exiting with code {}".format(lt.exit()))
	lt.debugPrint("queue size at exit: {}".format(lt.dataQueue.qsize()))
	raise SystemExit
#####################
## UNIT TEST 1 END ##
#####################


##
# Placeholder for cartesian conversion ftn
##
def sphericalToCartesian(data):
	time.sleep(0.2)
	print("Placeholder: Cartesian map conversion")
	return data



##
# LidarThreads
# class controls threads for gathering LIDAR data
# **Version 0.10 the actual functions are simulated with time.sleep statements**
##
class LidarThreads():
	def __init__(self):
		# don't forget: netsh interface ip set address "Local Area Connection" static 192.168.0.100
		# global nhokreadings

		# controls a number of debug statements which should only print sometimes
		self.debug = True

		# establish communication with the sensor
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# try:
		# 	self.socket.settimeout(1.0)
		# 	self.socket.connect(("192.168.0.10", 10940))
		# except socket.timeout, e:
		# 	self.debugPrint("I can't connect. Exiting.")
		# 	exit(-1)

		# dataQueue is a Queue of strings
		# each string representing a slice (scan)
		self.dataQueue = Queue.Queue(maxsize=90)

	##
	# produce
	#
	# Description: gets data from the LIDAR unit, puts it into the queue
	#
	# Parameters:
	#   dataQueue - queue to submit data to
	#   stop_event - event to listen to for exit
	##
	def produce(self, dataQueue, stop_event):
		counter = 0
		while (not stop_event.is_set()):
			# get data from the LIDAR scanner
			#self.socket.send('MS'+'0000'+'0000'+'01'+'0'+'03\n')
			time.sleep(0.05) #simulate scan-time


			data = "{0} : This_is_a_string_containing_data".format(counter)
			try:
				print "Producer : "+data
				dataQueue.put(data)
			except Queue.Full, e:
				continue
			counter += 1

		# close thread
		raise SystemExit

	##
	# consume
	#
	# Description: consumes data from the queue
	#
	# Parameters:
	#   dataQueue - queue to consume from
	#   stop_event - the event to watch for quitting.
	##
	def consume(self, dataQueue, stop_event):
		while (not stop_event.is_set()):
			try:
				dataline = dataQueue.get()

				cartDataline = sphericalToCartesian(dataline)

				self.debugPrint("Consumer " + cartDataline)
			except Queue.Empty, e:
				continue

		# close thread
		raise SystemExit

	##
	# debugPrint
	#
	# Description: prints the specified string only when debug boolean is set to True
	#
	# __params__
	##
	def debugPrint(self, str):
		if self.debug == True:
			print str
		return

	##
	# exit
	#
	# Description: closes out the socket
	# returns: 0 on success, -1 on failure
	##
	def exit(self):
		if not self.socket is None:
			self.socket.close()
			return 0
		else:
			return -1

## run the program
main()