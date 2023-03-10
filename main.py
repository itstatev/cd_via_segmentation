import os
import cv2
import numpy as np
from modules.stitch.match_pairs import match_pairs
from modules.change_detection import Change
from tools.seperate_mask_into_objects import seperate_a_mask_into_objects
from modules.DeepLabV3_segmentation.model import createDeepLabv3
from modules.DeepLabV3_segmentation.DeepLabV3 import deeplabv3_segment


def main():
    img_dir = './images/'
    names = [file for file in sorted(os.listdir(os.path.join(img_dir + 'A/')))]
    model = createDeepLabv3()

    for name in names:
        img1 = cv2.imread(os.path.join(img_dir + 'A/' + name))
        img2 = cv2.imread(os.path.join(img_dir + 'B/' + name))

        mask_of_first_img = deeplabv3_segment(model, img1)
        mask_of_second_img = deeplabv3_segment(model, img2) 

        layers_of_first_img = seperate_a_mask_into_objects(mask_of_first_img)   
        layers_of_second_img = seperate_a_mask_into_objects(mask_of_second_img)

        keypoints = match_pairs([img1, img2]) 
        keypoints1, keypoints2, matches = keypoints[0], keypoints[1], keypoints[2]

        print(keypoints1)

        object_keypoints_A = []
        object_keypoints_B = []

        for a_layer in layers_of_first_img:
            keys = []
            for el in keypoints1:
                check = a_layer[el[1], el[0]]
                if not (check[0] < 50 and check[1] < 50 and check[2] < 50):
                    keys.append(keypoints1.index(el)) 
                object_keypoints_A.append(keys)

        for a_layer in layers_of_second_img:
            keys = []
            for el in keypoints2:
                check = a_layer[el[1], el[0]]
                if not (check[0] < 50 and check[1] < 50 and check[2] < 50):
                    keys.append(keypoints1.index(el)) 
                object_keypoints_B.append(keys)

        change = Change(keypoints1, matches, layers_of_first_img, layers_of_second_img, object_keypoints_A, object_keypoints_B)
        change.change_detection()

        # for a_layer in layers_of_first_img:
        #     for b_layer in layers_of_second_img:
        #         change = Change(keypoints1, matches, layers_of_first_img, layers_of_second_img, object_keypoints_A, object_keypoints_B)
        #         change.change_detection()

if __name__ == "__main__":
    main() 