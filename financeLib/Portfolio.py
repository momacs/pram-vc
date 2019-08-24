import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import scipy.stats as scs
import math
import numpy.random as npr
from pylab import plt, mpl
from financeLib.Asset import Asset

class Portfolio(object):

    def __init__(self, num_samples):
        self.assetList = []
        self.final_portfolio_valuation = None
        self.num_samples = num_samples

    def add_new_asset(self,new_asset):
        self.assetList.append(new_asset)

    def generate_porfolio_samples(self):
        self.max_year = 1
        for asset in self.assetList:
            if asset.investment_period_year > self.max_year:
                self.max_year = asset.investment_period_year
        # self.final_portfolio_valuation = np.zeros((self.max_year+1, self.num_samples))

        for asset in self.assetList:
            asset.generate_samples(distribution='exponential',num_samples=self.num_samples)

        self.final_portfolio_valuation =   np.zeros((self.num_samples))

        for current_asset in self.assetList:
            # print("Running loop")
            # print(current_asset.get_exit_val_from_samples().shape)
            # print(self.final_portfolio_valuation.shape)
            # print(current_asset.get_exit_val_from_samples())
            self.final_portfolio_valuation = np.add(self.final_portfolio_valuation,current_asset.get_exit_val_from_samples())


        # Experimental
        # self.portolio_valuation = np.zeros((self.max_year,self.num_samples))
        #
        # for year in range(self.max_year):
        #     for asset in self.assetList:
        #         print("current year {}".format(year))
        #         print(asset.exit_investment.shape)
        #         if year > asset.investment_period_year:
        #
        #             print("Skipping {}".format(asset.name))
        #             continue
        #         else:
        #             self.portolio_valuation[year] = \
        #                 np.add(self.portolio_valuation[year],
        #                        asset.exit_investment[year])

        return self.final_portfolio_valuation

    def plot_charts(self):
        print(self.final_portfolio_valuation)
        plt.figure(figsize=(10, 6))
        plt.hist( self.final_portfolio_valuation, bins=100)
        plt.title("Final Exit Valuation complete Portfolio after {} year as Geometric Brownian Motion".format(self.max_year))
        plt.xlabel('Exit Valuation')
        plt.ylabel('frequency');
        plt.show()

        # plt.figure(figsize=(10, 6))
        # plt.plot(self.portolio_valuation[:, :10], lw=1.5)
        # plt.xlabel('time')
        # plt.ylabel('index level');
        # plt.title('Sample Path')
        # plt.show()


def main():
    a = Asset(100,0.4)
    b = Asset(200,0.4)
    c = Asset(100, 0.2)
    p = Portfolio(10000)
    p.add_new_asset(a)
    p.add_new_asset(b)
    p.add_new_asset(c)
    p.add_new_asset(Asset(200,0.2,period_year = 5))
    p.generate_porfolio_samples()
    p.plot_charts()

if __name__ == "__main__":
    main()
