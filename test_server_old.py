#################################################
#####  test Server old version without chunk
#################################################

from random import random

import time
from time import sleep
from bokeh.layouts import column, row
# from bokeh.models import Button
from bokeh.palettes import BuPu9
from bokeh.palettes import RdYlBu6
from bokeh.plotting import figure, curdoc
from bokeh.io import curdoc, show
from bokeh.client import push_session
from bokeh.models import PrintfTickFormatter, CustomJS, ColumnDataSource
from bokeh.models.tickers import FixedTicker
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider
from bokeh.layouts import widgetbox

from pylsl import StreamInlet, resolve_stream
from threading import Thread
from tornado import gen
from functools import partial



doc = curdoc()
# todo: maybe later in the code???

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

# get number of channels
num_channels = inlet.channel_count

update_intervall = 5. #seconds
sampling_frequency = inlet.info().nominal_srate()
print(update_intervall, sampling_frequency)

print("number of channels:", num_channels)

history = num_channels

# create a plot and style its properties
#p = figure(x_range=(0, 100), y_range=(-1, 10), responsive=True)
p = figure()#x_range=(6, 7), y_range=(-1, 10), width=900)
p.background_fill_color = 'white'
p.outline_line_color = None

# only horizontal lines
p.ygrid.grid_line_color = 'gray'
p.ygrid.grid_line_alpha = 0.5
p.ygrid.grid_line_dash = [6, 4]
p.xgrid.grid_line_color = None
p.ygrid.bounds = (0, num_channels)

num_ticker = range(num_channels)

#p.yaxis.ticker = FixedTicker(ticks= list(num_ticker))

p.yaxis.ticker = list(num_ticker)

#p.yaxis.ticker = FixedTicker(ticks=range(num_channels))

p.yaxis[0].formatter = PrintfTickFormatter(format="Channel%2d")
p.yaxis.minor_tick_line_color = None

#p.toolbar_location = None

# add a text renderer to our plot (no data yet)
#r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
#           text_baseline="middle", text_align="center")


#for index in reversed(range(num_channels)):
#    color = BuPu#[index % 6]
#    name = "Channel %d" % index
#    source = ColumnDataSource(data=dict(x=[], y=[]))
#    p.line(x='x', y='y', source=source, line_width=2, legend='name', alpha=1.)


data_dict = dict(x=[])
for index in range(num_channels):
    data_dict['y%d' % index] = []
    print("line90:", data_dict)


source = ColumnDataSource(data=data_dict)
print("line 93:",source)

#interactive legend
for index in reversed(range(num_channels)):
    color = BuPu9[index % 9]
    name = "Channel %d" % index
    #print(index)
    p.line(x='x', y='y%d' % index, source=source, line_width=2, color=color, legend=name, alpha=1.)



p.legend.location = "top_left"
p.legend.click_policy = "hide"



@gen.coroutine
def update(update_dict):
    #print("line 112:",update_dict)
    print("KARO")
    source.stream(update_dict)
    #print("line 115", update_dict)
    print("ALEKS")


# create a callback that will update the samples
def thread_function():

    while True:
        time.sleep(1.)

        # BEST PRACTICE --- update .data in one step with a new dict

        sample, timestamp = inlet.pull_sample()


        #finally saving timestamps in the dict
        update_dict = dict(x=[timestamp])
        #print("line 135", update_dict)

        #going through the samples and save them to the responding y-value/channel


        for count in reversed(range(num_channels)):
            update_dict['y%d' % count] = [sample[count] + count]
            print("sample[count]",sample[count])
            print(sample[count]+1)
        #print(chunk)

        # but update the document from callback
        #doc.add_next_tick_callback(partial(update, update_dict=update_dict))
        doc.add_next_tick_callback(partial(update, update_dict=update_dict))




thread = Thread(target=thread_function)
thread.start()

doc.add_root(p)


