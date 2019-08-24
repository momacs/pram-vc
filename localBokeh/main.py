import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6

from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from PramAnalysis import analysis_simple

# updated_cycle_val = 0
# fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
# counts = [[5, 3, 4, 2, 4, 6],[1, 2, 3, 4, 5, 6],[6, 5, 4, 3, 2, 1]]
# source = ColumnDataSource(data=dict(fruits=fruits, counts=counts[updated_cycle_val]))
# plot = figure(x_range=fruits, plot_height=650, toolbar_location=None, title="Fruit Counts")
# plot.vbar(x = 'fruits', top = 'counts', width=0.9, source=source, legend="fruits",
#           line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))
args:dict
keys = ['initial_population', 'round_seed_a', 'round_seed_failure',
        'round_a_b', 'round_a_failure', 'round_b_c', 'round_b_failure',
        'round_c_success', 'round_c_failure', 'round_success_success',
        'round_success_failure', 'round_failure_success', 'round_failure_failure']
tx_dict = dict()
args = curdoc().session_context.request.arguments
for k in keys:
    tx_dict[k] = float((args.get(k)[0]).decode("utf-8"))


probe_data: pd.DataFrame
probe_data = analysis_simple(tx_dict=tx_dict, population=tx_dict.get('initial_population'))
max_rows = len(probe_data.index)
min_rows = 0
plot_data = probe_data.iloc[min_rows]
plot_x = list(plot_data.index)
plot_y = plot_data.values
# print(plot_x)
# # print(plot_y)

probe_source = ColumnDataSource(data=dict(plot_x=plot_x, plot_y=plot_y))
plot = figure(x_range=plot_x, plot_height=650, toolbar_location=None, title="Population Distribution")
plot.vbar(x = 'plot_x', top = 'plot_y', width=0.9, source=probe_source, legend="plot_x",
          line_color='white', fill_color=factor_cmap('plot_x', palette=Spectral6, factors=plot_x))
plot.legend.location = "top_center"
# print(probe_source)
# plot = figure(x_range=plot_x, plot_height=650, toolbar_location=None, title="Fruit Counts")
# plot.vbar(x = 'fruits', top = 'counts', width=0.9, source=source, legend="fruits",
#           line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))


# Set up widgets
text = TextInput(title="title", value='Probes and Population')
# cycle = Slider(title="Cycle", value=0, start=0, end=2, step=1)
cycle = Slider(title="Cycle", value=min_rows, start=min_rows, end=max_rows, step=1)

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):
    updated_cycle_val = cycle.value;
    # print("updated_cycle_val = ", updated_cycle_val)

    # print(counts[updated_cycle_val])
    # source.data = dict(fruits=fruits, counts=counts[updated_cycle_val])

    plot_data = probe_data.iloc[updated_cycle_val]
    plot_x = list(plot_data.index)
    plot_y = plot_data.values
    probe_source.data = dict(plot_x = plot_x, plot_y = plot_y)


cycle.on_change('value', update_data)

# Set up layouts and add to document
inputs = column(cycle)

curdoc().add_root(column(plot, inputs, width=1400))
curdoc().title = "Distribution"