"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import time
import numpy as np
from random import random as rand
from math import*

from pylsl import StreamInfo, StreamOutlet

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 1 channel, 100 Hz, and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover)
#info = StreamInfo('EEG', 2, 10)
fs=100.
info = StreamInfo('BioSemi', 'EEG', 6, fs, 'float32', 'myuid34234')
x = (0, 4*np.pi, 100)
# next make an outlet
outlet = StreamOutlet(info)

print("now sending data...")
while True:
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
    mysample = [rand(),rand(),rand(),rand(),rand(),rand()]
    #
    # now send it and wait for a bit
    outlet.push_sample(mysample)
    time.sleep(1./fs)