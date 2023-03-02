import os
import argparse
# import cv2
from PIL import Image
from tqdm import tqdm
from matplotlib import pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument('-s', "--source_dir", type=str, required=True, help="path of the source directory")
parser.add_argument('-d', "--destination_dir", type=str, required=True, help="path of the destination directory")
args = parser.parse_args()


def tif2png(source_dir, destination_dir):

    img_names = [file for file in os.listdir(source_dir) if not file.startswith(".")]

    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)

    for name in tqdm(img_names):
        img = Image.open(source_dir+name)
        # print(img.size)
        # plt.imshow(img)
        # plt.show()
        rgb_img = img.convert("RGB")
        rgb_img.save(destination_dir+name[:name.rfind(".")]+".png")


if __name__ == "__main__":
    tif2png(args.source_dir, args.destination_dir)
