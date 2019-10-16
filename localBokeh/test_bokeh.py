import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import pandas as pd
import numpy as np

import numpy as np
import pandas as pd
# from bokeh.io import curdoc
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

growth_rate_min = 0.5
growth_rate_max = 5.0

args:dict
keys = ['initial_population', 'round_seed_a', 'round_seed_failure', 'round_a_b',
        'round_a_failure', 'round_b_c', 'round_b_failure', 'round_c_success',
        'round_c_failure', 'round_success_success', 'round_success_failure',
        'round_failure_success', 'round_failure_failure', 'round_a_a', 'round_b_b',
        'round_c_c', 'growth_a', 'growth_b', 'growth_c', 'growth_success',]

tx_dict = dict()
# args = curdoc().session_context.request.arguments
args = None
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
    ("Group Valuation", "($plot_y)")

]

probe_source = ColumnDataSource(data=dict(plot_x=plot_x, plot_y=plot_y, plot_pop = plot_pop))
plot = figure(x_range=plot_x, plot_height=650, toolbar_location=None, tooltips = TOOLTIPS,
              title="Valuation Distribution Among various stages")
plot.vbar(x = 'plot_x', top = 'plot_y', width=0.9, source=probe_source, legend="plot_x",
          line_color='white', fill_color=factor_cmap('plot_x', palette=Spectral6, factors=plot_x,))
plot.legend.location = "top_left"
plot.legend.orientation = "horizontal"
show(plot)
