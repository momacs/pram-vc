from pram.rule import Sequence, DifferenceEquation, TimeAlways, Rule, FibonacciSeq  # , FibonacciSeq
from pram.sim import Simulation
from pram.entity import Group, GroupQry, GroupSplitSpec, Site

from pprint import pprint as pp
from pram.data import ProbeMsgMode, GroupSizeProbe, ProbePersistanceDB, ProbePersistanceMem
from pram.entity import Group, GroupSplitSpec
from pram.rule import Rule, TimeAlways
from pram.sim import Simulation


class Sample(Rule):

    def __init__(self, t=TimeAlways(), memo=None):
        super().__init__('startup-growth', t, memo)

    def apply(self, pop, group, iter, t):
        if group.has_attr({'stage': 'c'}):
            return [
                GroupSplitSpec(p=0.3, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=0.4, attr_set={'stage': 'c'}),
                GroupSplitSpec(p=0.3, attr_set={'stage': 'success'})
            ]
        if group.has_attr({'stage': 'success'}):
            return [
                GroupSplitSpec(p=0.1, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=0.2, attr_set={'stage': 'c'}),
                GroupSplitSpec(p=0.7, attr_set={'stage': 'success'}),

            ]
        if group.has_attr({'stage': 'failure'}):
            return [
                GroupSplitSpec(p=0.75, attr_set={'stage': 'failure'}),
                GroupSplitSpec(p=0.2, attr_set={'stage': 'c'}),
                GroupSplitSpec(p=0.05, attr_set={'stage': 'success'})
            ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr(['stage'])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={'stage': 'c'})
        ]


class SimpleMultiplyCombined(Rule):

    def __init__(self, t=TimeAlways(), memo=None):
        super().__init__('startup-growth', t, memo)

    def apply(self, pop, group, iter, t):
        if group.has_attr({'stage': 'c'}):
            c_value = group.get_attr("value") or 0
            # print("c_value is ",c_value)
            return [
                GroupSplitSpec(p=0.3, attr_set={'stage': 'failure', 'value': 0 * c_value}),
                GroupSplitSpec(p=0.4, attr_set={'stage': 'c', 'value': 2 * c_value}),
                GroupSplitSpec(p=0.3, attr_set={'stage': 'success', 'value': 1.5 * c_value})
            ]
        if group.has_attr({'stage': 'success'}):
            success_value = group.get_attr("value") or 0
            return [
                GroupSplitSpec(p=0.1, attr_set={'stage': 'failure', 'value': 0 * success_value}),
                GroupSplitSpec(p=0.2, attr_set={'stage': 'c', 'value': 2 * success_value}),
                GroupSplitSpec(p=0.7, attr_set={'stage': 'success', 'value': 1.5 * success_value}),

            ]
        if group.has_attr({'stage': 'failure'}):
            failure_value = group.get_attr("value") or 0
            return [
                GroupSplitSpec(p=0.75, attr_set={'stage': 'failure', 'value': 0 * failure_value}),
                GroupSplitSpec(p=0.2, attr_set={'stage': 'c', 'value': 2 * failure_value}),
                GroupSplitSpec(p=0.05, attr_set={'stage': 'success', 'value': 1.5 * failure_value})
            ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr(['stage']) and group.has_attr(['value'])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={'stage': 'c', "value": 1000})
        ]


class SimpleMultiplyMain(Rule):

    def __init__(self, t=TimeAlways(), memo=None):
        super().__init__('valuation', t, memo)

    def apply(self, pop, group, iter, t):
        if group.has_attr({'stage': 'c'}):
            c_value = group.get_attr("value") or 0

            return [
                GroupSplitSpec(p=0.3, attr_set={'value': 0 * c_value}),
                GroupSplitSpec(p=0.4, attr_set={'value': 2 * c_value}),
                GroupSplitSpec(p=0.3, attr_set={'value': 1.5 * c_value})
            ]
        if group.has_attr({'stage': 'success'}):
            success_value = group.get_attr("value") or 0
            return [
                GroupSplitSpec(p=0.1, attr_set={'value': 0 * success_value}),
                GroupSplitSpec(p=0.2, attr_set={'value': 2 * success_value}),
                GroupSplitSpec(p=0.7, attr_set={'value': 1.5 * success_value}),

            ]
        if group.has_attr({'stage': 'failure'}):
            failure_value = group.get_attr("value") or 0
            return [
                GroupSplitSpec(p=0.75, attr_set={'value': 0 * failure_value}),
                GroupSplitSpec(p=0.2, attr_set={'value': 2 * failure_value}),
                GroupSplitSpec(p=0.05, attr_set={'value': 1.5 * failure_value})
            ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr(['stage', 'value'])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={"value": 1000})
        ]


old_p = GroupSizeProbe.by_attr('stage', 'stage', ['c', 'success', 'failure'], persistance=ProbePersistanceMem(),
                               msg_mode=ProbeMsgMode.CUMUL)

probe2 = GroupSizeProbe.by_attr("value", "value", ['c', 'success', 'failure'], persistance=ProbePersistanceMem(),
                                msg_mode=ProbeMsgMode.DISP)

# c_group = Group(name="c", m = 100, attr = {"stage" : "c", "value": 1000})
# success_group = Group(name="success", m = 100, attr ={"stage":"success", "value" : 1000})
# failure_group = Group(name="failure", m = 100, attr = {"stage": "failure", "value" : 1000})

c_group = Group(name="c", m=100, attr={"stage": "c"})
success_group = Group(name="success", m=100, attr={"stage": "success"})
failure_group = Group(name="failure", m=100, attr={"stage": "failure"})

sim = (
    Simulation().
        add([
        SimpleMultiplyCombined(),
        old_p,
        probe2,
        c_group, success_group, failure_group
    ]).
        run(10)
)

print(sim.probes[0].get_msg())
print(sim.probes[1].get_msg())
print()
