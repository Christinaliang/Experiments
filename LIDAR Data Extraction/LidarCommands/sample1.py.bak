import usb, sys, time, argparse, struct, socket, binascii, Queue
from threading import Thread

parser = argparse.ArgumentParser(description='Data log imu and laser')
parser.add_argument('-f', '--file', dest='filename', help="logfilename", metavar="FILE", default="ghgh.txt")
parser.add_argument("-q", "--quiet", action="store_false", dest="verbose", default=False, help="don't print status messages to stdout")
args = parser.parse_args()

dataqueue = Queue.Queue()
nimureadings, nhokreadings = 0, 0
bTerminate = False

# handle incoming commands from command line
def ReadStdin():
    global bTerminate
    print "Type 'q' and return to quit"
    while True:
        x = sys.stdin.read(2) 
        if x[0] == 'q':
            bTerminate = True
            dataqueue.put("TERMINATE")
            break
        print [x]


# handle the output to file
def OutputQueue():
    fout = open(args.filename, "w")
    while True:
        try:
            x = dataqueue.get(timeout=10)
        except Queue.Empty, e:
            continue
        if x == "TERMINATE":
            fout.write("TERMINATE\n")
            break
        fout.write("".join([x[0], " ", str(x[1]), " ", x[2], "\n"]))
    fout.close()
    

# IMU connection and reading
def IMUreading():
    global nimureadings
    dev = usb.core.find(idProduct=0x3065)
    endpoints = [e  for c in dev  for i in c  for e in i]
    e0, e1, e2 = endpoints
    e1.write(binascii.unhexlify("75650C0505110101000319"))  # stop sending
    x = e2.read(1000, timeout=1000)
    e1.write(binascii.unhexlify("75650C101008010404000A07000A0A000A0E000A5EF6"))  # enable accel delta-theta, quat, time
    x = e2.read(1000, timeout=1000)
    e1.write(binascii.unhexlify("75650C050511010101041A"))  # start streaming
    x = e2.read(1000, timeout=1000)
    while not bTerminate:
        x = e2.read(1000, timeout=1000)
        dataqueue.put(("IMU", time.clock(), binascii.hexlify(x)))
        nimureadings += 1

    e1.write(binascii.unhexlify("75650C0505110101000319"))  # stop sending
    x = e2.read(1000, timeout=1000)


# IMU connection and reading
def HOKreading():
    # don't forget: netsh interface ip set address "Local Area Connection" static 192.168.0.5   then ipconfig/renew to check
    global nhokreadings
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    s.connect(("192.168.0.10", 10940))
    s.send('PP\n')
    s.send('MD0000108001000\n')
    res = [ ]
    for i in range(100):
        lres = s.recv(100).split("\n")
        rectime = time.clock()
        lres.reverse()
        res.append(lres.pop())
        while lres:
            sres = "".join(res)
            if not sres:
                nhokreadings += 1
            print ("HOK", rectime, len(sres))
            res = [ lres.pop() ]
            
    # should turn it off

threads = [ ]
for f in [ OutputQueue, ReadStdin, IMUreading, HOKreading ]:
    fthread = Thread(target=f)
    fthread.daemon = True
    fthread.start()
    threads.append(fthread)
    
while not bTerminate:
    time.sleep(1)
    if int(time.clock()) % 5 == 1:
        print time.clock(), "seconds passed; hokreadings:", nhokreadings, " imureadings:", nimureadings

threads[0].join()
    