import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import pandas as pd
import numpy as np

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
from PramAnalysis import analysis_Complex

args:dict
keys = ['initial_population', 'round_seed_a', 'round_seed_failure', 'round_a_b',
        'round_a_failure', 'round_b_c', 'round_b_failure', 'round_c_success',
        'round_c_failure', 'round_success_success', 'round_success_failure',
        'round_failure_success', 'round_failure_failure', 'round_a_a', 'round_b_b',
        'round_c_c', 'growth_a', 'growth_b', 'growth_c', 'growth_success',]

tx_dict = dict()
args = curdoc().session_context.request.arguments
if len(args) > 2:
    for k in keys:
        tx_dict[k] = float((args.get(k)[0]).decode("utf-8"))
else:
    tx_dict = None
# print(tx_dict)
probe_data: pd.DataFrame
probe_data = analysis_Complex(tx_dict=tx_dict, population=None)
max_rows = len(probe_data.index)-1
min_rows = 0
plot_data = probe_data.iloc[min_rows]
plot_x = list(plot_data.index)
plot_y = plot_data.values
# print(probe_data)

annual_data = probe_data.sum(axis= 1)
# print(annual_data)
year = [str(i) for i in range(annual_data.shape[0])]

p = figure(x_range=year, plot_height=550, title="Annual Exit Valuations",
           toolbar_location=None, tools="")
p.vbar(x=year, top=annual_data, width=0.9)


probe_source = ColumnDataSource(data=dict(plot_x=plot_x, plot_y=plot_y))
plot = figure(x_range=plot_x, plot_height=650, toolbar_location=None, title="Valuation Distribution Among various stages")
plot.vbar(x = 'plot_x', top = 'plot_y', width=0.9, source=probe_source, legend="plot_x",
          line_color='white', fill_color=factor_cmap('plot_x', palette=Spectral6, factors=plot_x))
plot.legend.location = "top_left"
plot.legend.orientation = "horizontal"

# print(probe_source)
# plot = figure(x_range=plot_x, plot_height=650, toolbar_location=None, title="Fruit Counts")
# plot.vbar(x = 'fruits', top = 'counts', width=0.9, source=source, legend="fruits",
#           line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))


# Set up widgets
text = TextInput(title="title", value='Probes and Population')
# cycle = Slider(title="Cycle", value=0, start=0, end=2, step=1)
cycle = Slider(title="Year", value=min_rows, start=min_rows, end=max_rows, step=1)

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

curdoc().add_root(column(plot, inputs,column(p), width=1800))
curdoc().title = "Distribution"



#
# fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
# years = ["2015", "2016", "2017"]
# colors = ["#c9d9d3", "#718dbf", "#e84d60"]
#
# data = {'fruits' : fruits,
#         '2015'   : [2, 1, 4, 3, 2, 4],
#         '2016'   : [5, 3, 4, 2, 4, 6],
#         '2017'   : [3, 2, 4, 4, 5, 3]}
#
# colors = ["#c9d9d3", "#718dbf", "#e84d60","#c9d9d3", "#718dbf", "#e84d60"]
# cols = ["Seed", "a", "b", "c", "success", "failure"]
# p = figure(x_range=cols, plot_height=250, title="Exit Valuation by Year",
#             toolbar_location=None)
#            # toolbar_location=None, tools="hover", tooltips="$name @fruits: @$name")
# years = list(range(max_rows))
# p.vbar_stack(years, x='year', width=0.9,color=colors, source=probe_source,
#              )
#
# # p.y_range.start = 0
# # p.x_range.range_padding = 0.1
# p.xgrid.grid_line_color = None
# p.axis.minor_tick_line_color = None
# p.outline_line_color = None
# p.legend.location = "top_left"
# p.legend.orientation = "horizontal"
# #
# # curdoc().add_root(row(p, width=800))
# # curdoc().title = "sample"
#
# curdoc().add_root(column(plot, inputs,p , width=1400))
# curdoc().title = "Distribution"