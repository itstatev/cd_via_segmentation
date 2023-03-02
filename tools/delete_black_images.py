import numpy as np
import os
import cv2
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-p', "--dir_path", type=str, required=True, help="path of the directory containing sub directories including files with same names. \
                                                                   also one of the sub directories should be the special one, mentioned in bellow argument")
parser.add_argument('-n', "--special_dir_name", type=str, default="gt", help="name of the sub directory of directory mentioned in above argument, \
                                                                              which files should be checked whether they are fully black")

args = parser.parse_args()


def delete_black_images(special_dir_name, dir_path):
    sub_dirs = [file for file in os.listdir(dir_path) if not file.startswith(".")]
    if special_dir_name not in sub_dirs:
        print("Error")
        exit(0)
    else:
        black_image_names = []
        image_names = [img_name for img_name in os.listdir(dir_path+special_dir_name) if not img_name.startswith(".")]
        for img_name in image_names:
            img = cv2.imread(dir_path+special_dir_name+"/"+img_name)
            if np.all(img == 0):
                black_image_names.append(img_name)
        for img_name in black_image_names:
            for sub_dir in sub_dirs:
                print("X")
                os.remove(dir_path+sub_dir+"/"+img_name)




if __name__ == "__main__":
    delete_black_images(args.special_dir_name, args.dir_path)