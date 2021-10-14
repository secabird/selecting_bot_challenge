# trality_challenge
I run the code with Python 3.7.11

The results are:
- overview_performance.pdf: overview tearsheet of all bots
- 5447dd37-4788-4e1e-b714-67b00bd9f024_performance.pdf: tearsheet of the winner bot, my criteria is the bot with best Sortino ratio

In AnomaliesHandler, after using K-means clustering to identify good time series range on some bots, we see that all good ranges start from 2020-12-08 08:55:00

Notice:
- DataHandler class: we can use load_data_from_csv() or quickly load object with load_data_from_pkl()
- AnomaliesHandler class: we can use clean_data() or quickly load object with load_good_data_from_pkl()
- Overivew performance object: we can use create_performance_stats(anomalies_handler.good_data) or quickly load object with load_performance_stats()


