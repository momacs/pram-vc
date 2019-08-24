from OpenSSL._util import byte_string
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
import  numpy as np

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [[5, 3, 4, 2, 4, 6],[1, 2, 3, 4, 5, 6],[6, 5, 4, 3, 2, 1]]

source1 = ColumnDataSource(data=dict(fruits=fruits, counts=counts[0]))

print(counts[0])
print(counts[1])
print(counts[2])

data = {}

# print(data.get("abc"))
population = "population"
a = ["n0","n1","n2","n3","n4","n5"]
b = ['seed', 'a', 'b', 'c',  'success', 'failure']
c = [population, 0, 0, 0, 0, 0]
# print(dict(zip(b,c)))

args = {'bokeh-autoload-element': [b'1002'], 'bokeh-app-path': [b'/main'],
        'bokeh-absolute-url': [b'http://localhost:5006/main'],
        'initial_population': [b'100000000'],
        'round_seed_a': [b'0.2'], 'round_seed_failure': [b'0.2'], 'round_a_b': [b'0.2'],
        'round_a_failure': [b'0.2'], 'round_b_c': [b'0.2'], 'round_b_failure': [b'0.2'],
        'round_c_success': [b'0.2'], 'round_c_failure': [b'0.2'],
        'round_success_success': [b'0.2'], 'round_success_failure': [b'0.2'],
        'round_failure_success': [b'0.2'], 'round_failure_failure': [b'0.2']}
#
# print(int(args.get('initial_population')[0]))
# print((args.get('round_seed_a')[0]).decode("utf-8"))
# print(type(float((args.get('round_seed_a')[0]).decode("utf-8"))))
# keys = ['initial_population', 'round_seed_a', 'round_seed_failure', 'round_a_b', 'round_a_failure', 'round_b_c', 'round_b_failure', 'round_c_success', 'round_c_failure', 'round_success_success', 'round_success_failure', 'round_failure_success', 'round_failure_failure']
#
# for k in keys:
#     args[k] = float((args.get(k)[0]).decode("utf-8"))
#

print(args)


def get_stochastic_multiplier(param = [1, 1.5, 2, 1.5, 1.1, 0]):
    stage_multiplier_list = [np.random.normal(param[0], 0.1 * param[0]),
                             np.random.normal(param[1], 0.1 * param[1]),
                             np.random.normal(param[2], 0.1 * param[2]),
                             np.random.normal(param[3], 0.1 * param[3]),
                             np.random.normal(param[4], 0.1 * param[4]),
                             np.random.normal(param[5], 0.1 * param[5])
                             ]
    return stage_multiplier_list

print(get_stochastic_multiplier())