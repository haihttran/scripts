import os
import shutil

def retrieve_all_files(root):
    #retrieving all csv files in all subdirs
    file_list = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if (name.endswith('.txt') or name.endswith('.jpg')):
                # file_list.append(os.path.splitext(os.path.join(path, name))[0])
                file_list.append(os.path.splitext(name)[0])
            else:
                # file_list.append(os.path.join(path, name))
                file_list.append(name)
    return file_list

if __name__ == "__main__":

    # text_files = set(retrieve_all_files("../data/labels_raw"))
    text_files = set(retrieve_all_files("../labels_without_dog"))
    video_files = set(retrieve_all_files("../data/images_raw_2"))
    # print(len(text_files))
    # print(len(video_files))
    diff = video_files - text_files
    # print(len(diff))
    for item in diff:
        item = item + '.jpg'
        # os.remove(os.path.join("../data/images_raw",item))
        shutil.move(os.path.join("../data/images_raw_2",item),"../temp_2")
        print("moved - " + item)