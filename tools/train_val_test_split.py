import random
import os
import shutil
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-p', "--proportions", type=str, required=True, help="proportions like x_train:x_val:x_test according which the data should be divided")
parser.add_argument('-s', "--source", type=str, required=True, help="data directory path whose children_dirs should contain files with same names")
parser.add_argument('-d', "--destination", type=str, default='', help="destination dir path where train, val, test dirs should be. Considered to be a source dir neighbour if not provided")

args = parser.parse_args()


def split(proportions, source_dir, destination_dir):
    if not destination_dir:
        slash_pos = source_dir[:-1].rfind("/")
        source_dir_name = source_dir[slash_pos+1:]
        destination_dir_name = (source_dir_name if source_dir_name[-1] != "/" else source_dir_name[:-1]) + "_splitted/"
        destination_dir = source_dir[:slash_pos+1] + destination_dir_name
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)

    phases = ["train/", "val/", "test/"]

    for phase in phases:
        if not os.path.exists(destination_dir+phase):
            os.mkdir(destination_dir+phase)

    train_proportion, val_proportion, test_proportion = proportions.split(":")
    train_proportion = int(train_proportion)
    val_proportion = int(val_proportion)
    test_proportion = int(test_proportion)

    for i, sub_dir in enumerate([sub for sub in os.listdir(source_dir) if os.path.isdir(source_dir+sub) and not sub.startswith(".")]):
        # print(sub_dir)
        if i == 0:
            data_names = [file for file in os.listdir(source_dir+sub_dir) if not file.startswith(".")]
            data_count = len(data_names)
            train_count = train_proportion * data_count // (train_proportion + val_proportion + test_proportion)
            val_count = val_proportion * data_count // (train_proportion + val_proportion + test_proportion)
            # test_count = data_count - train_count - val_count
            names = {"train/": [], "val/": [], "test/": []}
            names["train/"] = random.sample(data_names, train_count)
            names["val/"] = random.sample([name for name in data_names if name not in names["train/"]], val_count)
            names["test/"] = [name for name in data_names if name not in names["train/"] and name not in names["val/"]]
        # if not os.path.exists(destination_dir+sub_dir):
        #     os.mkdir(destination_dir+sub_dir)
        for phase in phases:
            if not os.path.exists(destination_dir+phase+sub_dir):
                os.mkdir(destination_dir+phase+sub_dir)
            for name in names[phase]:
                shutil.copyfile(source_dir+sub_dir+"/"+name, destination_dir+phase+sub_dir+"/"+name)



if __name__ == "__main__":
    split(args.proportions, args.source, args.destination)


