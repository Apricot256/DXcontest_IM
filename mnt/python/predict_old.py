# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter('ignore', FutureWarning)

from keras.models import model_from_json
import numpy as np
from PIL import Image
import json

model_arc_str = open("result/model_architecture.json").read()
model = model_from_json(model_arc_str)
model.load_weights("./result/weights.hdf5")
data = json.load(open('./python/list.json', 'r'))['object_list']

image_size = 128
label = ['cover', 'zero', 'few', 'much']
image = Image.open('./target.jpg')

apex, target = [], []

for i in range(len(data)):
    for j in ['left-top', 'right-bottom']:
        for k in ['x', 'y']:
            apex.append(data[i][j][k])

apex = np.asarray(apex)
apex = np.reshape(apex, [len(data), 4])

for i in range(int(apex.size/4)):
    tmp = image.crop(apex[i])
    tmp = tmp.convert("RGB")
    tmp = tmp.resize((image_size, image_size))
    tmp = np.asarray(tmp)
    target.append(tmp)

target = np.array(target)

target = target.astype('float32')
target = target / 255.0

y_predict = model.predict(target)
answers = y_predict.argmax(axis=-1)

print("answers :", end='')

for i in answers:
    print(' ', label[i], end='')
print()