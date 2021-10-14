import pickle
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from data_handler import DataHandler

class AnomaliesHandler:
    
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.pkl_path = 'good_data.pkl'
        # clean_data or load_good_data_from_pkl
        self.good_data = self.clean_data()
        
    def clean_data(self):
        
        good_data = {}
        for bot in self.raw_data:
            time_column = self.raw_data[bot].index
            time_diff = np.diff(np.array(time_column))
            data_to_label = np.array(list(zip(time_column.astype(int)/10**9, time_diff)))
            clusters = self.label_clusters(data_to_label)
            self.raw_data[bot]['cluster'] = np.concatenate([[99], clusters])
            counts = np.bincount(self.raw_data[bot]['cluster'])                             

            # After visualizing, we get only data with time index >= 2020-12-08 08:55:00
            start_time = datetime.strptime('2020-12-08 08:55:00', "%Y-%m-%d %H:%M:%S")
            good_data[bot] = self.raw_data[bot].loc[(self.raw_data[bot]['cluster'] == np.argmax(counts)) & (self.raw_data[bot].index >= start_time)]
            good_data[bot].drop(columns=['cluster'], inplace=True)
        
        with open(self.pkl_path, 'wb') as f:
            pickle.dump(good_data, f)   

        return good_data

    @staticmethod
    def label_clusters(data):
        
        km3 = KMeans(n_clusters=3)
        km3.fit(data)
        return km3.labels_

    def load_good_data_from_pkl(self):
        
        with open(self.pkl_path, 'rb') as f:
            data = pickle.load(f)        
        
        return data
