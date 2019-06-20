#!/usr/bin/env python
# coding: utf-8

# <div>
#     <!-- Left DIV -->
#     <div style="float: left; width: 70%;">
#         <h1>{ Darwinex Labs }</h1>
#         <h3>Prop Investing Arm & Quant Team @ Darwinex (<a href="https://www.darwinex.com/?utm_source=github&utm_medium=jupyter-notebook&utm_content=intro-to-strategy-rd-darwin-api-1">www.darwinex.com</a>)
#         </h3>
#         <hr />
#         <p>This Jupyter Notebook references content, DARWIN API functionality and example source code that has been covered in past video tutorials, available via the following links:
#         </p>
#         <p>
#             <ol>
#                 <li><a href="https://www.youtube.com/watch?v=IDDHyjqt_TY&list=PLv-cA-4O3y96EwRy0T6Y6CY52_x9Zdec9" target="_blank"><b>YouTube Playlist - Algorithmic Trading & Investing with the DARWIN API</b></a>
#                 </li>
#                 <li><a href="https://github.com/darwinex/darwin-api-tutorials" target="_blank"><b>DARWIN API GitHub Repository</b></a>
#                 </li>
#             </ol>
#         </p>
#         <p>
#             <b>Copyright (c) 2017-2019, Darwinex. All rights reserved.</b>
#         </p>
#         <p>
#             This content is licensed under the BSD 3-Clause License, you may not use this file except in compliance with the License. You may obtain a copy of the License <a href="https://opensource.org/licenses/BSD-3-Clause" target="_blank">here</a>.
#         </p>
#     </div>
#     <!-- Right DIV -->
#     <div style="float: right;">
#         <img src="https://avatars2.githubusercontent.com/u/26509507?s=460&v=4" width="280px" height="280px" />
#     </div>
# </div>

# <hr />
# 
# # Introduction to Trading Strategy R&D with the DARWIN API
# ## Jun 17, 2019
# If you've been following our video tutorials on YouTube, we've now completed everything to do with the **DARWIN Info** and **Quotes APIs** in terms of their implementation in **Python 3**.
# 
# This means that we're now able to access DARWIN data in a number of ways, and have written the necessary code to begin trading strategy R&D on DARWIN asset portfolios.
# 
# This Jupyter Notebook serves as an introduction to trading strategy research & development applied to DARWIN asset portfolios. 
# 
# **We recommend that you follow this tutorial while watching the accompanying YouTube video here:**
# <br /><a href="https://youtu.be/KEtp_fAlDRc" target="_blank"><b>[YouTube] Quant Workflow & Algorithmic Trading R&D with the DARWIN API</b></a>
# 
# **Please note:**
# - The order of the table of contents below is important, as it represents the workflow followed by this tutorial.
# - The example strategy described herein is **not trading and/or investment advice in any shape or form**. It merely serves to demonstrate the process outlined in the tutorial.
# 
# **Please ensure you've read and understood the <a href="https://www.darwinex.com/legal/risk-disclaimer" target="_blank">Darwinex Risk Disclosure</a> before proceeding further in this tutorial.** The remainder of this tutorial assumes that you have already read and understood the contents of the risk disclosure referenced above.
# 
# ## Table of Contents:
# 1. Develop a hypothesis
# 1. Assess data requirements
# 1. Create the dataset
# 1. Generate factors
# 1. Calculate strategy returns
# 1. Evaluate results
# 1. Run statistical tests e.g. what is P(&mu; != 0) ? (***we'll cover this in future tutorials***)
# 
# ## What this tutorial does NOT cover (but future tutorials will):
# 
# 1. Performance fees
# 1. Volatility of returns
# 1. Divergence
# 1. Custom portfolio weights
# 1. DARWIN validation dates
# 
# <hr />

# # 1) Hypothesis
# 
# For this tutorial, our dummy hypothesis is that a **DARWIN's *_end-of-period_ return* is predictive of the *direction* of its *next-period return***.
# 
# To keep things simple (*future tutorials will iteratively add complexity*), we will:
# 
# 1. Not look at anything other than **return**.
# 1. Trade only the **top n DARWINs by end-of-period past return**, each period.

# # 2) Assess data requirements
# 
# 1. DARWIN symbols (to construct a universe)
# 1. Quotes for each symbol (for calculating returns)
# 1. Past Returns
# 1. Future Returns
# 1. Projected Returns of a Long-Only DARWIN portfolio

# # 3) Create the dataset
# 
# We need to call the **DARWIN Info API** as follows:
# 
# ### DARWIN symbols
# 
# For this we need to call `GET /products`. The function `_Get_DARWIN_Universe_()` in class `DWX_Info_API` implements this in Python.
# 
# ### DARWIN Quotes
# 
# For this we need to call `GET /products/{DARWIN Symbol}/history/quotes`. The function `_Get_Historical_Quotes_()` in class `DWX_Info_API` implements this in Python.
# 
# * Given the API limits at the present time, the above queries require a few hours to complete successfully. 
# 
# Therefore, for this tutorial, we've pre-downloaded and saved a DataFrame of DARWIN Quotes for all ACTIVE and DELETED status DARWINs, in a **pickle** archive called ***jn_all_quotes_active_deleted_12062019.pkl***, located in the **DATA/** directory.
# 
# Let's load this now:

# In[1]:


###########
# Imports #
###########
import os, pickle
os.chdir('E:/DARWIN_API_TUTORIALS/PYTHON/')

from MINIONS.dwx_graphics_helpers import DWX_Graphics_Helpers
from plotly.offline import init_notebook_mode
from scipy.stats import zscore
import pickle, warnings
import pandas as pd
import numpy as np

################################
# Some configuration for later #
################################
warnings.simplefilter("ignore") # Suppress warnings
init_notebook_mode(connected=True)
################################

# Create DWX Graphics Helpers object for later
_graphics = DWX_Graphics_Helpers()

# Load DataFrame of DARWIN quotes (Daily precision) from pickle archive.
quotes = pickle.load(open('../DATA/jn_all_quotes_active_deleted_12062019.pkl', 'rb'))

# Remove non-business days (consider Monday to Friday only)
quotes = quotes[quotes.index.dayofweek < 5]

# Load FX Market Volatility data upto 2019-06-17 (for evaluation later)
voldf = pd.read_csv('../DATA/volatility.beginning.to.2019-06-17.csv', 
                    index_col=0, 
                    parse_dates=True,
                    infer_datetime_format=True)

# Print DARWINs in dataset
print(f'DARWIN assets in dataset: {quotes.shape[1]}') # 5331 DARWINs

# Print list of DARWINs in DataFrame
print(f'\nDARWIN Symbols: \n{quotes.columns}')

# Select an example DARWIN and plot its Quotes
test_darwin = 'LVS.4.20'

# Plot test DARWIN Quotes
_graphics._plotly_dataframe_scatter_(
                            _df=pd.DataFrame(quotes[test_darwin].dropna()),
                            _x_title = "Date / Time",
                            _y_title = "Quote",
                            _main_title = f'${test_darwin} Quotes',
                            _plot_only = True)

print(quotes[test_darwin].tail())
pass; # Suppress object output


# ### Calculate Returns
# 
# #### Simple
# $$R_t = \frac{Q_t - Q_{t-1}}{Q_{t-1}}$$
# 
# .. which also simplifies to:
# 
# $$R_t = \frac{Q_t}{Q_{t-1}} - 1$$
# 
# 
# #### Logarithmic
# 
# $$R_t = log_e(Q_t) - log_e(Q_{t-1})$$
# 
# .. where ***Q*** represents the DARWIN Quote, and ***R*** represents Return.
# 
# Given a Pandas DataFrame where the columns contain DARWIN symbols, and the index contains timestamps, the following code can be used to generate returns for each DARWIN.
# 
# **Note:** There are certain advantages to using log over simple returns such as their time-additivity and avoidance of arithmetic underflow. But when calculating compounded returns, note that due to log returns being *continuously compounded*, the output values for compounded log returns are expected to be slightly different to compounded simple returns.
# 
# Both have been implemented below for you.

# In[2]:


"""
Function: Calculate log returns
Parameters: quotes -> pandas DataFrame containing DARWIN Quotes
Returns: log returns
"""
def calculate_log_returns(quotes):
    return np.log(quotes) - np.log(quotes.shift(1))

def calculate_simple_returns(quotes):
    return quotes.pct_change()


# In[3]:


# Calculate both simple and log returns for the loaded DataFrame above
log_returns = calculate_log_returns(quotes)
simple_returns = calculate_simple_returns(quotes)

# Print shape
print(f'\nShape of Returns: {log_returns.shape}') # 3204 rows, 5331 DARWINs

# Print last 5 log returns of randomly chosen DARWIN from earlier
print(f'\nLast 5 log returns of example DARWIN {test_darwin}: \n{log_returns.loc[:,test_darwin].tail(5)}')

# Print last 5 simple returns of randomly chosen DARWIN from earlier
print(f'\nLast 5 simple returns of example DARWIN {test_darwin}: \n{simple_returns.loc[:,test_darwin].tail(5)}')

# Print and plot all-time return of test DARWIN
print(f'\n${test_darwin} Price-based return: {quotes[test_darwin].dropna().values[-1] / quotes[test_darwin].dropna().values[0] - 1}')

# Compounded log return
print(f'\n${test_darwin} Compounded log return: {log_returns[test_darwin].dropna().sum()}')
print(f'\n${test_darwin} Compounded log return (converted to simple): {np.exp(np.log(quotes[test_darwin].dropna().values[-1]) - np.log(quotes[test_darwin].dropna().values[0])) - 1}')

# Compounded simple return
print(f'\n${test_darwin} Compounded simple return: {((1 + simple_returns[test_darwin].dropna()).cumprod() - 1)[-1]}')


# ## 3) Generate factors
# 
# ### Past & future returns
# 
# To select which DARWINs to buy at the beginning of a new period (e.g. Daily, Weekly, Monthly), we'll need to:
# 
# - Look at the past returns of all DARWINs in the DataFrame
# - Rank them in descending order of their most recent end-of-period return
# - Select the top n DARWINs in this ranked list
# 
# Generating past and future returns can be achieved by using the .shift() function in pandas as follows:
# 
# `log_returns.shift(1)`, where `1`represents the periods to shift, positive periods meaning *backwards*, negative periods meaning *forwards*.
# 
# Let's put this into a function of its own:

# In[4]:


"""
Function: Get shifted log returns
Parameters: log_returns, periods
Returns: shifted log returns
"""
def shifted_returns(log_returns, periods=1):
    return log_returns.shift(periods)

"""
Function: Get Top n DARWINs by past return
Parameters: log_returns, number of DARWINs
Returns: DataFrame of 0s and 1s, 1 being DARWIN to buy on next day's Open
"""
def get_top_n_in_row(row, _n):
    
    top_n = row[list(np.nonzero(row.values)[0])].nlargest(_n)
    _out = pd.Series(data=0, index=row.index)
    
    if len(top_n) == _n and top_n.values.min() > 0:
        _out[list(top_n.index)] = 1
    
    # Default
    return _out
    
def get_top_n_darwins(past_returns, n=20):
    return past_returns.apply(lambda row: get_top_n_in_row(row, n), axis=1)


# We can use the same function for both **past** and **future** returns.

# In[5]:


past_returns = shifted_returns(log_returns, 1)
future_returns = shifted_returns(log_returns, -1)

# Plot and print last 21 trading days of Quotes, past and future returns for the test DARWIN
df_c_test = pd.concat([quotes[test_darwin],
                 log_returns[test_darwin],
                 past_returns[test_darwin],
                 future_returns[test_darwin]
                ], axis=1)

# Set meaningful columns
df_c_test.columns = ['Quote','log_return','past_return','future_return']

# Plot
_graphics._plotly_dataframe_scatter_(
                            _df=pd.DataFrame(df_c_test.iloc[-21:, 1:].dropna()),
                            _x_title = "Date / Time",
                            _y_title = "Returns",
                            _main_title = f'${test_darwin} Log, Past & Future Returns',
                            _plot_only = True)

# Print last 5 log, past and future returns
print(f'Last 5 log, past and future return for ${test_darwin}:\n{df_c_test.tail(5)}')

# Let's see what the output of get_top_n_darwins() looks like.
top_20_darwins = get_top_n_darwins(past_returns, 20)

pass;


# #### BACKTESTING NOTE: Notice how the log returns shift in the outputs above. 
# 
# For example, on `2019-06-11`, the most recent `past return` to use in calculating the day's `projected returns` later on, was `-0.012200` or `-1.22%`, while the `future_return` is NaN or unknown.
# 
# This is precisely the behaviour we expect, since we only want to know information `valid up until the current period`, because in real-world trading we wouldn't know the `Close Quote: 342.35` and hence `log_return: -0.015966` for `2019-06-11` *yet*.. otherwise we'd be peeking into the future and generating a spectacular backtest **:smiley:**
# 
# **To make sense of this**, just remember that the strategy (in this case with the period set to 'Daily') will *trade on the Open of `2019-06-11`*, therefore those two values wouldn't be available at the time you intend on executing the trade, since they only get updated at the *Close of `2019-06-11`*!
# 
# ### So which DARWINs should we trade in the next period?

# In[6]:


# Example: Top 20 DARWINs to buy next
print(f'\nTop 20 DARWINs symbol names for next day:\n{top_20_darwins.iloc[-1,:].sort_values(ascending=False).index[:20].values.tolist()}')


# ### Which DARWINs have been traded the most, historically?

# In[7]:


# Example: Top 20 DARWINs bought historically
print(f'\nTop 20 DARWINs traded the most, historically:\n{top_20_darwins.sum().sort_values(ascending=False).index[:20].values.tolist()}')


# ## 4) Calculate strategy returns
# 
# Now that we have:
# 
# - A dataframe containing which n DARWINs we would trade every next period, and
# - A dataframe containing future returns
# 
# .. we can calculate the strategy's returns by simply multiplying each corresponding row in both dataframes together.
# 
# This will return a dataframe where only the DARWINs that have been traded on a particular day (row) will have a return associated with them.
# 
# Let's code this into a function, as below:

# In[8]:


"""
Function: Calculate strategy returns
Parameters: top_darwins and future_returns DataFrames
Returns: DataFrame of strategy returns
"""
def calculate_strategy_returns(top_darwins_df, future_returns_df, n=20, cost=np.log(1 + 0.002)):
    return top_darwins_df * (future_returns_df - cost) / n


# ### Let's create one function that encapsulates all our logic:

# In[9]:


def darwin_momentum_strategy(_timeframe='', top_n=50, _tcost=0.002):
    
    # Load DataFrame of DARWIN quotes (Daily precision) from pickle archive.
    quotes = pickle.load(open('../DATA/jn_all_quotes_active_deleted_12062019.pkl', 'rb'))

    # Remove non-business days (consider Monday to Friday only)
    quotes = quotes[quotes.index.dayofweek < 5]
    
    # Resample if timeframe != ''
    if _timeframe == 'W':
        quotes = quotes.resample('W-FRI').last()
    elif _timeframe == 'M':
        quotes = quotes.resample('M').last()
      
    # Calculate log, past and future returns
    log_returns = calculate_log_returns(quotes)
    past_returns = shifted_returns(log_returns, 1)
    future_returns = shifted_returns(log_returns, -1)
    
    # Generate DataFrame of Top n DARWINs by periodic return
    top_n_darwins = get_top_n_darwins(past_returns, top_n)
    
    # Calculate strategy returns
    strategy_returns = calculate_strategy_returns(top_n_darwins, future_returns, top_n, np.log(1 + _tcost))

    # Plot strategy returns
    strategy_returns = strategy_returns.sum(axis=1)
    cumulative_strategy_returns = strategy_returns.cumsum()
    cumulative_strategy_returns[cumulative_strategy_returns < -1] = -1

    return [strategy_returns, cumulative_strategy_returns]


# ### Now let's run some tests, using top_n = 10, 20, 30, 40 ... 100, setting transaction costs to 0.2%:

# In[10]:


"""
Function: Accept timeframe, top_n and _tcost and plot simulation results
"""
def plot_strategy_results(_timeframe='', 
                          top_n_range=[10,101,10], 
                          _tcost=0.002,
                          return_results=True):
    
    results = {}
    
    for _n in range(top_n_range[0],top_n_range[1],top_n_range[2]):
        print(f'Processing {_n} DARWINs..')
        results[(_timeframe,_n,_tcost)] = darwin_momentum_strategy(_timeframe, _n, _tcost)

    # Transform results into iterable data structures
    _k = list(results.keys())
    _v = list(results.values())
    
    print('\nGenerating plot.. please wait..')
    _graphics._plotly_dataframe_scatter_(
                            _df=pd.DataFrame(data={str(_k[i]): _v[i][1].values.tolist() 
                                                   for i in range(len(_k))},
                                             index=_v[0][1].index),
                            _x_title = 'Date / Time',
                            _y_title = 'Returns',
                            _main_title = f'[Strategy] Timeframe: {_timeframe}, Cost: {_tcost*100}%, Top "n" DARWINs = {top_n_range}',
                            _plot_only = True)
    
    print('\n..DONE!')
    
    if return_results:
        return [_k,_v]
    
# This dictionary will hold strategy results for each combination employed
results = {}


# ### Test 1: Daily sampling with transaction cost of 0.2%, in steps of 5 Top n DARWINs

# In[11]:


# Daily timeframe, 10 to 100 DARWINs in steps of 5, cost of 0.2%
results['Daily'] = plot_strategy_results('', [10,101,5], 0.002, True)


# ### Test 2: The daily strategy failed very quickly.. let's resample to Weekly and re-test the same strategy.

# In[12]:


# Weekly timeframe, 10 to 100 DARWINs in steps of 5, cost of 0.2%
results['Weekly'] = plot_strategy_results('W', [10,101,5], 0.002, True)


# ### Test 3: Weekly was better, but still obviously not investable.. let's resample to Monthly and re-test:

# In[13]:


# Monthly timeframe, 10 to 100 DARWINs in steps of 5, cost of 0.2%
results['Monthly'] = plot_strategy_results('M', [10,101,5], 0.002, True)


# ## 5) Evaluate results
# 
# We've now run a few tests using various parameter ranges.
# 
# Despite the **Monthly** rebalancing proving considerably more robust than the failed Daily and Weekly rebalancing, the results aren't particularly reliable.
# 
# **Here's why:**
# 
# 1. Incrementally adding more DARWINs to the momentum portfolio leads to progressively lower cumulative returns. 
# 
# 1. This is to be expected, but notice how all tests begin a downtrend from around **March 2018** onwards.
# 
# 1. From a Quant's perspective, this indicates that there is possibly a **regime shift** in play, one that could potentially have ***broken*** the momentum factor, i.e. a momentum driven DARWIN trading strategy became progressively less effective since around that time.
# 
# ### What can we make of this?
# 
# Well, to keep things simple in this first tutorial, we'll use our domain knowledge and investigate the correlation between our momentum trading strategy in this tutorial, and FX market volatility.
# 
# The assumption here that we'd like to validate with data, is that momentum factors are likely positively correlated with market volatility.
# 
# Given that a large majority of DARWINs in this example universe trade FX, it makes sense to investigate this relationship and evaluate further.
# 
# You'll have noticed at the beginning of this notebook, that we've preloaded an ***FX market volatility*** dataset for you, constructed through a proprietary technique we use in Darwinex Labs.
# 
# **For your convenience, we've also uploaded this volatility dataset to our GitHub repo here:**
# <p><a href="https://github.com/darwinex/DarwinexLabs/tree/master/research/fx_market_volatility" target="_blank">Volatility Dataset up to June 17, 2019</a></p>
# 
# ### Let's write some functions to help us with this:

# In[19]:


def generate_comparable_dataset(_strategy, _volatility, _timeframe):
    
    _voldf = _volatility[_volatility.index.dayofweek < 5]
    
    if _timeframe != '':
        if _timeframe == 'M':
            _voldf = _voldf.vol_portfolio.resample('M').last()
        elif _timeframe == 'W':
            _voldf = _voldf.vol_portfolio.resample('W-FRI').last()
    
    _retdf = _strategy[_strategy.index.isin(_voldf.index)]
    _retdf = _retdf[_retdf != 0]
    
    _vol = _voldf[_voldf.index.isin(_retdf.index)] 
    
    _vol.index = _vol.index.date
    _retdf.index = _retdf.index.date
    
    if _timeframe == '':
        _vol = _vol.vol_portfolio
        
    return _retdf, _vol

def compare_strategy_to_market_volatility(_strategy, _volatility, _timeframe='M'):

    _returns, _volatility = generate_comparable_dataset(_strategy, _volatility, _timeframe)

    print(f'Correlation: {np.corrcoef(_returns, _volatility)[0][1]}')
    
    print('\nGenerating plot.. please wait..')
    _graphics._plotly_dataframe_scatter_(
                            _df=pd.DataFrame(data={'strategy': zscore(_returns.values),
                                                   'volatility': zscore(_volatility.values)},
                                             index=_volatility.index),
                            _x_title = 'Date / Time',
                            _y_title = 'Z Score',
                            _main_title = f'Strategy Returns vs FX Market Volatility',
                            _plot_only = True)
    
def plot_all_test_correlations_to_market_volatility(_data,
                                                    _volatility,
                                                    _timeframe='M'):
    
    _tests = len(_data[1])
    _corrs = {}
    
    for i in range(_tests):
        _rets, _vol = generate_comparable_dataset(_data[1][i][0], _volatility, _timeframe)
        _corrs[i] = np.corrcoef(_rets, _vol)[0][1]
        
    print('\nGenerating plot.. please wait..')
    _graphics._plotly_dataframe_scatter_(
                            _df=pd.DataFrame(data={'correlation': _corrs},
                                             index=range(len(_corrs))),
                            _x_title = 'Date / Time',
                            _y_title = 'Correlation',
                            _main_title = f'{_timeframe} - Test Correlations with FX Market Volatility',
                            _plot_only = True)


# ### Let's now visualize how correlation of strategy returns changes with changes in the number of DARWINs and the rebalancing period.

# In[20]:


plot_all_test_correlations_to_market_volatility(results['Daily'], voldf, '')

plot_all_test_correlations_to_market_volatility(results['Weekly'], voldf, 'W')

plot_all_test_correlations_to_market_volatility(results['Monthly'], voldf, 'M')


# ### Let's also plot a few tests and visualize the evolution of returns vs market volatility.

# In[21]:


"""
Structure of each value in results{} -> [[test1,test2..], [result1, result2..]]
where resultx = [periodic_returns, cumulative_returns].

Therefore, to get periodic returns for:

test ('M', 10, 0.005) -> results['Monthly'][1][0][0]
test ('M', 20, 0.005) -> results['Monthly'][1][1][0]
test ('M', 30, 0.005) -> results['Monthly'][1][2][0] .. and so on.
"""

# Compare ('', 100, 0.002) returns to FX market volatility
compare_strategy_to_market_volatility(results['Daily'][1][9][0], voldf, '')

# Compare ('W', 100, 0.002) returns to FX market volatility
compare_strategy_to_market_volatility(results['Weekly'][1][9][0], voldf, 'W')

# Compare ('M', 100, 0.002) returns to FX market volatility
compare_strategy_to_market_volatility(results['Monthly'][1][9][0], voldf, 'M')


# ## Conclusion
# 
# Wow.. that was a LOT to go through!
# 
# This first tutorial was meant to introduce you to the **Quant / Algorithmic Trader's approach to Alpha Research**.
# 
# We discussed the workflow in brief, and came up with an example momentum factor to backtest across our universe of DARWIN assets.
# 
# And believe it or not.. this was just scratching the surface! :)
# 
# Future tutorials will go into progressively more detail, enhancing what we've covered today.
# 
# Hope you enjoyed it!
# 
# If so, please do take a moment to comment on this notebook's corresponding YouTube video, like and share it with your friends, colleagues and social networks - we would be eternally grateful for your support.
# 
# Thank you!
# 
