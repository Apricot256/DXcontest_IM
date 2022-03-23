# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter('ignore', FutureWarning)

from keras.models import model_from_json
import datetime
import numpy as np
from PIL import Image
import json
import os

model_arc_str = open("result/model_architecture.json").read()
model = model_from_json(model_arc_str)
model.load_weights("./result/weights.hdf5")
data = json.load(open('./python/list.json', 'r'))['object_list']

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
filename = now.strftime('%Y-%m-%d-%H')

os.system('scp -P 546 -i id_rsa cam@sus-dx.sora210.net:~/Image/' + filename + '.jpg ./temp/')

image_size = 128
label = ['cover', 'none', 'few', 'many']
image = Image.open('./temp/' + filename + '.jpg')
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

data = json.load(open('./temp/data.json', 'r'))  #["Camera 1"]

print("answers :", end='')

for i, array in enumerate(data["data"][0][1]):
    print(' ', label[answers[i]], end='')
    array['status'] = label[answers[i]]
print()

data = json.dumps(data)

with open('./temp/' + filename + '.json', 'w') as f:
    f.write(data)

os.system('scp -P 546 -i id_rsa ./temp/' + filename + '.json cam@sus-dx.sora210.net:~/inference/')
os.system('rm ./temp/*.jpg')