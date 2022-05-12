# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter('ignore', FutureWarning)

from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from PIL import Image
import numpy as np
import json
import glob

class Dataset():

    def __init__(self):
        self.image_shape = (128, 128, 3)
        self.num_class = 4
        self.img = []

        files = glob.glob("./images/*.jpg")
        for i, file in enumerate(files):
            image = Image.open(file)
            self.img.append(image)


    def crop(self):

        data = json.load(open('./python/list.json', 'r'))['object_list']
        apex, img = [], []

        for i in range(len(data)):
            for j in ['left-top', 'right-bottom']:
                for k in ['x', 'y']:
                    apex.append(data[i][j][k])

        apex = np.asarray(apex)
        apex = np.reshape(apex, [len(data), 4])
        for im in self.img:
            for k in range(int(apex.size/4)):
                img.append(im.crop(apex[k]))

        self.img = img


    def save_img(self):
        for i, im in enumerate(self.img):
            print('processing ./trainImg/{:0>4}.jpg'.format(str(i)))
            im.save('./trainImg/{:0>4}.jpg'.format(str(i)))

    def get_batch(self):
        X = []
        Y = []
        image_size = 128
        for index, name in enumerate(['cover', 'zero', 'few', 'much']): 
            files = glob.glob("./trainImg/categorized/" + name + "/*.jpg")
            for i, file in enumerate(files):
                image = Image.open(file)
                image = image.convert("RGB")
                image = image.resize((image_size, image_size))
                data = np.asarray(image)
                X.append(data)
                Y.append(index)
        
        X = np.array(X)
        Y = np.array(Y)

        X = X.astype('float32')
        X = X / 255

        # conv label
        Y = np_utils.to_categorical(Y, 4)

        return train_test_split(X, Y, test_size=0.10)   #x_train, x_test, y_train, y_test



'''
if __name__ == '__main__':
    data = Dataset()
    data.crop()
    data.save_img()
'''