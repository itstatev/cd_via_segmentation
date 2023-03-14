import os
import cv2
import torchvision
import numpy as np
import matplotlib.pyplot as plt
from modules.stitch.match_pairs import match_pairs
from modules.change_detection import Change
from tools.seperate_mask_into_objects import seperate_a_mask_into_objects
from modules.DeepLabV3_segmentation.model import createDeepLabv3
from modules.DeepLabV3_segmentation.DeepLabV3 import deeplabv3_segment


def main():
    model = torchvision.models.segmentation.deeplabv3_resnet101(pretrained=True)

    img_dir = './images/'
    names = [file for file in sorted(os.listdir(os.path.join(img_dir + 'A/')))]
    print('names', names)
    for name in names:
        img1 = cv2.imread(os.path.join(img_dir + 'A/' + name))
        img2 = cv2.imread(os.path.join(img_dir + 'B/' + name))

        mask_of_first_img = deeplabv3_segment(model, img1)
        # plt.savefig('my_figure.png')
        # plt.imshow(mask_of_first_img)
        # plt.show()
        mask_of_second_img = deeplabv3_segment(model, img2) 
        layers_of_first_img = seperate_a_mask_into_objects(mask_of_first_img)   
        layers_of_second_img = seperate_a_mask_into_objects(mask_of_second_img)

        a = np.array(layers_of_first_img[0])
        print('unique', np.unique(a))

        keypoints = match_pairs([img1, img2]) 
        keypoints1, keypoints2, matches = keypoints['keypoints0'], keypoints['keypoints1'], keypoints['matches']
        keypoints1 = keypoints1[0]
        keypoints1 = [[int(j) for j in i] for i in keypoints1]
        keypoints2 = keypoints2[0]
        keypoints2 = [[int(j) for j in i] for i in keypoints2]
        matches = matches[0]

        object_keypoints_A = []
        object_keypoints_B = []

        for a_layer in layers_of_first_img:
            keys = []
            for el in keypoints1:
                check = a_layer[el[1], el[0]]
                if check == 255:
                    keys.append(keypoints1.index(el)) 
            object_keypoints_A.append(keys)

        print('object_keypoints_A', object_keypoints_A)
        
        for a_layer in layers_of_second_img:
            keys = []
            for el in keypoints2:
                # print('el', el)
                check = a_layer[el[1], el[0]]
                if check == 255:
                    keys.append(keypoints2.index(el)) 
            object_keypoints_B.append(keys)

        print('object_keypoints_B', object_keypoints_B)
        change = Change(keypoints1, matches, layers_of_first_img, layers_of_second_img, object_keypoints_A, object_keypoints_B)
        change.change_detection()

        print('lalalala', matches[object_keypoints_A[0]])

if __name__ == "__main__":
    main() 