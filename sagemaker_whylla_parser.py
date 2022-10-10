import csv
import json
import pandas as pd 
import os
from pathlib import Path
import argparse
from PIL import Image
import shutil

HD_W = 1920
HD_H = 1080

ANN_DEST = 'D:/Data/temp/raw_dataset/annotation/'
FRM_DEST = 'D:/Data/temp/raw_dataset/frame/'
ANN_DIR = 'D:/Data/temp/annotation/'
FRM_DIR = 'D:/Data/temp/frame/'

data_folder = Path.home()

class_list = ['cow','human','dog']

def load_csv_to_file_list(file):
    ls = []
    df = pd.read_csv(file)
    # return df.columns
    for row in df['manifest']:
        tmp = str(row).rsplit('-', 2)[0].rsplit('/',1)[1]
        # print(tmp)
        ls.append(tmp)
    return ls

def retrieve_all_json_files(root):
    #retrieving all csv files in all subdirs
    file_list = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if (name.endswith('.json')):
                file_list.append(os.path.join(path, name))
    return file_list

def extract_json(video_source_file, json_file):
    with open(json_file) as file:
        data = json.load(file)['detectionAnnotations']
        frame = data['frame']
        anns = data['boundingBoxes']
        print(video_source_file + "/" + frame)
        # print(anns[0])
        # bounding_rects = []
        for ann in anns:
            object_label = ann['label']
            if object_label == 'cow_head':
                object_label = 'cow'
            if object_label == 'person':
                object_label = 'human'
            class_id = class_list.index(object_label)
            # print("Width: {}, Height: {}, x_min: {}, y_min: {}"
            #     .format(ann['width']/HD_W,ann['height']/HD_H,ann['left']/HD_W,ann['top']/HD_H))
            rect_tuple = calculate_rect(ann['left'],ann['top'],ann['height'],ann['width'], HD_W, HD_H)
            # bounding_rects.append((class_id, rect_tuple[0], rect_tuple[1], rect_tuple[2], rect_tuple[3]))
            # print("Class: {}, x_center: {}, y_center: {}, width: {}, height: {}"
            #     .format(class_id, rect_tuple[0], rect_tuple[1], rect_tuple[2], rect_tuple[3]))
            format_and_write_to_txt(video_source_file, frame, class_id, rect_tuple[0], rect_tuple[1], rect_tuple[2], rect_tuple[3])
            copy_frame_to_dir(video_source_file, frame)

def calculate_rect(left, top, input_width, input_height, w_dim, l_dim):
    #Calculate rectangle's center, width, and height
    x_center, y_center = 0.0, 0.0
    x_min = left
    y_min = top
    x_max = x_min + input_width
    y_max = y_min + input_height
    height = input_height/l_dim
    width = input_width/w_dim
    x_center = ((x_min + x_max) / 2 ) / w_dim
    y_center = ((y_min + y_max) / 2 ) / l_dim
    return (x_center, y_center, width, height)  

def format_and_write_to_txt(video_source_file, file, class_id, x_center, y_center, width, height):
    #Format string and write to file
    file = video_source_file + '_' + os.path.splitext(file)[0] + '.txt'
    file = os.path.join(ANN_DEST, file)
    with open(file, 'a+') as f:
        str = "{0} {1} {2} {3} {4}\n".format(class_id, x_center, y_center, width, height)
        f.write(str)
        f.close()

def copy_frame_to_dir(video_source_file, frame_url):
    frame_src = os.path.join(FRM_DIR, video_source_file + '/' + frame_url)
    frame_dest = os.path.join(FRM_DEST, video_source_file + '_' + frame_url)
    # Copy file from source to destination
    shutil.copyfile(frame_src, frame_dest)

def make_raw_dataset(video_list):
    for dir in video_list:
        working_dir = os.path.join(ANN_DIR, str(video_list.index(dir)))
        ls = retrieve_all_json_files(working_dir)
        for json in ls:
            extract_json(dir, json)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--csv", required=True,
        help="csv file")
    args = vars(ap.parse_args())
    csv_file = args['csv']

    ls = load_csv_to_file_list(csv_file)
    # print(ls)

    make_raw_dataset(ls)

    # extract_json("whyalla_unloading_ch1_20220901160649_20220901161030_73.mp4",
    #         "D:/Data/S3/whyalla/sept/annotation/annotations/worker-response/iteration-1/0/2ff99e13e1e053f494f4457accb039ac1342c7c3/frame_0019.jpeg.json")

    