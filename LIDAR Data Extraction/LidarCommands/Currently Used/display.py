#Author: Alex Schendel
#A little program intended to be used with raspi_threads
#Given a data file from the rpi, this will open the file and display the data.

import pickle
import matplotlib.pyplot as plt
import numpy as np

def main():
    filename=input('Enter the filename: ')
    with open(filename, 'rb') as f:
        data_arrays = pickle.load(f)
    display_map(data_arrays)


def display_map(data):
    X = np.asarray(data[0])
    y = np.asarray(data[1])
    z = np.asarray(data[2])
    plt.pcolormesh([z, data[5]])  # Figure out how this works! Also, why z and dist
    plt.colorbar()  # need a colorbar to show the intensity scale
    plt.show()


main()