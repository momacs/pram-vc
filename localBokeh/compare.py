''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Button
from bokeh.plotting import figure
import os,sys
from collections import OrderedDict
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from PramAnalysis import analysis_simple
from PramAnalysis import analysis_Complex
from localBokeh.transition_graphviz import generate_digraph
from localBokeh.chart_utils import PramInteractiveBokehInputs, PramInteractiveCharts

args:dict
keys = ['initial_population', 'round_seed_a', 'round_seed_failure', 'round_a_b',
        'round_a_failure', 'round_b_c', 'round_b_failure', 'round_c_success',
        'round_c_failure', 'round_success_success', 'round_success_failure',
        'round_failure_success', 'round_failure_failure', 'round_a_a', 'round_b_b',
        'round_c_c', 'growth_a', 'growth_b', 'growth_c', 'growth_success',]
tx_dict = OrderedDict()
args = curdoc().session_context.request.arguments
# if args is not None and len(args) > 2:
#     for k in keys:
#         tx_dict[k] = float((args.get(k)[0]).decode("utf-8"))
# else:
#     tx_dict = None
tx_dict = None
this_sim = PramInteractiveCharts(tx_dict)
this_sim.generate_simualtions()
p1,p2,p3 = this_sim.generate_fancy_plot()
# sim_input = PramInteractiveBokehInputs(tx_dict)
that_sim = PramInteractiveCharts(tx_dict)
that_sim.generate_simualtions()
r1,r2,r3 = that_sim.generate_fancy_plot()
this_inputs = PramInteractiveBokehInputs(tx_dict)
that_inputs = PramInteractiveBokehInputs(tx_dict)
max_row = this_sim.max_row
min_row = this_sim.min_row
btn_submit = Button(label= 'Run Simulations')
def btn_submit_handler():
    this_tx_matrix = this_inputs.update_tx_matrix()
    this_sim.regenerate_simulation(this_tx_matrix)
    that_tx_matrix = that_inputs.update_tx_matrix()
    that_sim.regenerate_simulation(that_tx_matrix)
    cycle.value = min_row
btn_submit.on_click(btn_submit_handler)
cycle = Slider(title="Year", bar_color = "green", value=min_row, start=min_row, end=max_row, step=1)
def cycle_change_handler(attrname, old, new):
    updated_cycle_val = cycle.value;
    this_sim.update_plot_data(index=updated_cycle_val)
    that_sim.update_plot_data(index=updated_cycle_val)
cycle.on_change('value', cycle_change_handler)

# Set up layouts and add to document
left_plot = row(column(*this_inputs.get_sliders(), btn_submit, width = 200), column(p1, p2, p3), width = 1000)
right_plot = row(column(r1, r2, r3), column(*that_inputs.get_sliders(), btn_submit, width = 200),  width = 1000)
plots = row(left_plot, right_plot, width = 2000)
input = row(column(width = 400), column(cycle, width = 1000))
curdoc().add_root(column(plots,input))
curdoc().title = "Compare Distribution"