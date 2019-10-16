import os,sys
from collections import OrderedDict
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
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
from localBokeh.transition_graphviz import generate_digraph

growth_rate_min = 0.5
growth_rate_max = 5.0

args:dict
keys = ['initial_population', 'round_seed_a', 'round_seed_failure', 'round_a_b',
        'round_a_failure', 'round_b_c', 'round_b_failure', 'round_c_success',
        'round_c_failure', 'round_success_success', 'round_success_failure',
        'round_failure_success', 'round_failure_failure', 'round_a_a', 'round_b_b',
        'round_c_c', 'growth_a', 'growth_b', 'growth_c', 'growth_success',]


tx_dict = OrderedDict()
args = curdoc().session_context.request.arguments
if args is not None and len(args) > 2:
    for k in keys:
        tx_dict[k] = float((args.get(k)[0]).decode("utf-8"))
else:
    tx_dict = None
# print(tx_dict)
probe_group_valuation: pd.DataFrame
probe_group_mass: pd.DataFrame
probe_group_valuation, probe_group_mass = analysis_Complex(tx_dict=tx_dict, population=None)
max_row = len(probe_group_valuation.index) - 1
min_row = 0
plot_data = probe_group_valuation.iloc[min_row]
plot_x = list(plot_data.index)
plot_y = plot_data.values
plot_pop = probe_group_mass.iloc[min_row]
# print(probe_data)

annual_data = probe_group_valuation.sum(axis= 1)
# print(annual_data)
year = [str(i) for i in range(annual_data.shape[0])]

p = figure(x_range=year, plot_height=550, title="Annual Exit Valuations",
           toolbar_location=None, tools="")
p.vbar(x=year, top=annual_data, width=0.9)

TOOLTIPS = [
    ("Group Valuation", '@plot_y')
]
#todo - Add Hover, Add mass chart, Add another chart for comparision, Add proper labels, Display markov chain on the UI
probe_source = ColumnDataSource(data=dict(plot_x=plot_x, plot_y=plot_y, plot_pop = plot_pop))

exit_valuation_plot = figure(x_range=plot_x, plot_height=650, toolbar_location=None, tooltips = TOOLTIPS,
                             title="Valuation Distribution Among various stages")
# exit_valuation_plot.yaxis.axis_label.format(text_font_size = '24pt' )
exit_valuation_plot.vbar(x ='plot_x', top ='plot_y', width=0.9, source=probe_source, legend="plot_x",
                         line_color='white', fill_color=factor_cmap('plot_x', palette=Spectral6, factors=plot_x,))
exit_valuation_plot.legend.location = "top_left"
exit_valuation_plot.legend.orientation = "horizontal"
exit_valuation_plot.xaxis.axis_label = "Rounds"
exit_valuation_plot.yaxis.axis_label = "Exit Valuation"
exit_valuation_plot.xaxis.axis_label_text_font_size = '16pt'
exit_valuation_plot.yaxis.axis_label_text_font_size = '16pt'
# exit_valuation_plot.title.axis_label_text_font_size = '16pt'
#Charting for mass in groups
exit_population_plot = figure(x_range=plot_x, plot_height=650, toolbar_location=None, tooltips = TOOLTIPS,
                             title="Population Distribution Among various stages")
exit_population_plot.vbar(x ='plot_x', top ='plot_pop', width=0.9, source=probe_source, legend="plot_x",
                         line_color='white', fill_color=factor_cmap('plot_x', palette=Spectral6, factors=plot_x,))
exit_population_plot.legend.location = "top_left"
exit_population_plot.legend.orientation = "horizontal"
exit_population_plot.xaxis.axis_label = "Rounds"
exit_population_plot.yaxis.axis_label = "Number of startups (Mass)"
# Set up widgets
text = TextInput(title="title", value='Probes and Population')
# cycle = Slider(title="Cycle", value=0, start=0, end=2, step=1)
cycle = Slider(title="Year", bar_color = "green", value=min_row, start=min_row, end=max_row, step=1)
# Set up widgets

growth_rate_A = Slider(title="Growth Rate A", value=1.5, start=-5.0, end=5.0, step=0.1)
growth_rate_B = Slider(title="Growth Rate A", value=1.0, start=-5.0, end=5.0, step=0.1)
growth_rate_C = Slider(title="Growth Rate A", value=0.0, start=0.0, end=2*np.pi)
growth_rate_success = Slider(title="Growth Rate A", value=1.0, start=0.1, end=5.1, step=0.1)

transition_matrix  = generate_digraph()

# Set up callbacks
def update_title(attrname, old, new):
    exit_valuation_plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):
    updated_cycle_val = cycle.value;
    # print("updated_cycle_val = ", updated_cycle_val)

    # print(counts[updated_cycle_val])
    # source.data = dict(fruits=fruits, counts=counts[updated_cycle_val])

    plot_data = probe_group_valuation.iloc[updated_cycle_val]
    population_data = probe_group_mass.iloc[updated_cycle_val]
    plot_x = list(plot_data.index)
    plot_y = plot_data.values
    plot_pop = population_data.values
    probe_source.data = dict(plot_x = plot_x, plot_y = plot_y, plot_pop = plot_pop)


cycle.on_change('value', update_data)

# Set up layouts and add to document
inputs = column(cycle)

curdoc().add_root(column(row(exit_valuation_plot, exit_population_plot),
                         row(widgetbox([inputs],sizing_mode="stretch_width")),
                         row(p), width=1200))
curdoc().title = "Distribution"
