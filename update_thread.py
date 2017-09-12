#################################################
#####  does only update
#################################################

from functools import partial
from random import random
from threading import Thread
import time

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure

from tornado import gen
from pylsl import StreamInlet, resolve_stream

# first resolve an EEG stream on the lab network
#print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])
num_channels = inlet.channel_count
_, time_offset = inlet.pull_sample()
print("inlet time offset:", time_offset)

# this must only be modified from a Bokeh session callback
d = dict(x=[])
for c in range(num_channels):
    d['y%d' % c] = []

source = ColumnDataSource(data=d)

# This is important! Save curdoc() to make sure all threads
# see then same document.
doc = curdoc()



@gen.coroutine
def update(d):
    source.stream(d)

#def blocking_task():

#    t=0
#    while True:
#
#        # do some blocking computation
#        time.sleep(0.1)
#        #x, y = random(), random()
#
#        y = random();
#        # but update the document from callback
#        doc.add_next_tick_callback(partial(update, x=t, y=y))
#        t = t+1

def blocking_task():
    while True:
        # do some blocking computation
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        time.sleep(0.5)
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        print(timestamp, sample)

        x = timestamp - time_offset

        # but update the document from callback
        d = dict(x=[x])
        for c in range(num_channels):
            d['y%d' % c] = [sample[c] + c]
        doc.add_next_tick_callback(partial(update, d=d))


p = figure()
for c in range(num_channels):
    p.line(x='x', y='y%d' % c, source=source)

doc.add_root(p)

thread = Thread(target=blocking_task)
thread.start()