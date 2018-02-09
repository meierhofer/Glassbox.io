import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource


data_dict = dict(x=[10,20,30,40], y=[50,60,70,80])

source = ColumnDataSource(data=data_dict)


print('data_dict:  ', data_dict)

new_data_dict = dict(x=[1,2,3,4], y=[5,6,7,8])
print('new_data_dict:  ', new_data_dict)


new_data_dict.update(data_dict)
#print('update', new_data_dict)



source.patch({ 'x' : [(slice(len(new)), new_data_dict['x'])], 'y' : [(slice(1), new_data_dict['y'])] })

print(data_dict)

#source.stream(data_dict)

#print('patches:  ', patches)

#update = dict(list(new_data_dict.items()) + list(data_dict.items()))

#update = dict(new_data_dict.items() + data_dict.items())





#dest = {**new_data_dict, **data_dict}

#dest = {}
#dest.update(data_dict.items() + new_data_dict.items())
#dest.update(new_data_dict)


#print('dest:  ', dest)
