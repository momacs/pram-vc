import os,sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


from pram.data   import ProbeMsgMode, GroupSizeProbe
from pram.entity import  Group, GroupQry, GroupSplitSpec
from pram.rule   import Rule, TimeAlways
from pram.sim    import Simulation

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
class StartupGrowthRule(Rule):
    def __init__(self, t=TimeAlways(), memo=None):
        super().__init__('startup-growth', t, memo)

    def apply(self, pop, group, iter, t):

        # Transition matrix: All at seed level

        #	    se	a	b	c	ss		ff
        # se	0	0.3	0	0	0.03	0.67
        # a	    0	0	0.2	0	0.2		0.6
        # b	    0	0	0	0.3	0.3		0.4
        # c	    0	0	0	0	0.5		0.5
        # ss	0	0	0	0	1		0
        # ff	0	0	0	0	0		1

        # Stage : Seed -> A -> B -> C -> Success -> Failure
        # Success is IPO or acquisition
        # Failure is investment = 0

        p_success = 0.03  # prob of success
        p_next = 0.3


        if group.has_attr({ 'stage': 's' }):
            return [
                GroupSplitSpec(p=1 - p_success - p_next, attr_set={ 'stage': 'failure' }),
                GroupSplitSpec(p= p_next  ,   attr_set={ 'stage': 'a' }),
                GroupSplitSpec(p=p_success,  attr_set={ 'stage': 'success' })
            ]
        if group.has_attr({ 'stage': 'a' }):
            return [
                GroupSplitSpec(p=0.20, attr_set={ 'stage': 'b' }),
                GroupSplitSpec(p=0.20, attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=0.60, attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'b' }):
            return [
                GroupSplitSpec(p=0.30, attr_set={ 'stage': 'c' }),
                GroupSplitSpec(p=0.30, attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=0.40, attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'c' }):
            return [
                GroupSplitSpec(p=0.50, attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=0.50, attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'success' }):
            return [
                GroupSplitSpec(p=1, attr_set={ 'stage': 'success' }),
            ]
        if group.has_attr({ 'stage': 'failure' }):
            return [
                GroupSplitSpec(p=1, attr_set={ 'stage': 'failure' })
            ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr([ 'stage' ])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={ 'stage': 's' })
        ]


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
class StartupLocationRule(Rule):
    def __init__(self, t=TimeAlways(), memo=None):
        super().__init__('startup-location', t, memo)



    def apply(self, pop, group, iter, t):
        if group.has_attr({ 'location': 'usa' }):

            #	USA
            #		se		a		b		c		ss		ff
            #	se	0.00	0.35	0.00	0.00	0.07	0.58
            #	a	0.00	0.00	0.30	0.00	0.25	0.45
            #	b	0.00	0.00	0.00	0.45	0.30	0.25
            #	c	0.00	0.00	0.00	0.00	0.70	0.30
            #	ss	0.00	0.00	0.00	0.00	1.00	0.00
            #	ff	0.00	0.00	0.00	0.00	0.00	1.00
            #

            #
            #	Others
            #		se		a		b		c		ss		ff
            #	se	0.00	0.25	0.00	0.00	0.02	0.73
            #	a	0.00	0.00	0.17	0.00	0.17	0.66
            #	b	0.00	0.00	0.00	0.25	0.27	0.48
            #	c	0.00	0.00	0.00	0.00	0.40	0.60
            #	ss	0.00	0.00	0.00	0.00	1.00	0.00
            #	ff	0.00	0.00	0.00	0.00	0.00	1.00

            p_success = 0.07  # prob of success
            p_next = 0.35

            if group.has_attr({'stage': 's'}):
                return [
                    GroupSplitSpec(p=1 - p_success - p_next, attr_set={'stage': 'failure'}),
                    GroupSplitSpec(p=p_next, attr_set={'stage': 'a'}),
                    GroupSplitSpec(p=p_success, attr_set={'stage': 'success'})
                ]
            if group.has_attr({'stage': 'a'}):
                return [
                    GroupSplitSpec(p=0.30, attr_set={'stage': 'b'}),
                    GroupSplitSpec(p=0.25, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.45, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'b'}):
                return [
                    GroupSplitSpec(p=0.45, attr_set={'stage': 'c'}),
                    GroupSplitSpec(p=0.30, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.25, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'c'}):
                return [
                    GroupSplitSpec(p=0.7, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.3, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'success'}):
                return [
                    GroupSplitSpec(p=1, attr_set={'stage': 'success'}),
                ]
            if group.has_attr({'stage': 'failure'}):
                return [
                    GroupSplitSpec(p=1, attr_set={'stage': 'failure'})
                ]

        # Other location:
        if group.has_attr({ 'location': 'others' }):

            p_success = 0.02  # prob of success
            p_next = 0.25

            if group.has_attr({'stage': 's'}):
                return [
                    GroupSplitSpec(p=1 - p_success - p_next, attr_set={'stage': 'failure'}),
                    GroupSplitSpec(p=p_next, attr_set={'stage': 'a'}),
                    GroupSplitSpec(p=p_success, attr_set={'stage': 'success'})
                ]
            if group.has_attr({'stage': 'a'}):
                return [
                    GroupSplitSpec(p=0.17, attr_set={'stage': 'b'}),
                    GroupSplitSpec(p=0.17, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.66, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'b'}):
                return [
                    GroupSplitSpec(p=0.25, attr_set={'stage': 'c'}),
                    GroupSplitSpec(p=0.27, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.48, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'c'}):
                return [
                    GroupSplitSpec(p=0.40, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.60, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'success'}):
                return [
                    GroupSplitSpec(p=1, attr_set={'stage': 'success'}),
                ]
            if group.has_attr({'stage': 'failure'}):
                return [
                    GroupSplitSpec(p=1, attr_set={'stage': 'failure'})
                ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr([ 'stage', 'location' ])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={ 'stage': 's' })
        ]


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
class StartupLocationRevivalRule(Rule):
    def __init__(self, t=TimeAlways(), memo=None):
        super().__init__('startup-location', t, memo)



    def apply(self, pop, group, iter, t):
        if group.has_attr({ 'location': 'usa' }):

            #	USA
            #		se		a		b		c		ss		ff
            #	se	0.00	0.35	0.00	0.00	0.07	0.58
            #	a	0.00	0.00	0.30	0.00	0.25	0.45
            #	b	0.00	0.00	0.00	0.45	0.30	0.25
            #	c	0.00	0.00	0.00	0.00	0.70	0.30
            #	ss	0.00	0.00	0.00	0.00	0.90	0.10
            #	ff	0.00	0.00	0.00	0.00	0.15	0.85
            #

            #
            #	Others
            #		se		a		b		c		ss		ff
            #	se	0.00	0.25	0.00	0.00	0.02	0.73
            #	a	0.00	0.00	0.17	0.00	0.17	0.66
            #	b	0.00	0.00	0.00	0.25	0.27	0.48
            #	c	0.00	0.00	0.00	0.00	0.40	0.60
            #	ss	0.00	0.00	0.00	0.00	0.90	0.10
            #	ff	0.00	0.00	0.00	0.00	0.05	0.95

            p_success = 0.07  # prob of success
            p_next = 0.35

            if group.has_attr({'stage': 's'}):
                return [
                    GroupSplitSpec(p=1 - p_success - p_next, attr_set={'stage': 'failure'}),
                    GroupSplitSpec(p=p_next, attr_set={'stage': 'a'}),
                    GroupSplitSpec(p=p_success, attr_set={'stage': 'success'})
                ]
            if group.has_attr({'stage': 'a'}):
                return [
                    GroupSplitSpec(p=0.30, attr_set={'stage': 'b'}),
                    GroupSplitSpec(p=0.25, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.45, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'b'}):
                return [
                    GroupSplitSpec(p=0.45, attr_set={'stage': 'c'}),
                    GroupSplitSpec(p=0.30, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.25, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'c'}):
                return [
                    GroupSplitSpec(p=0.7, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.3, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'success'}):
                return [
                    GroupSplitSpec(p=0.90, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.10, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'failure'}):
                return [
                    GroupSplitSpec(p=0.15, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.85, attr_set={'stage': 'failure'})
                ]

        # Other location:
        if group.has_attr({ 'location': 'others' }):

            p_success = 0.02  # prob of success
            p_next = 0.25

            if group.has_attr({'stage': 's'}):
                return [
                    GroupSplitSpec(p=1 - p_success - p_next, attr_set={'stage': 'failure'}),
                    GroupSplitSpec(p=p_next, attr_set={'stage': 'a'}),
                    GroupSplitSpec(p=p_success, attr_set={'stage': 'success'})
                ]
            if group.has_attr({'stage': 'a'}):
                return [
                    GroupSplitSpec(p=0.17, attr_set={'stage': 'b'}),
                    GroupSplitSpec(p=0.17, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.66, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'b'}):
                return [
                    GroupSplitSpec(p=0.25, attr_set={'stage': 'c'}),
                    GroupSplitSpec(p=0.27, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.48, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'c'}):
                return [
                    GroupSplitSpec(p=0.40, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.60, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'success'}):
                return [
                    GroupSplitSpec(p=0.90, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.10, attr_set={'stage': 'failure'})
                ]
            if group.has_attr({'stage': 'failure'}):
                return [
                    GroupSplitSpec(p=0.05, attr_set={'stage': 'success'}),
                    GroupSplitSpec(p=0.95, attr_set={'stage': 'failure'})
                ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr([ 'stage', 'location' ])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={ 'stage': 's' })
        ]


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------

class StochasticStartupGrowthRule(Rule):
    def __init__(self, t=TimeAlways(), memo=None):
        super().__init__('startup-growth', t, memo)

    def apply(self, pop, group, iter, t):

        # Transition matrix: All at seed level

        #	    se	a	b	c	ss		ff
        # se	0	0.3	0	0	0.03	0.67
        # a	    0	0	0.2	0	0.2		0.6
        # b	    0	0	0	0.3	0.3		0.4
        # c	    0	0	0	0	0.5		0.5
        # ss	0	0	0	0	1		0
        # ff	0	0	0	0	0		1

        # Stage : Seed -> A -> B -> C -> Success -> Failure
        # Success is IPO or acquisition
        # Failure is investment = 0

        p_s_a   = np.random.uniform(0.2, 0.4)
        p_s_ss  = np.random.uniform(0.01, 0.1)
        p_a_b   = np.random.uniform(0.1, 0.4)
        p_a_ss  = np.random.uniform(0.1, 0.4)
        p_b_c   = np.random.uniform(0.2, 0.49)
        p_b_ss  = np.random.uniform(0.2, 0.49)
        p_c_ss  = np.random.uniform(0.3, 0.7)

        # psea,psess,pseff,pab,pass,paff,pbc,pbss,pbff,pcss,pcff

        if group.has_attr({ 'stage': 's' }):
            return [

                GroupSplitSpec(p= p_s_a                 , attr_set={ 'stage': 'a' }),
                GroupSplitSpec(p=p_s_ss                 , attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=1 - p_s_a - p_s_ss     , attr_set={'stage': 'failure'}),
            ]
        if group.has_attr({ 'stage': 'a' }):
            return [
                GroupSplitSpec(p=p_a_b                  , attr_set={ 'stage': 'b' }),
                GroupSplitSpec(p=p_a_ss                 , attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=1 - p_a_ss - p_a_b     , attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'b' }):
            return [
                GroupSplitSpec(p=p_b_c                  , attr_set={ 'stage': 'c' }),
                GroupSplitSpec(p=p_b_ss                 , attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=1 - p_b_c - p_b_ss     , attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'c' }):
            return [
                GroupSplitSpec(p= p_c_ss                , attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p= 1 - p_c_ss            , attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'success' }):
            return [
                GroupSplitSpec(p=1                      , attr_set={ 'stage': 'success' }),
            ]
        if group.has_attr({ 'stage': 'failure' }):
            return [
                GroupSplitSpec(p=1                      , attr_set={ 'stage': 'failure' })
            ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr([ 'stage' ])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={ 'stage': 's' })
        ]

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------

class StochasticStartupGrowthRevivalRule(Rule):
    def __init__(self, t=TimeAlways(), memo=None):
        super().__init__('startup-growth', t, memo)

    def apply(self, pop, group, iter, t):

        # Transition matrix: All at seed level

        #	    se	a	b	c	ss		ff
        # se	0	0.3	0	0	0.03	0.67
        # a	    0	0	0.2	0	0.2		0.6
        # b	    0	0	0	0.3	0.3		0.4
        # c	    0	0	0	0	0.5		0.5
        # ss	0	0	0	0	1		0
        # ff	0	0	0	0	0		1

        # Stage : Seed -> A -> B -> C -> Success -> Failure
        # Success is IPO or acquisition
        # Failure is investment = 0

        p_s_a   = np.random.uniform(0.2, 0.4)
        p_s_ss  = np.random.uniform(0.01, 0.1)
        p_a_b   = np.random.uniform(0.1, 0.4)
        p_a_ss  = np.random.uniform(0.1, 0.4)
        p_b_c   = np.random.uniform(0.2, 0.49)
        p_b_ss  = np.random.uniform(0.2, 0.49)
        p_c_ss  = np.random.uniform(0.3, 0.7)
        p_ss_ss = np.random.uniform(0.90, 1.0)
        p_ff_ss = np.random.uniform(0.01, 0.05)
        # psea,psess,pseff,pab,pass,paff,pbc,pbss,pbff,pcss,pcff

        if group.has_attr({ 'stage': 's' }):
            return [

                GroupSplitSpec(p= p_s_a                 , attr_set={ 'stage': 'a' }),
                GroupSplitSpec(p=p_s_ss                 , attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=1 - p_s_a - p_s_ss     , attr_set={'stage': 'failure'}),
            ]
        if group.has_attr({ 'stage': 'a' }):
            return [
                GroupSplitSpec(p=p_a_b                  , attr_set={ 'stage': 'b' }),
                GroupSplitSpec(p=p_a_ss                 , attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=1 - p_a_ss - p_a_b     , attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'b' }):
            return [
                GroupSplitSpec(p=p_b_c                  , attr_set={ 'stage': 'c' }),
                GroupSplitSpec(p=p_b_ss                 , attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p=1 - p_b_c - p_b_ss     , attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'c' }):
            return [
                GroupSplitSpec(p= p_c_ss                , attr_set={ 'stage': 'success' }),
                GroupSplitSpec(p= 1 - p_c_ss            , attr_set={ 'stage': 'failure' })
            ]
        if group.has_attr({ 'stage': 'success' }):
            return [
                GroupSplitSpec(p=p_ss_ss                , attr_set={'stage': 'success'}),
                GroupSplitSpec(p=1 - p_ss_ss            , attr_set={'stage': 'failure'})
            ]
        if group.has_attr({ 'stage': 'failure' }):
            return [
                GroupSplitSpec(p=p_ff_ss                , attr_set={'stage': 'success'}),
                GroupSplitSpec(p=1 - p_ff_ss            , attr_set={'stage': 'failure'})
            ]

    def is_applicable(self, group, iter, t):
        return super().is_applicable(group, iter, t) and group.has_attr([ 'stage' ])

    def setup(self, pop, group):
        return [
            GroupSplitSpec(p=1.0, attr_set={ 'stage': 's' })
        ]

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    i = 1
    eq = 50
    print(eq*"=","starting sim {}".format(i),eq*"=")
    sim = (
        Simulation().
        add([
            StartupGrowthRule(),
            GroupSizeProbe.by_attr('stage', 'stage', ['s', 'a', 'b', 'c', 'success', 'failure'], msg_mode=ProbeMsgMode.CUMUL),
            Group(m=10000)
        ]).
        run(10)
    )
    print(sim.probes[0].get_msg())
    print()

    i += 1
    print(eq * "=", "starting sim {}".format(i), eq * "=")
    sim = (
        Simulation().
            add([
            StartupLocationRule(),
            GroupSizeProbe(
                'startup-location',
                [
                    GroupQry(attr={'location': 'usa', 'stage': 'success'}),
                    GroupQry(attr={'location': 'usa', 'stage': 'failure'}),
                    GroupQry(attr={'location': 'others', 'stage': 'success'}),
                    GroupQry(attr={'location': 'others', 'stage': 'failure'}),
                ],
                msg_mode=ProbeMsgMode.CUMUL,
            ),
            Group(m=10000, attr={'location': 'usa'}),
            Group(m=10000, attr={'location': 'others'})
        ]).
            run(10)
    )
    print(sim.probes[0].get_msg())
    print()

    i += 1
    print(eq * "=", "starting sim {}".format(i), eq * "=")
    sim = (
        Simulation().
            add([
            StartupLocationRevivalRule(),
            GroupSizeProbe(
                'startup-location',
                [
                    GroupQry(attr={'location': 'usa', 'stage': 'success'}),
                    GroupQry(attr={'location': 'usa', 'stage': 'failure'}),
                    GroupQry(attr={'location': 'others', 'stage': 'success'}),
                    GroupQry(attr={'location': 'others', 'stage': 'failure'}),
                ],
                msg_mode=ProbeMsgMode.CUMUL,
            ),
            Group(m=10000, attr={'location': 'usa'}),
            Group(m=10000, attr={'location': 'others'})
        ]).
            run(20)
    )
    print(sim.probes[0].get_msg())
    print()


    i += 1
    print(eq * "=", "starting sim {}".format(i), eq * "=")
    sim = (
        Simulation().
            add([
            StochasticStartupGrowthRule(),
            GroupSizeProbe.by_attr('stage', 'stage', ['s', 'a', 'b', 'c', 'success', 'failure'],
                                   msg_mode=ProbeMsgMode.CUMUL),
            Group(m=10000)
        ]).
            run(50)
    )
    print(sim.probes[0].get_msg())
    print()

    i += 1
    print(eq * "=", "starting sim {}".format(i), eq * "=")
    sim = (
        Simulation().
            add([
            StochasticStartupGrowthRevivalRule(),
            GroupSizeProbe.by_attr('stage', 'stage', ['s', 'a', 'b', 'c', 'success', 'failure'],
                                   msg_mode=ProbeMsgMode.CUMUL),
            Group(m=10000)
        ]).
            run(20)
    )
    print(sim.probes[0].get_msg())
    print()


