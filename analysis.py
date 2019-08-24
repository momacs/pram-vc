from financeLib.Asset import Asset
from financeLib.Portfolio import Portfolio
from typing import Dict
import numpy as np
import scipy.stats as scs
import math
import numpy.random as npr
from pylab import plt, mpl
import pandas as pd
import json
import scipy.special
from bokeh.layouts import gridplot,row
from bokeh.plotting import figure, show, output_file
from financeLib.stochastics import print_stats
import scipy.stats as scs

def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)
    # x-data for the ECDF: x
    x = np.sort(data)
    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n
    return x, y

def make_plot(title, hist, edges, x = None, pdf = None, cdf = None):

    p = figure(title=title, tools='', background_fill_color="#fafafa")

    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)

    if pdf is not None:
        p.line( x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend="PDF")

    if False:
        if cdf is not None:
            p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend="CDF")

    p.y_range.start = 0
    p.legend.location = "center_right"
    # p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'Exit Valuation'
    p.yaxis.axis_label = 'Normalized Frequency'

    # p.grid.grid_line_color="white"
    return p

def getFinalDistribution(data: Dict):
    {'dist': 'exponential', 'assetName': 'aa', 'entryVal': '100', 'ownPercent': '0.2', 'periodYears': '10',
     'growthRate': '0.25', 'sigma': '', 'samples': '100'}
    data.get('entryVal')
    newAsset = Asset(entry_val = data.get('entryVal'), own_percent = data.get('ownPercent'), mean_growth_rate  = data.get('growthRate'),
                 period_year  = data.get('periodYears'),  sigma  = data.get('sigma'), name = data.get('assetName'))

    newAsset.generate_samples( distribution = data.get('dist'),num_samples = data.get('samples'))
    measured = newAsset.get_exit_val_from_samples()
    measured = np.where(np.abs(measured - np.mean(measured)) > (3.5 * np.std(measured)),
                        (np.mean(measured) + 3.5 * np.std(measured)), measured)
    # Calculation of #bins using Sturge’s Rule
    # num_bins = int(round(1 + 3.322 * np.log10(len(measured))))

    # Calculation of #bins using Rice rule
    num_bins = int(round(2 * np.power(len(measured), 1/3)   ))

    x, samples_cdf = ecdf(measured)
    hist, edges = np.histogram(measured, density=True, bins=num_bins)
    p2 = make_plot("Sample Distribution", hist, edges, x=x, cdf=samples_cdf)

    # plotting random paths
    n_random_path = 10
    random_path = newAsset.get_exit_random_path(n_random_path)
    p1 = make_multiline_plot(random_path)
    p3 = make_ecdf_plot(measured)
    p = gridplot([p1,p2,p3], ncols=2)
    # p = tempfn()
    # p = row(p1,p2)
    # show(p)
    return p

def getCompareFinalDistribution(data: Dict):
    ################
    # for plot set A
    a_newAsset = Asset(entry_val=data.get('a_entryVal'), own_percent=data.get('a_ownPercent'),
                     mean_growth_rate=data.get('a_growthRate'),
                     period_year=data.get('a_periodYears'), sigma=data.get('a_sigma'), name=data.get('a_assetName'))

    a_newAsset.generate_samples(distribution=data.get('a_dist'), num_samples=data.get('samples'))

    measured = a_newAsset.get_exit_val_from_samples()
    measured = np.where(np.abs(measured - np.mean(measured)) > (3.5 * np.std(measured)),
                        (np.mean(measured) + 3.5 * np.std(measured)), measured)
    # Calculation of #bins using Sturge’s Rule
    # num_bins = int(round(1 + 3.322 * np.log10(len(measured))))

    # Calculation of #bins using Rice rule
    num_bins = int(round(2 * np.power(len(measured), 1 / 3)))

    x, samples_cdf = ecdf(measured)
    hist, edges = np.histogram(measured, density=True, bins=num_bins)
    a_p1 = make_plot("Sample Distribution", hist, edges, x=x, cdf=samples_cdf)

    # plotting random paths
    n_random_path = 10
    random_path = a_newAsset.get_exit_random_path(n_random_path)
    a_p2 = make_multiline_plot(random_path)
    a_p3 = make_ecdf_plot(measured)

    ################
    # for plot set B
    b_newAsset = Asset(entry_val=data.get('b_entryVal'), own_percent=data.get('b_ownPercent'),
                       mean_growth_rate=data.get('b_growthRate'),
                       period_year=data.get('b_periodYears'), sigma=data.get('b_sigma'), name=data.get('b_assetName'))

    b_newAsset.generate_samples(distribution=data.get('b_dist'), num_samples=data.get('samples'))

    measured = b_newAsset.get_exit_val_from_samples()
    measured = np.where(np.abs(measured - np.mean(measured)) > (3.5 * np.std(measured)),
                        (np.mean(measured) + 3.5 * np.std(measured)), measured)
    # Calculation of #bins using Sturge’s Rule
    # num_bins = int(round(1 + 3.322 * np.log10(len(measured))))

    # Calculation of #bins using Rice rule
    num_bins = int(round(2 * np.power(len(measured), 1 / 3)))

    x, samples_cdf = ecdf(measured)
    hist, edges = np.histogram(measured, density=True, bins=num_bins)
    b_p1 = make_plot("Sample Distribution", hist, edges, x=x, cdf=samples_cdf)

    # plotting random paths
    n_random_path = 10
    random_path = b_newAsset.get_exit_random_path(n_random_path)
    b_p2 = make_multiline_plot(random_path)
    b_p3 = make_ecdf_plot(measured)

    p = gridplot([a_p1,b_p1, a_p2,b_p2, a_p3,b_p3], ncols=2)
    # p = tempfn()
    # p = row(p1,p2)
    # show(p)

    ################
    # For statistical data
    ################
    # print_stats(a_newAsset.get_exit_val_from_samples(),b_newAsset.get_exit_val_from_samples())
    stats = dict(
    a_stats = scs.describe(a_newAsset.get_exit_val_from_samples()),
    b_stats = scs.describe(b_newAsset.get_exit_val_from_samples())
    )
    return p, stats

def make_ecdf_plot(measured):
    p = figure(title='Cummulative Distribution', tools='', background_fill_color="#fafafa")
    x,cdf = ecdf(measured)
    p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend="CDF")

    p.legend.location = "center_right"
    p.xaxis.axis_label = 'Exit Valuation'
    p.yaxis.axis_label = 'P(X < Exit Valuation)'
    return p

def make_multiline_plot(random_path, n_random_path = 10):

    col_dict = dict()
    for x in range(n_random_path):
        # print(random_path[:,x])
        col_dict[str(x)] = random_path[:,x]
    p1 = figure(title="Random Paths", tools='', background_fill_color="#fafafa")
    df = pd.DataFrame(col_dict)

    y = [str(i) for i in list(range(n_random_path))]
    print(y)

    mypalette = ['#440154', '#30678D', '#35B778', '#FDE724', '#35B778', '#FDE724', '#35B778', '#FDE724', '#35B778',
                 '#FDE724']
    print(mypalette)
    print(df)
    for z in range(10):
        print(df.iloc[:,z] )
    # for name in y:
    #     print(df[:,name])
    p1.multi_line(xs=n_random_path * [list(range(n_random_path))],
                  # ys=[df.iloc[:,:name] for name in range(10)],
                  ys=[df[name] for name in y],
                  line_color=mypalette, line_width=2)

    p1.legend.location = "center_right"
    # p.legend.background_fill_color = "#fefefe"
    p1.xaxis.axis_label = 'Random Path for Investments'
    p1.yaxis.axis_label = 'Exit Valuation'

    return p1

def make_plot1(title, hist, edges, x, pdf, cdf):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line(x, pdf, line_color="#ff8888", line_width=4, alpha=0.7, legend="PDF")
    p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend="CDF")

    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"
    return p

def tempfn():
    # Normal Distribution

    mu, sigma = 0, 0.5

    measured = np.random.normal(mu, sigma, 1000)
    hist, edges = np.histogram(measured, density=True, bins=50)

    x = np.linspace(-2, 2, 1000)
    pdf = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))
    cdf = (1 + scipy.special.erf((x - mu) / np.sqrt(2 * sigma ** 2))) / 2

    p1 = make_plot1("Normal Distribution (μ=0, σ=0.5)", hist, edges, x, pdf, cdf)

    # Log-Normal Distribution

    mu, sigma = 0, 0.5

    measured = np.random.lognormal(mu, sigma, 1000)
    hist, edges = np.histogram(measured, density=True, bins=50)

    x = np.linspace(0.0001, 8.0, 1000)
    pdf = 1 / (x * sigma * np.sqrt(2 * np.pi)) * np.exp(-(np.log(x) - mu) ** 2 / (2 * sigma ** 2))
    cdf = (1 + scipy.special.erf((np.log(x) - mu) / (np.sqrt(2) * sigma))) / 2

    p2 = make_plot1("Log Normal Distribution (μ=0, σ=0.5)", hist, edges, x, pdf, cdf)

    # Gamma Distribution

    k, theta = 7.5, 1.0

    measured = np.random.gamma(k, theta, 1000)
    hist, edges = np.histogram(measured, density=True, bins=50)

    x = np.linspace(0.0001, 20.0, 1000)
    pdf = x ** (k - 1) * np.exp(-x / theta) / (theta ** k * scipy.special.gamma(k))
    cdf = scipy.special.gammainc(k, x / theta)

    p3 = make_plot1("Gamma Distribution (k=7.5, θ=1)", hist, edges, x, pdf, cdf)

    # Weibull Distribution

    lam, k = 1, 1.25
    measured = lam * (-np.log(np.random.uniform(0, 1, 1000))) ** (1 / k)
    hist, edges = np.histogram(measured, density=True, bins=50)

    x = np.linspace(0.0001, 8, 1000)
    pdf = (k / lam) * (x / lam) ** (k - 1) * np.exp(-(x / lam) ** k)
    cdf = 1 - np.exp(-(x / lam) ** k)

    p4 = make_plot1("Weibull Distribution (λ=1, k=1.25)", hist, edges, x, pdf, cdf)

    output_file('histogram.html', title="histogram.py example")

    return (gridplot([p1, p2, p3, p4], ncols=2, plot_width=400, plot_height=400, toolbar_location=None))

if __name__ == "__main__":
    getFinalDistribution()