import os
import sys
from collections import OrderedDict
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import pandas as pd
from bokeh.models.widgets import Slider
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from PramAnalysis import analysis_Complex


class PramInteractiveCharts:

    def __init__(self, tx_dict = None):
        if  not tx_dict:
            tx_dict = OrderedDict(
                initial_population=100,
                invest_amt=1000,
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
                round_a_a=0.4,
                round_b_b=0.3,
                round_c_c=0.3,
                growth_a=2,
                growth_b=2.2,
                growth_c=2.5,
                growth_success=1.2,
            )
        self.transition_dict = OrderedDict.copy(tx_dict)
        self.inputs = PramInteractiveBokehInputs(self.transition_dict)
        self.probe_group_valuation: pd.DataFrame
        self.probe_group_mass: pd.DataFrame
        self.data_source :ColumnDataSource = None
        self.annual_valuation_source: ColumnDataSource = None
        self.tt_valuation = [("Group Valuation", "@valuation{(0.00)}"),("Round", "@plot_x")]
        self.tt_population = [("Group Population", "@population{(0.00)}"), ("Round", "@plot_x")]
        self.tt_annual_val = [("Annual Valuation", "@annual_valuation{(0.00)}"), ("Year", "@year")]

    def regenerate_simulation(self, tx_matrix):
        self.transition_dict = tx_matrix
        self.generate_simualtions()
        self.update_plot_data()

    def generate_simualtions(self):
        self.probe_group_valuation, self.probe_group_mass = analysis_Complex(tx_dict=self.transition_dict, population=None)
        plot_data = self.probe_group_valuation.iloc[0]
        self.plot_x = list(plot_data.index)
        self.min_row = 0
        self.max_row = len(self.probe_group_valuation.index) - 1

    def generate_fancy_plot(self, **kwargs):
        self.generate_simualtions()
        self.update_plot_data(self.min_row)
        # self.annual_valuation_bar_plot = self.generate_annual_valuation_bar_plot()
        # self.exit_valuation_plot = self.generate_exit_valuation_plot()
        # self.exit_population_plot = self.exit_population_plot()
        p1 = self.generate_annual_valuation_bar_plot()
        p2 = self.generate_exit_valuation_plot()
        p3 = self.generate_exit_population_plot()
        return p1,p2,p3

    def update_plot_data(self,index = 0):
        plot_data = self.probe_group_valuation.iloc[index]
        plot_x = list(plot_data.index)
        plot_valuation = plot_data.values
        plot_population = self.probe_group_mass.iloc[index]
        self.annual_valuation = self.probe_group_valuation.sum(axis=1)
        self.year = [str(i) for i in range(self.annual_valuation.shape[0])]
        if not self.data_source:
            self.data_source = ColumnDataSource(
                data=dict(plot_x=plot_x, valuation=plot_valuation, population=plot_population))
            self.annual_valuation_source = ColumnDataSource(data=dict(
                year=self.year,
                annual_valuation=self.annual_valuation )
            )
        else:
            self.data_source.data = dict(plot_x=plot_x, valuation=plot_valuation,
                                         population=plot_population)
            self.annual_valuation_source.data = dict(
                year=[str(i) for i in range(self.annual_valuation.shape[0])],
                annual_valuation=self.annual_valuation)

    def generate_exit_valuation_plot(self):
        exit_valuation_plot = figure(x_range=self.plot_x, plot_height=650, plot_width = 750, toolbar_location=None,
                                     tooltips=self.tt_valuation,
                                     title="Valuation Distribution Among various stages")
        # exit_valuation_plot.yaxis.axis_label.format(text_font_size = '24pt' )
        exit_valuation_plot.vbar(x='plot_x', top='valuation', width=0.9, source=self.data_source, legend="plot_x",
                                 line_color='white',
                                 fill_color=factor_cmap('plot_x', palette=Spectral6, factors=self.plot_x, ))
        exit_valuation_plot.title.text_font_size = '18pt'
        exit_valuation_plot.legend.location = "top_left"
        exit_valuation_plot.legend.orientation = "horizontal"
        exit_valuation_plot.xaxis.axis_label = "Rounds"
        exit_valuation_plot.yaxis.axis_label = "Exit Valuation"
        exit_valuation_plot.xaxis.axis_label_text_font_size = '16pt'
        exit_valuation_plot.yaxis.axis_label_text_font_size = '16pt'
        return exit_valuation_plot
        # exit_valuation_plot.title.axis_label_text_font_size = '16pt'

    def generate_exit_population_plot(self):
        exit_population_plot = figure(x_range=self.plot_x, plot_height=650, plot_width = 750, toolbar_location=None,
                                      tooltips=self.tt_population,
                                      title="Population Distribution Among various stages")
        exit_population_plot.vbar(x='plot_x', top='population', width=0.9, source=self.data_source, legend="plot_x",
                                  line_color='white',
                                  fill_color=factor_cmap('plot_x', palette=Spectral6, factors=self.plot_x, ))
        exit_population_plot.title.text_font_size = '18pt'
        exit_population_plot.legend.location = "top_left"
        exit_population_plot.legend.orientation = "horizontal"
        exit_population_plot.xaxis.axis_label = "Rounds"
        exit_population_plot.yaxis.axis_label = "Number of startups (Mass)"
        exit_population_plot.xaxis.axis_label_text_font_size = '16pt'
        exit_population_plot.yaxis.axis_label_text_font_size = '16pt'

        return exit_population_plot

    def generate_annual_valuation_bar_plot(self):
        self.annual_valuation = self.probe_group_valuation.sum(axis=1)
        p = figure(x_range=self.year, plot_height=650, plot_width = 750,
                   tooltips=self.tt_annual_val,
                   title="Annual Exit Valuations",
                   toolbar_location=None)
        p.vbar(x='year', top='annual_valuation', width=0.9, source=self.annual_valuation_source, )
        p.title.text_font_size = '18pt'
        p.legend.orientation = "horizontal"
        p.xaxis.axis_label = "Rounds"
        p.yaxis.axis_label = "Number of startups (Mass)"
        p.xaxis.axis_label_text_font_size = '16pt'
        p.yaxis.axis_label_text_font_size = '16pt'
        return p

class PramInteractiveBokehInputs:

    def __init__(self, tx_matrix = None):
        if not tx_matrix:
            tx_matrix = OrderedDict(
                initial_population=100,
                invest_val = 1000,
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
                round_a_a=0.4,
                round_b_b=0.3,
                round_c_c=0.3,
                growth_a=2,
                growth_b=2.2,
                growth_c=2.5,
                growth_success=1.2,
            )

        self.slider_dict = OrderedDict()
        self.tx_matrix = OrderedDict.copy(tx_matrix)
        # self.opt = ['100', '1000', '10000', '100000']
        self.opt = ['20', '1000', '10000', '100000']
        self.slider_dict['initial_population'] = Slider(title="Population", value=tx_matrix.get('initial_population'),
                                                        start = 20, end = 10000, step = 100)
        self.slider_dict['invest_val'] = Slider(title="Initial Investment",
                                                   value=tx_matrix.get("invest_val"), start = 1000, end = 100000, step = 1000)
        # self.slider_dict['initial_population'] = Select(title = "Population", options = [100,1000,10000,100000], value = 100)
        self.slider_dict["round_seed_a"]  = Slider(title="Prob. Seed to A",
                                                   value=tx_matrix.get("round_seed_a"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_seed_failure"]  = Slider(title="Prob. Seed to Failure",
                                                         value=tx_matrix.get("round_seed_failure"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_a_b"]  = Slider(title="Prob. A to B",
                                                value=tx_matrix.get("round_a_b"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_a_failure"]  = Slider(title="Prob. A to Failure",
                                                      value=tx_matrix.get("round_a_failure"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_b_c"]  = Slider(title="Prob. B to C",
                                                value=tx_matrix.get("round_b_c"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_b_failure"]  = Slider(title="Prob. B to Failure",
                                                      value=tx_matrix.get("round_b_failure"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_c_success"]  = Slider(title="Prob. C to Success",
                                                      value=tx_matrix.get("round_c_success"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_c_failure"]  = Slider(title="Prob. C to Failure",
                                                      value=tx_matrix.get("round_c_failure"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_success_success"]  = Slider(title="Prob. Success to Success",
                                                            value=tx_matrix.get("round_success_success"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_success_failure"]  = Slider(title="Prob. Success to Failure",
                                                            value=tx_matrix.get("round_success_failure"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_failure_success"]  = Slider(title="Prob. Failure to Success",
                                                            value=tx_matrix.get("round_failure_success"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_failure_failure"]  = Slider(title="Prob. Failure to Failure",
                                                            value=tx_matrix.get("round_failure_failure"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_a_a"]  = Slider(title="Prob. A to A",
                                                value=tx_matrix.get("round_a_a"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_b_b"]  = Slider(title="Prob. B to B",
                                                value=tx_matrix.get("round_b_b"), start = 0, end = 1, step = 0.01)
        self.slider_dict["round_c_c"]  = Slider(title="Prob. C to C",
                                                value=tx_matrix.get("round_c_c"), start = 0, end = 1, step = 0.01)
        self.slider_dict["growth_a"]  = Slider(title="Growth Rate A",
                                               value=tx_matrix.get("growth_a"), start = 0.5, end = 5, step = 0.01)
        self.slider_dict["growth_b"]  = Slider(title="Growth Rate B",
                                               value=tx_matrix.get("growth_b"), start = 0.5, end = 5, step = 0.01)
        self.slider_dict["growth_c"]  = Slider(title="Growth Rate C",
                                               value=tx_matrix.get("growth_c"), start = 0.5, end = 5, step = 0.01)
        self.slider_dict["growth_success"]  = Slider(title="Growth Rate Success",
                                                     value=tx_matrix.get("growth_success"), start = 0.5, end = 5, step = 0.01)

    def update_tx_matrix(self):
        for key, val in self.slider_dict.items():
            # if isinstance(self.slider_dict[key].value, str):
            #     self.tx_matrix[key] = int(self.slider_dict[key].value)
            self.tx_matrix[key] = self.slider_dict[key].value
        print(self.tx_matrix)
        return self.tx_matrix

    def get_sliders(self,*args):
        if args:
            return [val for key, val in self.slider_dict.items() if key in args]
        return [val for _, val in self.slider_dict.items()]
