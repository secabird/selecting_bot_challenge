import pickle
import pandas as pd
from itertools import groupby

import numpy as np

def aggregate_returns(returns, frequency):

    def cum_returns(x):
        return np.exp(np.log(1 + x).cumsum())[-1] - 1

    if frequency == 'monthly':
        return returns.groupby(
            [lambda x: x.year, lambda x: x.month]).apply(cum_returns)

    if frequency == 'yearly':
        return returns.groupby(
            [lambda x: x.year]).apply(cum_returns)

    ValueError('frequency must be monthly or yearly')


def create_cagr(cum_returns, period):

    return (cum_returns[-1] ** (1.0 / period)) - 1.0


def create_sharpe_ratio(returns, interval):

    return np.sqrt(365 * 24 * 60 * 60 / interval) * (np.mean(returns)) / np.std(returns)


def create_sortino_ratio(returns, interval):

    return np.sqrt(365 * 24 * 60 * 60 / interval) * (np.mean(returns)) / np.std(returns[returns < 0])


def create_drawdowns(cum_returns):

    hwm = [0]

    idx = cum_returns.index
    drawdowns = pd.Series(index = idx)
    duration = pd.Series(index = idx)

    for t in range(1, len(idx)):
        hwm.append(max(hwm[t-1], cum_returns[t]))
        drawdowns[t]= (hwm[t]-cum_returns[t])/hwm[t]
        duration[t]= (0 if drawdowns[t] == 0 else duration[t-1]+1)

    return drawdowns, drawdowns.max(), duration.max()

def create_performance_stats(data):

    perf_df = pd.DataFrame()

    for bot in data:
        period = (data[bot].index[-1] - data[bot].index[0]).days / 365
        interval = (data[bot].index[1] - data[bot].index[0]).seconds

        returns = data[bot]["portfolio_value"].pct_change().fillna(0.0)
        cum_returns = np.exp(np.log(1 + returns).cumsum())
        sharpe = create_sharpe_ratio(returns, interval)
        sortino = create_sortino_ratio(returns, interval)
        total_return = data[bot]["portfolio_value"].iloc[-1] / data[bot]["portfolio_value"].iloc[0] - 1
        _, max_drawdown, max_drawdown_duration = create_drawdowns(cum_returns)

        bot_df = pd.DataFrame(data={'Sharpe ratio':sharpe, 
                                    'Sortino ratio':sortino, 
                                    'Total Return':total_return, 
                                    'Max Drawdown':max_drawdown, 
                                    'Max Drawdown Duration':max_drawdown_duration},
                                    index=[bot])
        perf_df = perf_df.append(bot_df)

        with open('perf.pkl', 'wb') as f:
            pickle.dump(perf_df, f)           
    
    return perf_df

def load_performance_stats():

    with open('perf.pkl', 'rb') as f:
        data = pickle.load(f)        
    
    return data    

