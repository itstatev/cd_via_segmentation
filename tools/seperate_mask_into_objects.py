import os 
import cv2
import argparse


def get_name_and_extension(filename):
    slash_pos = filename[:-1].rfind("/")
    dot_pos = filename.rfind(".")
    return filename[slash_pos+1:dot_pos], filename[dot_pos:]


def seperate_a_mask_into_objects(mask, mask_path, destination):
    if  mask is None:
        mask = cv2.imread(mask_path)
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    

    def detect_islands(mask):
        m, n = mask.shape
        valid_row = lambda x: 0 <= x < m
        valid_col = lambda x: 0 <= x < n

        def bfs(mask, i, j, color):
            assert color != 254
            queue = []
            queue.append((i, j))
            while queue:
                i, j = queue[-1]
                queue.pop()
                mask[i, j] = 254
                if valid_row(i-1) and mask[i-1, j] == color:
                    queue.append((i-1, j))
                if valid_row(i+1) and mask[i+1, j] == color:
                    queue.append((i+1, j))
                if valid_col(j-1) and mask[i, j-1] == color:
                    queue.append((i, j-1))
                if valid_col(j+1) and mask[i, j+1] == color:
                    queue.append((i, j+1))

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--source", type=str, required=True, help="path of the image or directory containing images")
    parser.add_argument('-d', "--destination", type=str, default='', help="path of the destination directory. \
                                                                        Not storing results if destination is not provided")
    args = parser.parse_args()
    seperate_masks_into_objects(args.source, args.destination)