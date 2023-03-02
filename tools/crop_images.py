import numpy as np
import cv2
import os
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-cs', "--crop_size", type=int, required=True, help="size of the cropping kernel")
parser.add_argument('-s', "--source", type=str, required=True, help="source directory")
parser.add_argument('-d', "--destination", type=str, default='', help="destination directory. Source dir neighbour if not provided")
args = parser.parse_args()


def crop(image, crop_size):
    images = []
    for i in range(0, image.shape[0]-crop_size+1, crop_size):
        for j in range(0, image.shape[1]-crop_size+1, crop_size):
            images.append(image[i:i+crop_size, j:j+crop_size])
        if image.shape[1] % crop_size != 0:
            images.append(image[i:i+crop_size, image.shape[1]-crop_size:image.shape[1]])
    if image.shape[0] % crop_size != 0:
        for j in range(0, image.shape[1]-crop_size+1, crop_size):
            images.append(image[image.shape[0]-crop_size:image.shape[0], j:j+crop_size])
        if image.shape[1] % crop_size != 0:
            images.append(image[image.shape[0]-crop_size:image.shape[0], image.shape[1]-crop_size:image.shape[1]])

    x = (image.shape[0] // crop_size) * (image.shape[1] // crop_size) + \
        (image.shape[0] // crop_size) * (image.shape[1] % crop_size != 0) + \
        (image.shape[1] // crop_size) * (image.shape[0] % crop_size != 0) + \
        (image.shape[1] % crop_size != 0) * (image.shape[0] % crop_size != 0)

    assert len(images) == x, f"{len(images)}_vs_{x}"
    return images


def crop_recursively(crop_size, source_dir, destination_dir):
    if not destination_dir:
        slash_pos = source_dir[:-1].rfind("/")
        source_dir_name = source_dir[slash_pos+1:]
        source_dir_name = source_dir_name if source_dir_name[-1] != "/" else source_dir_name[:-1]
        destination_dir = source_dir[:slash_pos+1] + source_dir_name + f"_{crop_size}/" 
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)
    files = [i for i in os.listdir(source_dir) if not i.startswith(".")]
    files.sort()
    for file in tqdm(files):
        if not os.path.isdir(source_dir+file):
            image = cv2.imread(source_dir+file)
            images = crop(image, crop_size)
            dot_pos = file.rfind(".")
            for i, image in enumerate(images):
                cv2.imwrite(destination_dir+file[:dot_pos]+f"_{i}"+file[dot_pos:], image)
        else:
            file = file if file[-1] == "/" else file + "/"
            crop_recursively(crop_size, source_dir+file, destination_dir+file)


if __name__ == "__main__":
    crop_recursively(args.crop_size, args.source, args.destination)