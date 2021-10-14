from matplotlib.ticker import FuncFormatter
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
import performance as perf

class OverviewTearsheet:
    def __init__(self, data, title=None):
        self.data = data
        self.interval = 300 # 5min = 300s
        self.title = title

    def _plot_table(self, data, ax=None, title=None):

        ax.set_title(title, fontweight='bold')
        
        ax.text(0.35, 3.9, 'Bot ID', fontweight='bold', horizontalalignment='right', fontsize=8, color='green')
        ax.text(3, 3.9, 'Sharpe ratio', fontweight='bold', horizontalalignment='right', fontsize=8, color='green')
        ax.text(4.5, 3.9, 'Sortino ratio', fontweight='bold', horizontalalignment='right', fontsize=8, color='green')
        ax.text(6, 3.9, 'Total Return', fontweight='bold', horizontalalignment='right', fontsize=8, color='green')
        ax.text(7.5, 3.9, 'Max Drawdown', fontweight='bold', horizontalalignment='right', fontsize=8, color='green')
        ax.text(9, 3.9, 'Max Drawdown Duration', fontweight='bold', horizontalalignment='right', fontsize=8, color='green')

        ax.text(0, 2.9, data.index[0], fontsize=8)
        ax.text(3, 2.9, '{:.2f}'.format(data['Sharpe ratio'].iloc[0]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 1.9, data.index[1], fontsize=8)
        ax.text(3, 1.9, '{:.2f}'.format(data['Sharpe ratio'].iloc[1]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 0.9, data.index[2], fontsize=8)
        ax.text(3, 0.9, '{:.2f}'.format(data['Sharpe ratio'].iloc[2]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 2.9, data.index[0], fontsize=8)
        ax.text(4.5, 2.9, '{:.2f}'.format(data['Sortino ratio'].iloc[0]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 1.9, data.index[1], fontsize=8)
        ax.text(4.5, 1.9, '{:.2f}'.format(data['Sortino ratio'].iloc[1]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 0.9, data.index[2], fontsize=8)
        ax.text(4.5, 0.9, '{:.2f}'.format(data['Sortino ratio'].iloc[2]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 2.9, data.index[0], fontsize=8)
        ax.text(6, 2.9, '{:.2%}'.format(data['Total Return'].iloc[0]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 1.9, data.index[1], fontsize=8)
        ax.text(6, 1.9, '{:.2%}'.format(data['Total Return'].iloc[1]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 0.9, data.index[2], fontsize=8)
        ax.text(6, 0.9, '{:.2%}'.format(data['Total Return'].iloc[2]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 2.9, data.index[0], fontsize=8)
        ax.text(7.5, 2.9, '{:.2%}'.format(data['Max Drawdown'].iloc[0]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 1.9, data.index[1], fontsize=8)
        ax.text(7.5, 1.9, '{:.2%}'.format(data['Max Drawdown'].iloc[1]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 0.9, data.index[2], fontsize=8)
        ax.text(7.5, 0.9, '{:.2%}'.format(data['Max Drawdown'].iloc[2]), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 2.9, data.index[0], fontsize=8)
        ax.text(9, 2.9, '{:.2f} h'.format(data['Max Drawdown Duration'].iloc[0] * self.interval / (60 * 60)), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 1.9, data.index[1], fontsize=8)
        ax.text(9, 1.9, '{:.2f} h'.format(data['Max Drawdown Duration'].iloc[1] * self.interval / (60 * 60)), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0, 0.9, data.index[2], fontsize=8)
        ax.text(9, 0.9, '{:.2f} h'.format(data['Max Drawdown Duration'].iloc[2] * self.interval / (60 * 60)), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.grid(False)
        ax.spines['top'].set_linewidth(2.0)
        ax.spines['bottom'].set_linewidth(2.0)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.set_ylabel('')
        ax.set_xlabel('')

        ax.axis([0, 10, 0, 5])
        return ax

    def plot_results(self, filename=None):

            rc = {
                'lines.linewidth': 1.0,
                'axes.facecolor': '0.995',
                'figure.facecolor': '0.97',
                'font.family': 'serif',
                'font.serif': 'Ubuntu',
                'font.monospace': 'Ubuntu Mono',
                'font.size': 10,
                'axes.labelsize': 10,
                'axes.labelweight': 'bold',
                'axes.titlesize': 10,
                'xtick.labelsize': 8,
                'ytick.labelsize': 8,
                'legend.fontsize': 10,
                'figure.titlesize': 12
            }
            sns.set_context(rc)
            sns.set_style("whitegrid")
            sns.set_palette("deep", desat=.6)

            vertical_sections = 6
            fig = plt.figure(figsize=(16, 12))
            fig.suptitle(self.title, y=0.94, weight='bold')
            gs = gridspec.GridSpec(vertical_sections, 3, wspace=0.25, hspace=0.4)

            ax_best_return = plt.subplot(gs[:1, :])
            ax_best_sharpe = plt.subplot(gs[1:2, :])
            ax_best_sortino = plt.subplot(gs[2:3, :])
            ax_worst_return = plt.subplot(gs[3:4, :])
            ax_worst_sharpe = plt.subplot(gs[4:5, :])
            ax_worst_sortino = plt.subplot(gs[5:6, :])            


            best_returns = self.data.nlargest(3, 'Total Return')
            best_sharpe = self.data.nlargest(3, 'Sharpe ratio')
            best_sortino = self.data.nlargest(3, 'Sortino ratio')
            worst_returns = self.data.nsmallest(3, 'Total Return')
            worst_sharpe = self.data.nsmallest(3, 'Sharpe ratio')
            worst_sortino = self.data.nsmallest(3, 'Sortino ratio')            

            self._plot_table(best_returns, ax=ax_best_return, title='Top 3 best Total return')
            self._plot_table(best_sharpe, ax=ax_best_sharpe, title='Top 3 best Sharpe ratio')
            self._plot_table(best_sortino, ax=ax_best_sortino, title='Top 3 best Sortino ratio')
            self._plot_table(worst_returns, ax=ax_worst_return, title='Top 3 worst Total return')
            self._plot_table(worst_sharpe, ax=ax_worst_sharpe, title='Top 3 worst Sharpe ratio')
            self._plot_table(worst_sortino, ax=ax_worst_sortino, title='Top 3 worst Sortino ratio')            

            plt.show() 
            fig.savefig(filename, bbox_inches='tight')       

class PortfolioTearsheet:

    def __init__(self, portfolio_curve, title=None):
        self.portfolio_curve = portfolio_curve
        self.period = (portfolio_curve.index[-1] - portfolio_curve.index[0]).days / 365
        self.interval = (portfolio_curve.index[1] - portfolio_curve.index[0]).seconds
        self.title = title

    def get_results(self, portfolio_df):
        stats = {}
        stats["returns"] = portfolio_df["portfolio_value"].pct_change().fillna(0.0)
        stats["cum_returns"] = np.exp(np.log(1 + stats["returns"]).cumsum())
        stats["sharpe"] = perf.create_sharpe_ratio(stats["returns"], self.interval)
        stats["sortino"] = perf.create_sortino_ratio(stats["returns"], self.interval)
        stats["cagr"] = perf.create_cagr(stats["cum_returns"], self.period)
        drawdowns, max_drawdown, max_drawdown_duration = perf.create_drawdowns(stats["cum_returns"])
        stats["drawdowns"] = drawdowns
        stats["max_drawdown"] = max_drawdown
        stats["max_drawdown_pct"] = max_drawdown
        stats["max_drawdown_duration"] = max_drawdown_duration

        return stats

    def _plot_cumulative_returns(self, stats, ax=None):

        def format_two_dec(x, pos):
            return '%.2f' % x

        cum_returns = stats['cum_returns']

        if ax is None:
            ax = plt.gca()

        y_axis_formatter = FuncFormatter(format_two_dec)
        ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
        ax.xaxis.set_tick_params(reset=True)
        ax.yaxis.grid(linestyle=':')
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.grid(linestyle=':')

        cum_returns.plot(lw=2, color='green', alpha=0.6, x_compat=False,
                    label='Portfolio', ax=ax)

        ax.axhline(1.0, linestyle='--', color='black', lw=1)
        ax.set_ylabel('Cumulative returns')
        ax.legend(loc='best')
        ax.set_xlabel('')
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')
        return ax

    def _plot_drawdown(self, stats, ax=None):

        def format_perc(x, pos):
            return '%.0f%%' % x

        drawdown = stats['drawdowns']

        if ax is None:
            ax = plt.gca()

        y_axis_formatter = FuncFormatter(format_perc)
        ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
        ax.yaxis.grid(linestyle=':')
        ax.xaxis.set_tick_params(reset=True)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.grid(linestyle=':')

        underwater = -100 * drawdown
        underwater.plot(ax=ax, lw=2, kind='area', color='red', alpha=0.3)
        ax.set_ylabel('')
        ax.set_xlabel('')
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')
        ax.set_title('Drawdown (%)', fontweight='bold')
        return ax

    def _plot_monthly_returns(self, stats, ax=None):

        returns = stats['returns']
        if ax is None:
            ax = plt.gca()

        monthly_ret = perf.aggregate_returns(returns, 'monthly')
        monthly_ret = monthly_ret.unstack()
        monthly_ret = np.round(monthly_ret, 3)
        monthly_ret.rename(
            columns={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                     5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                     9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'},
            inplace=True
        )

        sns.heatmap(
            monthly_ret.fillna(0) * 100.0,
            annot=True,
            fmt="0.1f",
            annot_kws={"size": 8},
            alpha=1.0,
            center=0.0,
            cbar=False,
            cmap=cm.RdYlGn,
            ax=ax)
        ax.set_title('Monthly Returns (%)', fontweight='bold')
        ax.set_ylabel('')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        ax.set_xlabel('')

        return ax

    def _plot_yearly_returns(self, stats, ax=None):

        def format_perc(x, pos):
            return '%.0f%%' % x

        returns = stats['returns']

        if ax is None:
            ax = plt.gca()

        y_axis_formatter = FuncFormatter(format_perc)
        ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
        ax.yaxis.grid(linestyle=':')

        yly_ret = perf.aggregate_returns(returns, 'yearly') * 100.0
        yly_ret.plot(ax=ax, kind="bar")
        ax.set_title('Yearly Returns (%)', fontweight='bold')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.xaxis.grid(False)

        return ax

    def _plot_portfolio_stats(self, stats, ax=None):

        returns = stats["returns"]
        cum_returns = stats['cum_returns']
        tot_ret = cum_returns[-1] - 1.0
        cagr = stats['cagr']
        sharpe = stats['sharpe']
        sortino = stats['sortino']
        drawdowns = stats['drawdowns']
        max_drawdown = stats['max_drawdown']
        max_drawdown_duration = stats['max_drawdown_duration'] * self.interval / (60 * 60) # in hours

        ax.text(7.50, 8.2, 'Portfolio', fontweight='bold', horizontalalignment='right', fontsize=8, color='green')

        ax.text(0.25, 6.9, 'Total Return', fontsize=8)
        ax.text(7.50, 6.9, '{:.0%}'.format(tot_ret), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0.25, 5.9, 'CAGR', fontsize=8)
        ax.text(7.50, 5.9, '{:.2%}'.format(cagr), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0.25, 4.9, 'Sharpe Ratio', fontsize=8)
        ax.text(7.50, 4.9, '{:.2f}'.format(sharpe), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0.25, 3.9, 'Sortino Ratio', fontsize=8)
        ax.text(7.50, 3.9, '{:.2f}'.format(sortino), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0.25, 2.9, 'Annual Volatility', fontsize=8)
        ax.text(7.50, 2.9, '{:.2%}'.format(returns.std() * np.sqrt(365 * 24 * 60 * 60 / self.interval)), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0.25, 1.9, 'Max Drawdown', fontsize=8)
        ax.text(7.50, 1.9, '{:.2%}'.format(max_drawdown), color='red', fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.text(0.25, 0.9, 'Max Drawdown Duration', fontsize=8)
        ax.text(7.50, 0.9, '{:.2f} h'.format(max_drawdown_duration), fontweight='bold', horizontalalignment='right', fontsize=8)

        ax.set_title('Portfolio Statistics', fontweight='bold')

        ax.grid(False)
        ax.spines['top'].set_linewidth(2.0)
        ax.spines['bottom'].set_linewidth(2.0)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.set_ylabel('')
        ax.set_xlabel('')

        ax.axis([0, 10, 0, 10])
        return ax

    def plot_results(self, filename=None):

        rc = {
            'lines.linewidth': 1.0,
            'axes.facecolor': '0.995',
            'figure.facecolor': '0.97',
            'font.family': 'serif',
            'font.serif': 'Ubuntu',
            'font.monospace': 'Ubuntu Mono',
            'font.size': 10,
            'axes.labelsize': 10,
            'axes.labelweight': 'bold',
            'axes.titlesize': 10,
            'xtick.labelsize': 8,
            'ytick.labelsize': 8,
            'legend.fontsize': 10,
            'figure.titlesize': 12
        }
        sns.set_context(rc)
        sns.set_style("whitegrid")
        sns.set_palette("deep", desat=.6)

        vertical_sections = 6
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle(self.title, y=0.94, weight='bold')
        gs = gridspec.GridSpec(vertical_sections, 3, wspace=0.25, hspace=1)

        stats = self.get_results(self.portfolio_curve)

        ax_portfolio = plt.subplot(gs[:2, :])
        ax_drawdown = plt.subplot(gs[2, :])
        ax_monthly_returns = plt.subplot(gs[3, :2])
        ax_yearly_returns = plt.subplot(gs[3, 2])
        ax_txt_curve = plt.subplot(gs[4:, 0])


        self._plot_cumulative_returns(stats, ax=ax_portfolio)
        self._plot_drawdown(stats, ax=ax_drawdown)
        self._plot_monthly_returns(stats, ax=ax_monthly_returns)
        self._plot_yearly_returns(stats, ax=ax_yearly_returns)
        self._plot_portfolio_stats(stats, ax=ax_txt_curve)

        plt.show()
        fig.savefig(filename, bbox_inches='tight')
