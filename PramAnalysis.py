import os
import sys
from collections import OrderedDict

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import pandas as pd
from pprint import pprint as pp
from pram.data   import ProbeMsgMode, GroupSizeProbe, ProbePersistanceDB, ProbePersistanceMem
from pram.entity import  Group, GroupSplitSpec
from pram.rule   import Rule, TimeAlways
from pram.sim    import Simulation
pd.options.display.float_format = '{:.4f}'.format
np.set_printoptions(suppress=True)


class UserStartupGrowthRuleVersion2(Rule):
    def __init__(self, tx_matrix, t=TimeAlways(), memo=None):
        super().__init__('startup-growth', t, memo)
        # self.initial_population = tx_matrix.get("initial_population")
        self.round_seed_a = tx_matrix.get("round_seed_a")
        self.round_seed_failure = tx_matrix.get("round_seed_failure")
        self.round_a_a = tx_matrix.get("round_a_a", 0)
        self.round_a_b = tx_matrix.get("round_a_b")
        self.round_a_failure = tx_matrix.get("round_a_failure")
        self.round_b_b = tx_matrix.get("round_b_b", 0)
        self.round_b_c = tx_matrix.get("round_b_c")
        self.round_b_failure = tx_matrix.get("round_b_failure")
        self.round_c_c = tx_matrix.get("round_c_c", 0)
        self.round_c_success = tx_matrix.get("round_c_success")
        self.round_c_failure = tx_matrix.get("round_c_failure")
        self.round_success_success = tx_matrix.get("round_success_success")
        self.round_success_failure = tx_matrix.get("round_success_failure")
        self.round_failure_success = tx_matrix.get("round_failure_success")
        self.round_failure_failure = tx_matrix.get("round_failure_failure")

    def apply(self, pop, group, iter, t):

        # Transition matrix: All at seed level
        # Stage : Seed -> A -> B -> C -> Success -> Failure
        if group.has_attr({ 'stage': 'seed' }):
            return [
                GroupSplitSpec(p=   self.round_seed_failure, attr_set={ 'stage': 'failure' }),
                GroupSplitSpec(p=   self.round_seed_a ,   attr_set={ 'stage': 'a' }),
                GroupSplitSpec(p=   1 - self.round_seed_failure - self.round_seed_a,
                               attr_set={ 'stage': 'success' })
            ]
        if group.has_attr({ 'stage': 'a' }):
            return [
                GroupSplitSpec(p=self.round_a_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=self.round_a_b, attr_set={'stage': 'b'}),
                GroupSplitSpec(p=self.round_a_a, attr_set={'stage': 'a'}),
                GroupSplitSpec(p=1 - self.round_a_b - self.round_a_failure - self.round_a_a,
                               attr_set={'stage': 'success'})
            ]
        if group.has_attr({ 'stage': 'b' }):
            return [
                GroupSplitSpec(p=self.round_b_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=self.round_b_b, attr_set={'stage': 'b'}),
                GroupSplitSpec(p=self.round_b_c, attr_set={'stage': 'c'}),
                GroupSplitSpec(p=1 - self.round_b_failure - self.round_b_c - self.round_b_b,
                               attr_set={'stage': 'success'})
            ]
        if group.has_attr({ 'stage': 'c' }):
            return [
                GroupSplitSpec(p=self.round_c_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=self.round_c_c, attr_set={'stage': 'c'}),
                GroupSplitSpec(p=1 - self.round_c_failure - self.round_c_c
                               , attr_set={'stage': 'success'})
            ]
        if group.has_attr({ 'stage': 'success' }):
            return [
                GroupSplitSpec(p=self.round_success_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=1 - self.round_success_failure, attr_set={'stage': 'success'}),

            ]
        if group.has_attr({ 'stage': 'failure' }):
            return [
                GroupSplitSpec(p=self.round_failure_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=1 - self.round_failure_failure, attr_set={'stage': 'success'})
            ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr([ 'stage' ])

    # def setup(self, pop, group):
    #     return [
    #         GroupSplitSpec(p=0.5, attr_set={ 'stage': 'seed' }),
    #         GroupSplitSpec(p=0.2, attr_set={'stage': 'a'}),
    #         GroupSplitSpec(p=0.3, attr_set={'stage': 'b'})
    #     ]

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={ 'stage': 'seed' })
        ]

def analysis_Complex_version1(tx_dict= None, population = 10000, iteration = 20):

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
            round_a_a=0.4,
            round_b_b=0.3,
            round_c_c=0.3,
        )
    tx_numpy_array = np.array([])
    old_p = GroupSizeProbe.by_attr('stage', 'stage', ['seed', 'a', 'b', 'c', 'success', 'failure'],persistance=ProbePersistanceMem(),
                                   msg_mode=ProbeMsgMode.CUMUL)
    p = GroupSizeProbe.by_attr('stage', 'stage', ['seed', 'a', 'b', 'c',  'success', 'failure'],
                               persistance=ProbePersistanceDB())
    sim = (
        Simulation().
            add([
            UserStartupGrowthRuleVersion2(tx_dict),
            p,
            Group(m=population)
        ]).
            run(iteration)
    )
    print(sim.probes[0].get_msg())
    print()

    series = [
        {'var': 'p0'},
        {'var': 'p1'},
        {'var': 'p2'},
        {'var': 'p3'},
        {'var': 'p4'},
        {'var': 'p5'},
        {'var': 'n0'},
        {'var': 'n1'},
        {'var': 'n2'},
        {'var': 'n3'},
        {'var': 'n4'},
        {'var': 'n5'},
    ]
    col_names = {'n0': 'seed', 'n1': 'a', 'n2': 'b', 'n3': 'c', 'n4': 'success', 'n5': 'failure',
                  "p0" :"p_seed","p1" :"p_a","p2" :"p_b","p3" :"p_c","p4" :"p_success","p5" :"p_failure" }
    probe_data = p.probe_data(series)
    probe_frame:pd.DataFrame
    probe_frame = pd.DataFrame.from_dict(probe_data)
    probe_frame.rename(columns = col_names, inplace = True)
    probe_frame["i"] = probe_frame["i"]+1
    initial_condition = {'seed': population, 'a': 0, 'b': 0, 'c': 0, 'success': 0, 'failure': 0, 'i' : 0,
                            "p_seed":1,"p_a":0,"p_b":0,"p_c":0,"p_success":0,"p_failure":0}
    probe_frame = pd.concat([pd.DataFrame(initial_condition, index =[0]), probe_frame[:]]).reset_index(drop = True)
    probe_frame.drop(columns=['i'], inplace=True)
    print(probe_frame)
    # d = probe_frame.iloc[0]
    # print(d)
    # for chart
    plot_data = probe_frame.iloc[0]
    # probe_names = probe_frame
    print(plot_data.values)
    print(list(plot_data.index))


    # data_source = ColumnDataSource(probe_frame)
    probe_frame.to_csv("data_file.csv")
    return probe_frame

def analysis_Complex_version2(tx_dict= None, population = 100, iteration = 20):
    np.set_printoptions(suppress=True)
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
            round_a_a=0.4,
            round_b_b=0.3,
            round_c_c=0.3,
        )
        # seed = 1, a = 0, b = 0, c = 0, success = 0, failure = 0
    tx_matrix = np.array([
            [0,tx_dict['round_seed_a'], 0, 0, 1 - tx_dict['round_seed_failure']- tx_dict['round_seed_a'],
              tx_dict['round_seed_failure']],

            [0, tx_dict['round_a_a'], tx_dict['round_a_b'], 0,
             1 - tx_dict['round_a_failure'] - tx_dict['round_a_a'] - tx_dict['round_a_b'],
             tx_dict['round_a_failure']],

        [0, 0, tx_dict['round_b_b'],  tx_dict['round_b_c'],
         1 - tx_dict['round_b_failure'] - tx_dict['round_b_c'] - tx_dict['round_b_b'],
         tx_dict['round_b_failure']],

        [0, 0, 0, tx_dict['round_c_c'], 1 - tx_dict['round_c_failure'] - tx_dict['round_c_c'],
         tx_dict['round_c_failure']],

        [0, 0, 0, 0, 1 - tx_dict['round_success_failure'], tx_dict['round_success_failure']],
        [0, 0, 0, 0, 1 - tx_dict['round_failure_failure'], tx_dict['round_failure_failure']],
                        ])


    old_p = GroupSizeProbe.by_attr('stage', 'stage', ['seed', 'a', 'b', 'c', 'success', 'failure'],persistance=ProbePersistanceMem(),
                                   msg_mode=ProbeMsgMode.CUMUL)
    p = GroupSizeProbe.by_attr('stage', 'stage', ['seed', 'a', 'b', 'c',  'success', 'failure'],
                               persistance=ProbePersistanceDB())
    sim = (
        Simulation().
            add([
            UserStartupGrowthRuleVersion2(tx_dict),
            p,
            Group(m=population)
        ]).
            run(iteration)
    )
    print(sim.probes[0].get_msg())
    print()

    series = [
        {'var': 'p0'},
        {'var': 'p1'},
        {'var': 'p2'},
        {'var': 'p3'},
        {'var': 'p4'},
        {'var': 'p5'},
    ]
    col_names = {"p0" :"p_seed","p1" :"p_a","p2" :"p_b","p3" :"p_c","p4" :"p_success","p5" :"p_failure" }
    names = ["p0","p1","p2","p3","p4", "p5"]
    probe_data:dict
    probe_data = p.probe_data(series)
    probe_data_ordered = OrderedDict()

    for name in names:
        probe_data_ordered[col_names.get(name)] = probe_data.pop(name)
    # pp(probe_data_ordered)

    probe_data_frame = pd.DataFrame.from_dict(probe_data_ordered)
    pp(probe_data_frame)

    value_df = pd.DataFrame(columns=list(probe_data_ordered.keys()))
    # print(value_df)

    # proportion of investment
    investment_proportion = OrderedDict(seed = 1, a = 0, b = 0, c = 0, success = 0, failure = 0 )

    # hyper-parameters
    # stage_multiplier = {"seed": 3, "a": 5, "b": 7, "c": 5, "success": 5, "failure": 0}
    # stage_multiplier_dict = OrderedDict(seed=3, a=5, b=7, c=5, success=5, failure=0)
    stage_multiplier_list = [1, 1.1, 1.25, 1.3, 1, 0]
    # stage_multiplier_list = [1, 2, 3, 4, 5, 0]

    inital_investment_dict = OrderedDict(
        seed=population * investment_proportion.get("seed"),
        a = population * investment_proportion.get("a"),
        b = population * investment_proportion.get("b"),
        c = population * investment_proportion.get("c"),
        success = population * investment_proportion.get("success"),
        failure = population * investment_proportion.get("failure"),
    )

    sim_length = len(probe_data_ordered.get('p_a'))
    valuation_list = [population]
    for i in range(sim_length):
        # print(valuation_list[i] * probe_data_frame.iloc[[i]])
        val = valuation_list[i] * probe_data_frame.iloc[i]
        val = stage_multiplier_list * val
        valuation_list.append(np.sum(val))
        print(valuation_list)

    # print("sim_length",sim_length)
    #
    # # total_investment = sum(inital_investment)
    # print("inital_investment",inital_investment_dict)


    probe_frame: pd.DataFrame
    probe_frame = pd.DataFrame.from_dict(probe_data)
    probe_frame.rename(columns = col_names, inplace = True)

    probe_frame["i"] = probe_frame["i"]+1
    initial_condition = {'seed': population, 'a': 0, 'b': 0, 'c': 0, 'success': 0, 'failure': 0, 'i' : 0,
                            "p_seed":1,"p_a":0,"p_b":0,"p_c":0,"p_success":0,"p_failure":0}
    probe_frame = pd.concat([pd.DataFrame(initial_condition, index =[0]), probe_frame[:]]).reset_index(drop = True)
    probe_frame.drop(columns=['i'], inplace=True)
    print(probe_frame)
    # d = probe_frame.iloc[0]
    # print(d)
    # for chart
    plot_data = probe_frame.iloc[0]
    # probe_names = probe_frame
    print(plot_data.values)
    print(list(plot_data.index))


    # data_source = ColumnDataSource(probe_frame)
    probe_frame.to_csv("data_file.csv")
    return probe_frame

def get_stochastic_multiplier(param = [1, 1.5, 2, 1.5, 1.1, 0]):
    stage_multiplier_list = [np.random.normal(param[0], 0.1 * param[0]),
                             np.random.normal(param[1], 0.1 * param[1]),
                             np.random.normal(param[2], 0.1 * param[2]),
                             np.random.normal(param[3], 0.1 * param[3]),
                             np.random.normal(param[4], 0.1 * param[4]),
                             np.random.normal(param[5], 0.1 * param[5])
                             ]
    return stage_multiplier_list

def analysis_Complex(tx_dict= None, population = 100, iteration = 20):
    np.set_printoptions(suppress=True)
    if tx_dict is None:
        tx_dict = OrderedDict(
            initial_population=100,
            invest_val=1000,
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
        if population is None:
            population = tx_dict.get("initial_population")
        # hyper-parameters
        # stage_multiplier = {"seed": 3, "a": 5, "b": 7, "c": 5, "success": 5, "failure": 0}
        # stage_multiplier_dict = OrderedDict(seed=3, a=5, b=7, c=5, success=5, failure=0)
        # stage_multiplier_list = [1, 1.1, 1.25, 1.3, 1, 0]
        # stage_multiplier_list = [1, 2, 3, 4, 5, 0]
        # stage_multiplier_list = [1, 1.8, 2.2, 2.5, 1.2, 0]
        # stage_multiplier_list = [1, 2, 2.5, 2, 1, 0]
        stage_multiplier_list = [1, 1.8, 2.2, 2.5, 1.2, 0]
        init_inv_list = np.array([100, 300, 600, 0, 0, 0])
        # seed = 1, a = 0, b = 0, c = 0, success = 0, failure = 0
    # # Normalizing probabilities
    if (1 - tx_dict['round_seed_failure'] - tx_dict['round_seed_a']) < 0:
        tx_dict['round_seed_a'] = 1 - tx_dict['round_seed_failure']

    if (1 - tx_dict['round_a_failure'] - tx_dict['round_a_a'] - tx_dict['round_a_b']) < 0:
        tx_dict['round_a_b'] = 1 - tx_dict['round_a_failure']
        tx_dict['round_a_a'] = 0

    if (1 - tx_dict['round_b_failure'] - tx_dict['round_b_c'] - tx_dict['round_b_b']) < 0:
        tx_dict['round_b_c'] = 1 - tx_dict['round_b_failure']
        tx_dict['round_b_b'] = 0

    if (1 - tx_dict['round_c_failure'] - tx_dict['round_c_c']) < 0:
        tx_dict['round_c_c'] = 1 - tx_dict['round_c_failure']

        # Normalizing probabilities
        # if (1 - tx_dict['round_seed_failure'] - tx_dict['round_seed_a']) < 0:
        #     tx_dict['round_seed_failure'] = tx_dict['round_seed_failure'] / (
        #                 tx_dict['round_seed_failure'] + tx_dict['round_seed_a'])
        #     tx_dict['round_seed_a'] = tx_dict['round_seed_a'] / (
        #                 tx_dict['round_seed_failure'] + tx_dict['round_seed_a'])
        #
        # if (1 - tx_dict['round_a_failure'] - tx_dict['round_a_a'] - tx_dict['round_a_b']) < 0:
        #     tx_dict['round_a_failure'] = tx_dict['round_a_failure'] / (
        #                 tx_dict['round_a_failure'] + tx_dict['round_a_a'] + tx_dict['round_a_b'])
        #     tx_dict['round_a_a'] = tx_dict['round_a_a'] / (
        #                 tx_dict['round_a_failure'] + tx_dict['round_a_a'] + tx_dict['round_a_b'])
        #     tx_dict['round_a_b'] = tx_dict['round_a_b'] / (
        #                 tx_dict['round_a_failure'] + tx_dict['round_a_a'] + tx_dict['round_a_b'])
        #
        # if (1 - tx_dict['round_b_failure'] - tx_dict['round_b_c'] - tx_dict['round_b_b']) < 0:
        #     tx_dict['round_b_failure'] = tx_dict['round_b_failure'] / (
        #                 tx_dict['round_b_failure'] + tx_dict['round_b_c'] + tx_dict['round_b_b'])
        #     tx_dict['round_b_c'] = tx_dict['round_b_c'] / (
        #                 tx_dict['round_b_failure'] + tx_dict['round_b_c'] + tx_dict['round_b_b'])
        #     tx_dict['round_b_b'] = tx_dict['round_b_b'] / (
        #                 tx_dict['round_b_failure'] + tx_dict['round_b_c'] + tx_dict['round_b_b'])
        #
        # if (1 - tx_dict['round_c_failure'] - tx_dict['round_c_c']) < 0:
        #     tx_dict['round_c_failure'] = tx_dict['round_c_failure'] / (
        #                 tx_dict['round_c_failure'] + tx_dict['round_c_c'])
        #     tx_dict['round_c_c'] = tx_dict['round_c_c'] / (tx_dict['round_c_failure'] + tx_dict['round_c_c'])

    tx_matrix = np.array([
            [0,tx_dict['round_seed_a'], 0, 0, 1 - tx_dict['round_seed_failure']- tx_dict['round_seed_a'],
              tx_dict['round_seed_failure']],

            [0, tx_dict['round_a_a'], tx_dict['round_a_b'], 0,
             1 - tx_dict['round_a_failure'] - tx_dict['round_a_a'] - tx_dict['round_a_b'],
             tx_dict['round_a_failure']],

        [0, 0, tx_dict['round_b_b'],  tx_dict['round_b_c'],
         1 - tx_dict['round_b_failure'] - tx_dict['round_b_c'] - tx_dict['round_b_b'],
         tx_dict['round_b_failure']],

        [0, 0, 0, tx_dict['round_c_c'], 1 - tx_dict['round_c_failure'] - tx_dict['round_c_c'],
         tx_dict['round_c_failure']],

        [0, 0, 0, 0, 1 - tx_dict['round_success_failure'], tx_dict['round_success_failure']],
        [0, 0, 0, 0, 1 - tx_dict['round_failure_failure'], tx_dict['round_failure_failure']],
                        ])

    investment_proportion = OrderedDict(seed = 1, a = 0, b = 0, c = 0, success = 0, failure = 0 )

    stage_multiplier_list = [1, tx_dict.get("growth_a"), tx_dict.get("growth_b"),
                             tx_dict.get("growth_c"), tx_dict.get("growth_success"), 0 ]
    init_inv_list = np.array([tx_dict.get("invest_val") or 1000, 0, 0, 0, 0, 0])
    init_inv_list_population = np.array([tx_dict.get("initial_population") or 100, 0, 0, 0, 0, 0])
    # print("init_inv_list",init_inv_list)
    value = [population]
    # print(tx_matrix)
    # print(tx_matrix.shape)

    ad_value    = np.array(init_inv_list)
    ad_mass     = np.array(init_inv_list_population)
    population_per_group = np.empty(shape=(6,))
    ad_stage_multiplier_list = np.array(stage_multiplier_list)

    for i in range(iteration):
        # #todo costly operation needs to optimize
        init_inv_list = np.matmul(tx_matrix.T, init_inv_list)
        # #todo costly operation needs to optimize
        init_inv_list_population = np.matmul(tx_matrix.T, init_inv_list_population)
        print(init_inv_list_population)
        # print(50*'=')
        # init_inv_list = ad_stage_multiplier_list * init_inv_list

        # mul = get_stochastic_multiplier(stage_multiplier_list)
        mul = stage_multiplier_list
        init_inv_list = mul * init_inv_list
        # print(init_inv_list)
        ad_value = np.vstack([ad_value,init_inv_list])
        ad_mass = np.vstack([ad_mass, init_inv_list_population])

        # ad_value = np.vstack([ad_value,init_inv_list, temp])
    # print("final")
    # print(ad_value.shape)
    ad_mass = np.around(ad_mass, decimals=2)
    ad_value = np.around(ad_value, decimals=2)
    annual_valuation = np.sum(ad_value, axis=1)
    # print(np.sum(ad_value, axis=1))
    cols = ["seed", "a", "b", "c", "success", "failure"]
    final_valuation_frame = pd.DataFrame(ad_value, columns=cols)
    final_mass_frame = pd.DataFrame(ad_mass, columns= cols)

    # final_valuation_frame['year'] = final_valuation_frame.index
    print(final_mass_frame)
    return final_valuation_frame, final_mass_frame

def analysis_complex_montecarlo(sim = 1000):
    pass






    # probe_frame: pd.DataFrame
    # probe_frame = pd.DataFrame.from_dict(probe_data)
    # probe_frame.rename(columns = col_names, inplace = True)

    # probe_frame["i"] = probe_frame["i"]+1
    # initial_condition = {'seed': population, 'a': 0, 'b': 0, 'c': 0, 'success': 0, 'failure': 0, 'i' : 0,
    #                         "p_seed":1,"p_a":0,"p_b":0,"p_c":0,"p_success":0,"p_failure":0}
    # probe_frame = pd.concat([pd.DataFrame(initial_condition, index =[0]), probe_frame[:]]).reset_index(drop = True)
    # probe_frame.drop(columns=['i'], inplace=True)
    # print(probe_frame)
    # # d = probe_frame.iloc[0]
    # # print(d)
    # # for chart
    # plot_data = probe_frame.iloc[0]
    # # probe_names = probe_frame
    # print(plot_data.values)
    # print(list(plot_data.index))
    #
    #
    # # data_source = ColumnDataSource(probe_frame)
    # probe_frame.to_csv("data_file.csv")
    # return probe_frame



class UserStartupGrowthRule(Rule):
    def __init__(self, tx_matrix, t=TimeAlways(), memo=None):
        super().__init__('startup-growth', t, memo)
        # self.initial_population = tx_matrix.get("initial_population")
        self.round_seed_a = tx_matrix.get("round_seed_a")
        self.round_seed_failure = tx_matrix.get("round_seed_failure")
        self.round_a_b = tx_matrix.get("round_a_b")
        self.round_a_failure = tx_matrix.get("round_a_failure")
        self.round_b_c = tx_matrix.get("round_b_c")
        self.round_b_failure = tx_matrix.get("round_b_failure")
        self.round_c_success = tx_matrix.get("round_c_success")
        self.round_c_failure = tx_matrix.get("round_c_failure")
        self.round_success_success = tx_matrix.get("round_success_success")
        self.round_success_failure = tx_matrix.get("round_success_failure")
        self.round_failure_success = tx_matrix.get("round_failure_success")
        self.round_failure_failure = tx_matrix.get("round_failure_failure")

    def apply(self, pop, group, iter, t):

        # Transition matrix: All at seed level
        # Stage : Seed -> A -> B -> C -> Success -> Failure
        if group.has_attr({ 'stage': 'seed' }):
            return [
                GroupSplitSpec(p=   self.round_seed_failure, attr_set={ 'stage': 'failure' }),
                GroupSplitSpec(p=   self.round_seed_a ,   attr_set={ 'stage': 'a' }),
                GroupSplitSpec(p=   1 - self.round_seed_failure - self.round_seed_a,
                               attr_set={ 'stage': 'success' })
            ]
        if group.has_attr({ 'stage': 'a' }):
            return [
                GroupSplitSpec(p=self.round_a_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=self.round_a_b, attr_set={'stage': 'b'}),
                GroupSplitSpec(p=1 - self.round_a_b - self.round_a_failure,
                               attr_set={'stage': 'success'})
            ]
        if group.has_attr({ 'stage': 'b' }):
            return [
                GroupSplitSpec(p=self.round_b_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=self.round_b_c, attr_set={'stage': 'c'}),
                GroupSplitSpec(p=1 - self.round_b_failure - self.round_b_c,
                               attr_set={'stage': 'success'})
            ]
        if group.has_attr({ 'stage': 'c' }):
            return [
                GroupSplitSpec(p=self.round_c_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=1 - self.round_c_failure, attr_set={'stage': 'success'})
            ]
        if group.has_attr({ 'stage': 'success' }):
            return [
                GroupSplitSpec(p=self.round_success_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=1 - self.round_success_failure, attr_set={'stage': 'success'}),

            ]
        if group.has_attr({ 'stage': 'failure' }):
            return [
                GroupSplitSpec(p=self.round_failure_failure, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=1 - self.round_failure_failure, attr_set={'stage': 'success'})
            ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr([ 'stage' ])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={ 'stage': 'seed' })
        ]

def analysis_simple(tx_dict= None, population = 10000, iteration = 16):

    if tx_dict is None:
        tx_dict = dict(
            round_seed_a=0.3,
            round_seed_failure=0.67,
            round_a_b=0.2,
            round_a_failure=0.6,
            round_b_c=0.3,
            round_b_failure=0.4,
            round_c_success=0.5,
            round_c_failure=0.5,
            round_success_success=1,
            round_success_failure=0,
            round_failure_success=0,
            round_failure_failure=1,
            # round_a_a=0.2,
            # round_b_b=0.2,
            # round_c_c=0.2,
        )
    old_p = GroupSizeProbe.by_attr('stage', 'stage', ['seed', 'a', 'b', 'c', 'success', 'failure'],persistance=ProbePersistanceMem(),
                                   msg_mode=ProbeMsgMode.CUMUL)
    p = GroupSizeProbe.by_attr('stage', 'stage', ['seed', 'a', 'b', 'c',  'success', 'failure'],
                               persistance=ProbePersistanceDB())
    sim = (
        Simulation().
            add([
            UserStartupGrowthRule(tx_dict),
            p,
            Group(m=population)
        ]).
            run(iteration)
    )
    series = [
        {'var': 'n0'},
        {'var': 'n1'},
        {'var': 'n2'},
        {'var': 'n3'},
        {'var': 'n4'},
        {'var': 'n5'},
    ]
    col_names = {'n0': 'seed', 'n1': 'a', 'n2': 'b', 'n3': 'c', 'n4': 'success', 'n5': 'failure'}
    probe_data = p.probe_data(series)
    probe_frame:pd.DataFrame
    probe_frame = pd.DataFrame.from_dict(probe_data)
    probe_frame.rename(columns = col_names, inplace = True)
    probe_frame["i"] = probe_frame["i"]+1
    initial_condition = {'seed': population, 'a': 0, 'b': 0, 'c': 0, 'success': 0, 'failure': 0, 'i' : 0}
    probe_frame = pd.concat([pd.DataFrame(initial_condition, index =[0]), probe_frame[:]]).reset_index(drop = True)
    probe_frame.drop(columns=['i'], inplace=True)
    print(probe_frame)
    d = probe_frame.iloc[0]
    print(d)
    # for chart
    plot_data = probe_frame.iloc[0]
    # probe_names = probe_frame
    print(plot_data.values)
    print(list(plot_data.index))

    # data_source = ColumnDataSource(probe_frame)

    return probe_frame

if __name__ == "__main__":
    print("Running Simulations........")
    # analysis_simple()
    analysis_Complex()