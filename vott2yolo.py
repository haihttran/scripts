import csv
import pandas as pd 
import os
from pathlib import Path
import argparse

data_folder = Path.home()

class_list = ['sheep','sheep_head','person','person_head','dog','dog_head']

def load_csv_to_df(file):
    #Load csv file to dataframe
    df = pd.DataFrame()
    df.read_csv(file)
    return df

def calculate_rect(x_min, y_min, x_max, y_max):
    #Calculate rectangle's center, width, and height
    x_center, y_center, width, height = 0.0
    x_center = (x_min + x_max) / 2 
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min
    return (x_center, y_center, width, height)    

def format_and_write_to_txt(file, class_id, x_center, y_center, width, height):
    #Format string and write to file
    with open(file, 'a+') as f:
        str = "{1} {2} {3} {4} {5}".format(class_id, x_center, y_center, width, height)
        f.write(str)
        f.close()
        
if __name__ == "__main__":
    #Get list of photo file names
    #parse argument
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True,
        help="directory of csv files")
    args = vars(ap.parse_args())
    dir = args['dir']
    files = os.listdir(dir)
    for file in files:
        if os.path.isfile(os.path.join(your_path, file)):
            df = load_csv_to_df(file)
            for index, row in df.iterrows():
                class_id = class_list.index(row['label'])
                #calculate tuple of rect's center x, y, width, and height
                rect_tuple = calculate_rect(row['xmin'].astype(float),row['xmax'].astype(float),
                               row['ymin'].astype(float),row['ymax'].astype(float))
                format_and_write_to_txt(row['image'], rect_tuple[0], rect_tuple[1], rect_tuple[2], rect_tuple[3])
            
            
                
