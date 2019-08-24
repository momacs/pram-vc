import numpy as np
import scipy.stats as scs
import math
import numpy.random as npr
from pylab import plt, mpl

npr.seed(100)
plt.style.use('seaborn')
mpl.rcParams['font.family']='serif'

def generate_random_samples():
    sample_size = 100

    rn1 = npr.rand(sample_size, 3)
    rn2 = npr.randint(1, 10, sample_size)
    rn3 = npr.sample(size=sample_size)
    a = list(range(0, 101, 25))
    rn4 = npr.choice(a, sample_size)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))
    ax1.hist(rn1, bins=25, stacked=True)
    ax1.set_title('rand')
    ax1.set_ylabel('frequency')
    ax2.hist(rn2, bins=25)
    ax2.set_title('randint')
    ax3.hist(rn3, bins=25)
    ax3.set_title('sample')
    ax3.set_ylabel('frequency')
    ax4.hist(rn4, bins=25)
    ax4.set_title('choice');
    plt.show()


def compute_bsm_simple_options(current_val =100.0, riskless_rate = 0.05,
                               volatility_sigma = 0.25, time_year = 2.0,
                               num_samples = 10000):
    val_at_T = current_val * np.exp((riskless_rate - 0.5 * (volatility_sigma ** 2)) * time_year + \
                                    volatility_sigma * math.sqrt(time_year) * npr.standard_normal(num_samples))
    plt.hist(val_at_T, bins=50)
    plt.xlabel('Index Value')
    plt.ylabel('Frequency')
    plt.show()
    print(val_at_T)
    return val_at_T

def compute_bsm_logNormal_options(current_val =100.0, riskless_rate = 0.05,
                                  volatility_sigma = 0.25, time_year = 2.0,
                                  num_samples = 10000):
    val_at_T = current_val * npr.lognormal((riskless_rate - 0.5 * (volatility_sigma ** 2)) * time_year, \
                                           volatility_sigma * math.sqrt(time_year), size=num_samples)
    plt.hist(val_at_T, bins=50)
    plt.xlabel('Index Value')
    plt.ylabel('Frequency')
    plt.show()
    print(val_at_T)
    return val_at_T

def print_stats(v1,v2):
    stat1 = scs.describe(v1)
    stat2 = scs.describe(v2)
    print('%14s %14s %14s' %
          ('statistic', 'data set 1', 'data set 2'))
    print(45 * "-")
    print('%14s %14.3f %14.3f' % ('size', stat1[0], stat2[0]))
    print('%14s %14.3f %14.3f' % ('min', stat1[1][0], stat2[1][0]))
    print('%14s %14.3f %14.3f' % ('max', stat1[1][1], stat2[1][1]))
    print('%14s %14.3f %14.3f' % ('mean', stat1[2], stat2[2]))
    print('%14s %14.3f %14.3f' % ('std', np.sqrt(stat1[3]),
                                  np.sqrt(stat2[3])))
    print('%14s %14.3f %14.3f' % ('skew', stat1[4], stat2[4]))
    print('%14s %14.3f %14.3f' % ('kurtosis', stat1[5], stat2[5]))
    

def geometric_brownian_motion_option_pricing(initial_val = 100,
                                             num_samples = 10000,
                                             riskless_rate = 0.05,
                                             volatility_sigma = 0.25,
                                             time_year = 2.0,
                                             num_time_interval_discretization = 50
                                             ):
    dt = time_year / num_time_interval_discretization
    samples = np.zeros((num_time_interval_discretization+1, num_samples))
    samples[0] = initial_val

    for t in range(1, num_time_interval_discretization+1):
        samples[t] = samples[t-1] * np.exp((riskless_rate - 0.5 * ( volatility_sigma ** 2 )) * dt +
                                           volatility_sigma * np.sqrt(dt)
                                           * npr.standard_normal(num_samples))

    print(45*"=")
    print(samples[1])
    plt.figure(figsize=(10, 6))
    plt.hist(samples[50], bins=50)
    plt.title("Geometric Brownian Motion")
    plt.xlabel('index level')
    plt.ylabel('frequency');
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(samples[:, :10], lw=1.5)
    plt.xlabel('time')
    plt.ylabel('index level');
    plt.title('Sample Path')
    plt.show()

    return samples

def square_root_diffusion_euler(initial_val = 0.05, kappa = 3.0, theta = 0.02, sigma = 0.1, time_year = 2,
                                num_samples = 10000,num_time_interval_discretization = 50 ):
    dt = time_year / num_time_interval_discretization

    xh = np.zeros((num_time_interval_discretization + 1, num_samples))
    x = np.zeros_like(xh)
    xh[0] = initial_val
    x[0] = initial_val
    for t in range(1, num_time_interval_discretization + 1):
        xh[t] = (xh[t - 1] +
                 kappa * (theta - np.maximum(xh[t - 1], 0)) * dt +
                 sigma * np.sqrt(np.maximum(xh[t - 1], 0)) *
                 math.sqrt(dt) * npr.standard_normal(num_samples))
    x = np.maximum(xh, 0)

    plt.figure(figsize=(10, 6))
    plt.hist(x[-1], bins=50)
    plt.xlabel('value')
    plt.ylabel('frequency');
    plt.title('Square root diffusion Approx Euler')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(x[:, :10], lw=1.5)
    plt.xlabel('time')
    plt.ylabel('index level');
    plt.title('Sample Path SRD approx')
    plt.show()

    return x

def square_root_diffusion_exact(initial_val = 0.05, kappa = 3.0, theta = 0.02, sigma = 0.1, time_year = 2,
                                num_samples = 10000,num_time_interval_discretization = 50):
    x = np.zeros((num_time_interval_discretization + 1, num_samples))
    x[0] = initial_val
    dt = time_year / num_time_interval_discretization

    for t in range(1, num_time_interval_discretization + 1):
        df = 4 * theta * kappa / sigma ** 2
        c = (sigma ** 2 * (1 - np.exp(-kappa * dt))) / (4 * kappa)
        nc = np.exp(-kappa * dt) / c * x[t - 1]
        x[t] = c * npr.noncentral_chisquare(df, nc, size=num_samples)

    plt.figure(figsize=(10, 6))
    plt.hist(x[-1], bins=50)
    plt.title("Square root diffusion Exact")
    plt.xlabel('value')
    plt.ylabel('frequency');
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(x[:, :10], lw=1.5)
    plt.xlabel('time')
    plt.ylabel('index level');
    plt.title('Sample Path SRD Exact')
    plt.show()

    return x


def value_at_risk_gbm(initial_val = 100):
    initial_val = 100
    val_t = compute_bsm_simple_options( current_val = initial_val, volatility_sigma=0.25, time_year=30 / 365)
    R_gbm = np.sort(val_t)

    plt.figure(figsize=(10, 6))
    plt.hist(R_gbm, bins=50)
    plt.title("Value at Risk")
    plt.xlabel('absolute return')
    plt.ylabel('frequency');
    plt.show()

    percs = [0.01, 0.1, 1., 2.5, 5.0, 10.0]
    var = scs.scoreatpercentile(R_gbm, percs)
    print(var)
    print('%16s %16s' % ('Confidence Level', 'Value-at-Risk'))
    print(33 * '-')
    for pair in zip(percs, var):
        print('%16.2f %16.3f' % (100 - pair[0], initial_val - pair[1]))

def credit_valuation_at_risk(average_loss = 0.5, failure_prob = 0.01, time_year = 1, num_samples = 100000):
    D = npr.poisson(failure_prob *time_year, num_samples)




if __name__ == "__main__":
    print(50 * "-")
    v1 = compute_bsm_simple_options()
    v2 = compute_bsm_logNormal_options()
    geometric_brownian_motion_option_pricing()
    square_root_diffusion_euler()
    square_root_diffusion_exact()
    print_stats(v1,v2)
    value_at_risk_gbm(100)
