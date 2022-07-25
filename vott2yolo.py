import csv
import pandas as pd 
import os

def load_csv_to_df(file):
    df = pd.DataFrame()
    df.read_csv(file)
    return df

def calculate_rect(x_min, y_min, x_max, y_max):
    x_center, y_center, width, height = 0.0
    x_center = (x_min + x_max) / 2 
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min
    return (x_center, y_center, width, height)    

