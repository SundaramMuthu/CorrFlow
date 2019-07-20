import os
import torch.utils.data as data
import torch
import torchvision.transforms as transforms
import random

import cv2
import numpy as np
import functional.utils.io as davis_io

M = 8

def squeeze_index(image, index_list):
    for i, index in enumerate(index_list):
        image[image == index] = i
    return image

def r_loader(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def a_loader(path):
    anno, _ = davis_io.imread_indexed(path)
    return anno

def r_prep(image):
    image = np.float32(image) / 255.0

    h,w = image.shape[0], image.shape[1]
    if w%M != 0: image = image[:,:-(w%M)]
    if h%M != 0: image = image[:-(h%M),]

    return transforms.ToTensor()(image)

def a_prep(image):
    h,w = image.shape[0], image.shape[1]
    if w % M != 0: image = image[:,:-(w%M)]
    if h % M != 0: image = image[:-(h%M),:]
    image = np.expand_dims(image, 0)

    return torch.Tensor(image).contiguous().long()

class myImageFloder(data.Dataset):
    def __init__(self, annos, jpegs, training=False):

        self.annos = annos
        self.jpegs = jpegs
        self.training = training

    def __getitem__(self, index):
        annos = self.annos[index]
        jpegs = self.jpegs[index]

        annotations = [a_prep(a_loader(anno)) for anno in annos]
        images_rgb = [r_prep(r_loader(jpeg)) for jpeg in jpegs]

        return images_rgb, annotations

    def __len__(self):
        return len(self.annos)