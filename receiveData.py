"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream
from time import sleep
# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

update_intervall = 5. #seconds
sampling_frequency = inlet.info().nominal_srate()
print(update_intervall, sampling_frequency)

while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)

    sample, timestamp = inlet.pull_chunk(timeout=update_intervall*1.2, max_samples=int(sampling_frequency*update_intervall))
    chunk = list(map(list, zip(*sample)))
    d = dict(x=timestamp)
    for c in range(len(chunk)):
        d['y%d' % c] = chunk[c]
    print(len(sample))
    sleep(update_intervall*0.95)


