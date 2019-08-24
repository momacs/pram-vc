import numpy as np
import scipy.stats as scs
import pandas as pd
import numpy.random as npr
from pylab import plt, mpl
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file
# from bokeh import palettes
# palettes._PalettesModule.all_palettes()


class Asset(object):
    ObjNum = 0

    def __init__(self, entry_val, own_percent, mean_growth_rate = 0.10,
                 period_year = 10,  sigma = None, name=None):
        if name:
            self.name = name
        else:
            Asset.ObjNum += 1
            self.name = "asset"+(str(Asset.ObjNum))
        self.entry_valuation = entry_val
        self.ownership_percent = own_percent
        self.mean_growth_rate  = mean_growth_rate
        self.investment_period_year = period_year
        self.sigma = sigma
        self.mu = 1 + self.mean_growth_rate

        if self.sigma == None:
            self.sigma = np.sqrt(self.mu)

        self.initial_investment = self.entry_valuation * self.ownership_percent
        self.exit_investment = None

    def print_stats(self):
        stat1 = scs.describe(self.exit_investment[-1])
        print('%14s %14s' %
              ('statistic', 'data'))
        print(30 * "-")
        print('%14s %14.3f' % ('size', stat1[0]))
        print('%14s %14.3f' % ('min', stat1[1][0]))
        print('%14s %14.3f' % ('max', stat1[1][1]))
        print('%14s %14.3f' % ('mean', stat1[2]))
        print('%14s %14.3f' % ('std', np.sqrt(stat1[3])))
        print('%14s %14.3f' % ('skew', stat1[4]))
        print('%14s %14.3f ' % ('kurtosis', stat1[5]))


    def generate_samples(self,  distribution = 'exponential',num_samples = 10000, *args, **kwargs):

        self.exit_investment = np.zeros((self.investment_period_year+1,num_samples))
        self.exit_investment[0] = self.initial_investment
        for year in range(1, self.investment_period_year + 1):
            self.exit_investment[year] = self.exit_investment[year - 1] \
                                         * (1 + np.random.exponential(self.mean_growth_rate, num_samples))

        # for normal dist #todo : need to find efficient design for computing different function as the sample size grows
        self.exit_investment_normal = np.zeros((self.investment_period_year+1,num_samples))
        self.exit_investment_normal[0] = self.initial_investment
        for year in range(1, self.investment_period_year + 1):
            self.exit_investment_normal[year] = self.exit_investment[year - 1] \
                                         * (1 + np.random.normal(self.mu, self.sigma,num_samples))
        # for lognormal dist
        self.exit_investment_lognormal = np.zeros((self.investment_period_year + 1, num_samples))
        self.exit_investment_lognormal[0] = self.initial_investment

        for year in range(1, self.investment_period_year + 1):
            self.exit_investment_lognormal[year] = self.exit_investment[year - 1] \
                                             * (1 + np.random.lognormal(self.mu, self.sigma,num_samples))

        # for uniform dist
        self.exit_investment_unif = np.zeros((self.investment_period_year + 1, num_samples))
        self.exit_investment_unif[0] = self.initial_investment

        for year in range(1, self.investment_period_year + 1):
            self.exit_investment_unif[year] = self.exit_investment[year - 1] \
                                         * (1 + np.random.uniform(-self.mu,+self.mu,num_samples))

            # print(self.exit_investment)

    def get_value_at_risk(self):
        pass

    def get_exit_val_from_samples(self):
        # print(self.exit_investment.shape)
        # print(len(self.exit_investment[-1,:]))
        # print(self.exit_investment[-1,:])
        return self.exit_investment[-1,:]

    def get_exit_random_path(self, n = 10):

        n = int(round(n))
        if n is None or n > 100 or n < 10:
            n=10

        return self.exit_investment[:, :n]

    def plot_charts(self):

        plt.figure(figsize=(10, 6))
        plt.hist( self.exit_investment[-1], bins=50)
        plt.title("Final Exit Valuation after {} year as Geometric Brownian Motion".format(self.investment_period_year))
        plt.xlabel('Exit Valuation')
        plt.ylabel('frequency');
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(self.exit_investment[:, :10], lw=1.5)
        plt.xlabel('time')
        plt.ylabel('index level');
        plt.title('Sample Path')
        plt.show()



def main():
    a = Asset(entry_val=  100, own_percent=0.10)
    a.generate_samples()
    a.get_exit_val_from_samples()
    # a.plot_charts()
    # print(a.get_exit_random_path())
    # print(a.get_exit_random_path().T )
    random_path = a.get_exit_random_path()
    col_dict = dict()
    for x in range(10):
        print(random_path[:,x])

        col_dict[str(x)] = random_path[:,x]
    # col_dict['x'] = list(range(0,10+1,1))
    df = pd.DataFrame(col_dict)
    source = ColumnDataSource(df)
    print(df)
    p = figure(plot_width=800, plot_height=800)

    y = [str(i) for i in list(range(10))]
    print(y)
    # p.vline_stack([str(i) for i in list(range(10))], x='x', source=source)


    # p.vline_stack(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], x='x', source=source)

    mypalette = ['#440154', '#30678D', '#35B778', '#FDE724','#35B778', '#FDE724','#35B778', '#FDE724','#35B778', '#FDE724']
    p.multi_line(xs = 10*[list(range(10))], ys = [df[name] for name in y],line_color=mypalette, line_width=2)
    # print([str(i) for i in list(range(11))])
    show(p)
    print(10*[list(range(10))])
    a.print_stats()

if __name__ == "__main__":
    main()








# def get_random_rate_function(self, distribution = 'exponential',mean_rate = None, sigma=None, alpha = None, beta = None, ):
#     if distribution == 'exponential':
#         self.random_function = np.random.exponential
#     elif distribution == 'normal':
#         self.random_function = np.random.randn
#     elif distribution == 'lognormal':
#         self.random_function = np.random.lognormal
#     elif distribution == 'gamma':
#         self.random_function = np.random.gamma
#     elif distribution == 'beta':
#         self.random_function = np.random.beta
#     elif distribution == 'uniform':
#         self.random_function = np.random.uniform
#     else:
#         self.random_function = None