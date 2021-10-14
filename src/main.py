from data_handler import DataHandler
from tearsheet import PortfolioTearsheet
from tearsheet import OverviewTearsheet
from  anomalies_handler import AnomaliesHandler
import performance

def run():

    data_handler = DataHandler()
    anomalies_handler = AnomaliesHandler(data_handler.data)

    # overview = performance.create_performance_stats(anomalies_handler.good_data) or performance.load_performance_stats()
    overview_perf = performance.create_performance_stats(anomalies_handler.good_data)
    overview_teersheet = OverviewTearsheet(overview_perf, title='Overview Performance')
    overview_teersheet.plot_results('overview_performance.pdf')

    best_bot = overview_perf.nlargest(1, 'Sortino ratio').index[0]
    best_curve = anomalies_handler.good_data[best_bot]
    portfolio_tearsheet = PortfolioTearsheet(portfolio_curve=best_curve, title=f'{best_bot} Performance')
    portfolio_tearsheet.plot_results(f'{best_bot}_performance.pdf')

if __name__ == "__main__":
    run()