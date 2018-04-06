__author__ = 'Alex Schendel, Hayden Liao, and Alex Reinemann'

import raspi_threads as rasp
from rasp import *
from constants import *

def __main__():
    #TODO implement publisher... Also check timing (main may take time to run)
    rasp.scan()#run a LIDAR scan (see file raspi_threads.py)