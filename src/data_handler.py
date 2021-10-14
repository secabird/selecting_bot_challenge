import pandas as pd
import csv
import pickle

class DataHandler:

    def __init__(self):

        self.csv_path = 'data.csv'
        self.pkl_path = 'data.pkl'
        # load_data_from_csv or load_data_from_pkl
        self.data = self.load_data_from_csv()

    def load_data_from_csv(self):
        df = pd.read_csv(self.csv_path)
        df.set_index('time', inplace=True)
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S")

        bots_list = df['user_id'].unique()
        data = {}
        for bot in bots_list:
            data[bot] = df.loc[df['user_id']==bot]
            data[bot].drop(columns=['user_id'], inplace=True)
            data[bot].sort_index(inplace=True)

        with open(self.pkl_path, 'wb') as f:
            pickle.dump(data, f)            

        return data
    
    def load_data_from_pkl(self):

        with open(self.pkl_path, 'rb') as f:
            data = pickle.load(f)        
        
        return data
