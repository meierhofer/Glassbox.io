#################################################
#####  test Server that does all the vizualisation
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
from bokeh.layouts import layout

from pylsl import StreamInlet, resolve_stream
from threading import Thread
from tornado import gen
from functools import partial
import numpy as np



doc = curdoc()
# todo: maybe later in the code???

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

# get number of channels
num_channels = inlet.channel_count

update_intervall = 0.5 #seconds
fs = inlet.info().nominal_srate()
#print(update_intervall, sampling_frequency)

#print("number of channels:", num_channels)

history = num_channels

# create a plot and style its properties
#p = figure(x_range=(0, 100), y_range=(-1, 10), responsive=True)
p = figure(sizing_mode='stretch_both')#x_range=(6, 7), y_range=(-1, 10), width=900)
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
    #print("line90:", data_dict)


source = ColumnDataSource(data=data_dict)
#print("line 93:",source)

#interactive legend
for index in reversed(range(num_channels)):
    color = BuPu9[index % 9]
    name = "Channel %d" % index
    #print(index)
    p.line(x='x', y='y%d' % index, source=source, line_width=2, color=color, legend=name, alpha=1.)



p.legend.location = "top_left"
p.legend.click_policy = "hide"

sample_count = 1


@gen.coroutine
def update(update_dict):
    #print("line 112:",update_dict)
    print("UPDATE")
    source.stream(update_dict)
    #print("line 115", update_dict)
    print("STREAM")


# create a callback that will update the samples
def thread_function():
    global sample_count
    while True:
        time.sleep(1.)

        # BEST PRACTICE --- update .data in one step with a new dict

        #sample, timestamp = inlet.pull_sample()
        #sample, timestamp = inlet.do_pull_chunk()
        sample, timestamp = inlet.pull_chunk(timeout=update_intervall * 1.2, max_samples=int(fs * update_intervall))
        #transposing list of lists, to have the correct order for the samples
        chunk = list(map(list, zip(*sample)))

        #finally saving timestamps in the dict
        #print("line 135", update_dict)
        update_dict = dict(x=timestamp)

        #going through the samples and save them to the responding y-value/channel
        #patches = dict()
        #s = slice(3*fs)

        for ch_index in range(len(chunk)):
            #print("sample count:", sample_count)

            for s_index in range(len(chunk[ch_index])):
                #print("sample_index:", s_index)
                #sleep(3)
                #sample_count = sample_count + 1
                #print("update sample count:", sample_count)
                #sleep(5)
                #if sample_count == (7*fs):
                    #print("update sample count:", sample_count)
                    #print("sample_count mod 300:", sample_count % (3*fs))
                    #sample_count = 1
                    #sleep(2)
                    #patches['x'] = [slice(300), timestamp]
                    #patches['y%d' % ch_index] = [slice(300), chunk[ch_index]]
                    #source.patch(patches)
                    #update_dict.update(patches)
                    #sleep(30)

                #else:
                    #print("Hallo BIN IM ELSE")
                chunk[ch_index][s_index] = chunk[ch_index][s_index] + ch_index - 0.5
                update_dict['y%d' % ch_index] = chunk[ch_index]
                    #sleep(10)



        sleep(update_intervall * 0.95)

        # but update the document from callback

        doc.add_next_tick_callback(partial(update, update_dict=update_dict))




thread = Thread(target=thread_function)
thread.start()

# create some widgets
slider = Slider(start=0, end=10, value=1, step=.1, title="Slider")
button_group = RadioButtonGroup(labels=["Option 1", "Option 2", "Option 3"], active=0)
select = Select(title="Option:", value="foo", options=["1", "2", "3", "4"])
button_1 = Button(label="Button 1")
button_2 = Button(label="Button 2")

# put the results in a row
#show(widgetbox(button_1, slider, button_group, select, button_2, width=300))


# put the results in a row
widget_box = widgetbox(button_1, slider, button_group, select, button_2, sizing_mode='stretch_both')#, width=300)
#scale_both

#doc.add_root(toolbox)
#row(children=[widget_box_1, plot_1], sizing_mode='stretch_both')


#l = layout([
#    bollinger(),
#    slider(),
#    linked_panning(),
#], sizing_mode='stretch_both')
#doc_layout.children[0].children[-1].children.append(p)
#And change your layout to:

#doc_layout = layout(sizing_mode='scale_width')
#doc_layout.children.append(row(column(widgetbox(b, t1)), column()))

#layout = row(children=[widget_box_1, plot_1], sizing_mode='scale_both')

#resize_plot = layout(widget_box, p, sizing_mode='stretch_both')

#layout = row(widget_box, p)

#doc.add_root(layout)
doc.add_root(p)


