import csv
import pandas as pd 
import os
from pathlib import Path
import argparse

data_folder = Path.home()

class_list = ['sheep','sheep_head','person','person_head','dog','dog_head']

def load_csv_to_df(file):
    #Load csv file to dataframe

    df = pd.read_csv(file)
    return df

def calculate_rect(x_min, y_min, x_max, y_max):
    #Calculate rectangle's center, width, and height
    x_center, y_center, width, height = 0.0, 0.0, 0.0, 0.0
    x_center = ((x_min + x_max) / 2 ) / 1920
    y_center = ((y_min + y_max) / 2 ) / s1080
    width = x_max - x_min
    height = y_max - y_min
    return (x_center, y_center, width, height)    

def format_and_write_to_txt(file, class_id, x_center, y_center, width, height):
    #Format string and write to file
    file = file + '.txt'
    with open(file, 'a+') as f:
        str = "\n{0} {1} {2} {3} {4}".format(class_id, x_center, y_center, width, height)
        f.write(str)
        f.close()
        
if __name__ == "__main__":
    #Get list of photo file names
    #parse argument
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True,
        help="directory of csv files")
    args = vars(ap.parse_args())
    if os.path.exists(args['dir']):
        dir = args['dir']
    else:   
        print("Not a valid path")
    files = os.listdir(dir)
    for file in files:
        path = "../Output"
        if not os.path.exists(path):
            # Create a new directory because it does not exist 
            os.makedirs(path)
        if os.path.isfile(os.path.join(dir, file)):
            df = load_csv_to_df(os.path.join(dir, file))
            for index, row in df.iterrows():
                class_id = class_list.index(row['label'])
                #calculate tuple of rect's center x, y, width, and height
                rect_tuple = calculate_rect(pd.to_numeric(row['xmin']),pd.to_numeric(row['xmax']),
                               pd.to_numeric(row['ymin']),pd.to_numeric(row['ymax']))
                format_and_write_to_txt(os.path.join(path, row['image']), class_id, rect_tuple[0], 
                                        rect_tuple[1], rect_tuple[2], rect_tuple[3])
            
            
                
