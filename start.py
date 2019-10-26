#-*- coding: UTF-8 -*-

import scipy as sp
import os
# import Image
from PIL import Image
from PIL import ImageChops

from sys import argv

import cv2
# from scipy.misc import imread
from scipy.signal.signaltools import correlate2d as c2d


def get(path):
    data = cv2.imread(path)
    return data


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


def byte_compare(image_file_1, image_file_2):
    image_1 = Image.open(image_file_1)
    image_2 = Image.open(image_file_2)
    return ImageChops.difference(image_1, image_2).getbbox() is None


script, first = argv
first = first.replace("\\", "/")
file_list = get_image_from_subsection(load_images_from_folder(first), first)
file_list = delete_folder(file_list)

i = 0
for image in file_list:
  if os.path.exists(image):
      stream_image = os.stat(image)
      j = 0
      for compare_image in file_list:
        if not i == j:
            if os.path.exists(compare_image):
                stream_compare_image = os.stat(compare_image)
                if stream_compare_image.st_size == stream_image.st_size:
                    # print(c2d(get(image), get(compare_image), mode='same'))
                    if byte_compare(image, compare_image):
                        os.remove(compare_image)

        j += 1
  i += 1

file_list = get_image_from_subsection(load_images_from_folder(first), first)
file_list = delete_folder(file_list)


print(file_list)
print(len(file_list))
