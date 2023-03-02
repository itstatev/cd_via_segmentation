import os 
import cv2
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('-s', "--source", type=str, required=True, help="path of the image or directory containing images")
parser.add_argument('-d', "--destination", type=str, default='', help="path of the destination directory. \
                                                                       Not storing results if destination is not provided")
args = parser.parse_args()


def get_name_and_extension(filename):
    slash_pos = filename[:-1].rfind("/")
    dot_pos = filename.rfind(".")
    return filename[slash_pos+1:dot_pos], filename[dot_pos:]


def seperate_a_mask_into_objects(mask, mask_path, destination):
    if not mask:
        mask = cv2.imread(mask_path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    
    # mask[mask > 123] = 255
    # mask[mask <= 123] = 0

    def detect_islands(mask):
        # deep_copy = lambda arg: [deep_copy(el) if isinstance(el, list) else el for el in arg]
        # mat = deep_copy(mat)
        # m = len(mat)
        # n = len(mat[0])
        m, n = mask.shape
        valid_row = lambda x: 0 <= x < m
        valid_col = lambda x: 0 <= x < n
        def bfs(mask, i, j, color):
            if mask[i, j] == color:
                mask[i, j] = 254
                if valid_row(i-1):
                    bfs(mask, i-1, j, color)
                if valid_row(i+1):
                    bfs(mask, i+1, j, color)
                if valid_col(j-1):
                    bfs(mask, i, j-1, color)
                if valid_col(j+1):
                    bfs(mask, i, j+1, color)
        # color = 0

        masks = []

        for i in range(m):
            for j in range(n):
                if mask[i, j] != 0:
                    color = mask[i, j]
                    bfs(mask, i, j, color)
                    new_mask = 255 * (mask == 254)
                    masks.append(new_mask)
                    mask[mask == 254] = 0
        
        return masks
    
    masks = detect_islands(mask)

    if destination:
    
        if not os.path.exists(destination):
            os.mkdir(destination)
        
        name, extension = get_name_and_extension(mask_path)
        for i, mask in enumerate(masks):
            cv2.imwrite(destination+name+f"_{i}"+extension, mask)

    return masks



def seperate_masks_into_objects(source, destination):
    if destination:
        if not os.path.exists(destination):
            os.mkdir(destination)
    if not os.path.isdir(source):
        return seperate_a_mask_into_objects(source, destination)
    else:
        mask_names = [file for file in os.listdir(source) if not file.startswith(".")]
        ans = []
        for name in mask_names:
            ans += seperate_a_mask_into_objects(os.path.join(source, name), destination)
        return ans


if __name__ == "__main__":
    seperate_masks_into_objects(args.source, args.destination)