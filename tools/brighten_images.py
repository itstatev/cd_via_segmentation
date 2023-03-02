from tqdm import tqdm
import cv2
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-s', "--source_path", type=str, required=True, help="path of the directory with images")
parser.add_argument('-d', "--destination_path", type=str, required=True, help="path of the destination directory")
args = parser.parse_args()


def brighten_images(source_path, destination_path):
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
        
    img_names = [file for file in os.listdir(source_path) if not file.startswith(".")]
    for name in tqdm(img_names):
        img = cv2.imread(source_path+name)
        new_img = 85 * img
        cv2.imwrite(destination_path+name, new_img)


if __name__ == "__main__":
    brighten_images(args.source_path, args.destination_path)