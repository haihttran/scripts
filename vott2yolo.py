import csv
import pandas as pd 
import os
from pathlib import Path
import argparse
from PIL import Image
import shutil


data_folder = Path.home()

class_list = ['sheep','sheep_head','human','human_head','dog','dog_head']

def load_csv_to_df(file):
    #Load csv file to dataframe
    df = pd.read_csv(file)
    return df

def calculate_rect(x_min, y_min, x_max, y_max, w_dim, l_dim):
    #Calculate rectangle's center, width, and height
    x_center, y_center, width, height = 0.0, 0.0, 0.0, 0.0
    x_center = ((x_min + x_max) / 2 ) / w_dim
    y_center = ((y_min + y_max) / 2 ) / l_dim
    width = (x_max - x_min) / w_dim
    height = (y_max - y_min) / l_dim
    return (x_center, y_center, width, height)    

def format_and_write_to_txt(file, class_id, x_center, y_center, width, height):
    #Format string and write to file
    file = file + '.txt'
    with open(file, 'a+') as f:
        str = "{0} {1} {2} {3} {4}\n".format(class_id, x_center, y_center, width, height)
        f.write(str)
        f.close()

def retrieve_all_csv_files(root):
    #retrieving all csv files in all subdirs
    file_list = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if (name.endswith('.csv')):
                file_list.append(os.path.join(path, name))
    return file_list
            
        
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
    #Set output dir
    path = "../Output"
    # Remove existing dir and then Create a new directory because it does not exist 
    shutil.rmtree(path)	
    os.makedirs(path)
    files = retrieve_all_csv_files(dir)
    for file in files:
        if (os.path.isfile(file)):
            df = load_csv_to_df(file)
            for index, row in df.iterrows():
                # im = Image.open(os.path.join("../Data/", file))
                # width, height = im.size
                class_id = class_list.index(str(row['label']).lower())
                #calculate tuple of rect's center x, y, width, and height
                rect_tuple = calculate_rect(pd.to_numeric(row['xmin']),pd.to_numeric(row['ymin']),
                               pd.to_numeric(row['xmax']),pd.to_numeric(row['ymax']), 1920, 1080)
                format_and_write_to_txt(os.path.join(path, row['image']), class_id, rect_tuple[0], 
                                        rect_tuple[1], rect_tuple[2], rect_tuple[3])
            
            
                
