import scipy as sp
import os
import cv2
# from scipy.misc import imread
from scipy.signal.signaltools import correlate2d as c2d


def get(path):
    data = cv2.imread(path)
    data = sp.inner(data, [299, 587, 114]) / 1000.0
    return (data - data.mean()) / data.std()


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        images.append(folder + '/' + filename)

    return images


def get_image_from_subsection(file_list, path):
    new_file_list = file_list
    for file in file_list:
        if not '.jpg' in file and not '.png' in file:
            sub_folder = load_images_from_folder(file)

            if not sub_folder == []:
                new_file_list = new_file_list + get_image_from_subsection(sub_folder, path + '/' + file)
    if not new_file_list == []:
        return new_file_list

    return file_list


def delete_folder(file_list):
    result = []
    for file in file_list:
        if '.jpg' in file or '.png' in file:
            result.append(file)
    return result


file_list = get_image_from_subsection(load_images_from_folder("compare"), 'compare')
file_list = delete_folder(file_list)

# for image in file_list:


print(file_list)
print(len(file_list))
