import csv
import pandas as pd 
import os
from pathlib import Path
import argparse
from PIL import Image
import shutil

data_folder = Path.home()

class_list = ['cow','human','dog']

def load_csv_to_file_list(file):
    df = pd.read_csv(file)
    # return df.columns
    for row in df['manifest']:
        tmp = str(row).rsplit('-',2)[0].rsplit('/',1)[1]
        print(tmp)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--csv", required=True,
        help="csv file")
    args = vars(ap.parse_args())
    csv_file = args['csv']

    load_csv_to_file_list(csv_file)