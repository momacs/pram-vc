import base64
import math
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8
from graphviz import Digraph
import numpy as np

from bokeh.models import ColumnDataSource, Range1d, Plot, LinearAxis, Grid
from bokeh.models.glyphs import ImageURL
from bokeh.io import curdoc, show


def generate_digraph(tx_dict = None, node_list = None, op_png = False):
    # Sample for testing the function
    if tx_dict is None:
        tx_dict = dict(
            round_seed_a=0.3,
            round_seed_failure=0.67,
            round_a_b=0.2,
            round_a_failure=0.3,
            round_b_c=0.3,
            round_b_failure=0.2,
            round_c_success=0.3,
            round_c_failure=0.4,
            round_success_success=1,
            round_success_failure=0,
            round_failure_success=0,
            round_failure_failure=1,
            round_seed_success=0.03,
            round_a_success=0.1,
            round_b_success=0.2,
            round_a_a=0.4,
            round_b_b=0.3,
            round_c_c=0.3,
            growth_a=2,
            growth_b=2.2,
            growth_c=2.5,
            growth_success=1.2,
            initial_population=1000
        )

    if node_list is None:
        node_list = ["seed", "a", "b", "c", "success", "failure"]

    tx_graph = Digraph("Transition_Graph", filename="tx_graph.py",
                       node_attr={'color': 'lightblue2', 'style': 'filled'})
    tx_graph.attr(size='6,6')

    for node in node_list:
        tx_graph.node(node.upper())

    for node_name, node_value in tx_dict.items():
        node_name:str
        if node_name.find("round") >= 0:
            _, start_node, end_node = node_name.split("_")
            tx_graph.edge(start_node.upper(), end_node.upper(), label=str(round(node_value,2)))
    tx_graph.format='png'
    tx_graph.render()
    # Line below for PNG
    if op_png:
        chart_output = tx_graph.pipe(format='png')
        chart_output = base64.b64encode(chart_output).decode('utf-8')
    else:
        chart_output = tx_graph.pipe(format='svg')


    return chart_output
    # tx_graph.view()

generate_digraph(op_png = True)

def generate_bokeh_graph():

    N = 8
    node_indices = list(range(N))

    plot = figure(title="Graph Layout Demonstration", x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),
                  tools="", toolbar_location=None)

    graph = GraphRenderer()

    graph.node_renderer.data_source.add(node_indices, 'index')
    graph.node_renderer.data_source.add(Spectral8, 'color')
    graph.node_renderer.glyph = Oval(height=0.1, width=0.2, fill_color="color")

    graph.edge_renderer.data_source.data = dict(
        start=[0] * N,
        end=node_indices)

    ### start of layout code
    circ = [i * 2 * math.pi / 8 for i in node_indices]
    x = [math.cos(i) for i in circ]
    y = [math.sin(i) for i in circ]
    graph_layout = dict(zip(node_indices, zip(x, y)))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    ### Draw quadratic bezier paths
    def bezier(start, end, control, steps):
        return [(1 - s) ** 2 * start + 2 * (1 - s) * s * control + s ** 2 * end for s in steps]

    xs, ys = [], []
    sx, sy = graph_layout[0]
    steps = [i / 100. for i in range(100)]
    for node_index in node_indices:
        ex, ey = graph_layout[node_index]
        xs.append(bezier(sx, ex, 0, steps))
        ys.append(bezier(sy, ey, 0, steps))
    graph.edge_renderer.data_source.data['xs'] = xs
    graph.edge_renderer.data_source.data['ys'] = ys

    plot.renderers.append(graph)

    output_file("graph.html")
    show(plot)


# generate_bokeh_graph()
#
# u = Digraph('digraph', file_path='digraph.gv',
#             node_attr={'color': 'lightblue2', 'style': 'filled'})
# u.attr(size='6,6')
#
# u.edge('5th Edition', '6th Edition', label='n')
# u.edge('5th Edition', 'PWB 1.0',label='n')
# u.edge('6th Edition', 'LSX',label='n')
# u.edge('6th Edition', '1 BSD')
# u.edge('6th Edition', 'Mini Unix')
# u.edge('6th Edition', 'Wollongong')
# u.edge('6th Edition', 'Interdata')
# u.edge('Interdata', 'Unix/TS 3.0')
# u.edge('Interdata', 'PWB 2.0')
# u.edge('Interdata', '7th Edition')
# u.edge('7th Edition', '8th Edition')
# u.edge('7th Edition', '32V')
# u.edge('7th Edition', 'V7M')
# u.edge('7th Edition', 'Ultrix-11')
# u.view()







#https://stackoverflow.com/questions/51038073/flask-dynamic-graphviz-and-svg-example
# You can use svg just like this:
#
# {{ chart_output|safe }}
# and also, you can use png format:
#
# @app.route('/')
# def svgtest():
#     chart_data = Graph()
#
#     chart_data.node('H', 'Hello')
#     chart_data.node('W', 'World')
#     chart_data.edge('H', 'W')
#
#
#     chart_output = chart_data.pipe(format='png')
#     chart_output = base64.b64encode(chart_output).decode('utf-8')
#
#     return render_template('svgtest.html', chart_output=chart_output)
# and the html like this:
#
# <img src="data:image/png;base64,{{chart_output|safe}}" />