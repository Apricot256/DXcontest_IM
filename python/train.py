# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter('ignore', FutureWarning)

import os
from dataset import Dataset
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten, Dropout
from keras.layers.core import Dense
from keras.optimizers import SGD
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
import numpy as np


def network(input_shape, num_classes):

    '''
     model = Sequential()
    
    model.add(Conv2D(8, (3, 3), padding='same',input_shape=input_shape))
    model.add(Activation('tanh'))#
    model.add(MaxPooling2D(pool_size=(2, 2)))#
    model.add(Dropout(0.2))#
    model.add(Activation('tanh'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    
    model.add(Conv2D(16, (3, 3), padding='same'))
    model.add(Activation('tanh'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    
    model.summary()

    return model
    '''
    
    model = Sequential()
    model.add(Conv2D(input_shape=input_shape,filters=64,kernel_size=(3,3),padding="same", activation="relu"))
    model.add(Conv2D(filters=64,kernel_size=(3,3),padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
    model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
    model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
    model.add(Flatten())
    model.add(Dense(units=4096,activation="relu"))
    model.add(Dense(units=4096,activation="relu"))
    model.add(Dense(num_classes, activation="softmax"))

    model.summary()

    return model



class Trainer():

    def __init__(self, model, loss, optimizer):
        self.target = model
        self.target.compile(
            loss=loss, optimizer=optimizer, metrics=["accuracy"]
            )
        self.verbose = 1
        logdir = "log"
        self.log_dir = os.path.join(os.path.dirname(__file__), logdir)
        self.model_file_name = "model_file.hdf5"

    def train(self,x_train,y_train, batch_size, epochs, validation_split):
        if os.path.exists(self.log_dir):
            import shutil
            shutil.rmtree(self.log_dir)  # remove previous execution
        os.mkdir(self.log_dir)
    
        datagen = ImageDataGenerator(
            featurewise_center=False,  # set input mean to 0 over the dataset
            samplewise_center=False,  # set each sample mean to 0
            featurewise_std_normalization=False,  # divide inputs by std
            samplewise_std_normalization=False,  # divide each input by its std
            zca_whitening=False,  # apply ZCA whitening
            rotation_range=70,  # randomly rotate images in the range (0~180)
            width_shift_range=0.2,  # randomly shift images horizontally
            height_shift_range=0.2,  # randomly shift images vertically
            horizontal_flip=True,  # randomly flip images
            vertical_flip=False)  # randomly flip images

        # compute quantities for normalization (mean, std etc)
        datagen.fit(x_train)

        
        # split for validation data
        indices = np.arange(x_train.shape[0])
        np.random.shuffle(indices)
        validation_size = int(x_train.shape[0] * validation_split)
        x_train, x_valid = x_train[indices[:-validation_size], :], x_train[indices[-validation_size:], :]
        y_train, y_valid = y_train[indices[:-validation_size], :], y_train[indices[-validation_size:], :]
        

        model_path = os.path.join(self.log_dir, self.model_file_name)
        self.target.fit_generator(
            datagen.flow(x_train, y_train, batch_size=batch_size),
            steps_per_epoch = x_train.shape[0] // batch_size,
            epochs = epochs,
            validation_data = (x_valid, y_valid),
            callbacks = [
                TensorBoard(log_dir=self.log_dir),
                ModelCheckpoint(model_path, save_best_only=True)
            ],
            verbose=self.verbose,
            workers=4
        )


if __name__ == '__main__':

    dataset = Dataset()

    model = network((128, 128, 3), 4)
    x_train, x_test, y_train, y_test = dataset.get_batch()

    trainer = Trainer(model, loss = 'categorical_crossentropy', optimizer = SGD())
    trainer.train(x_train, y_train, batch_size = 16, epochs = 150, validation_split = 0.2) #best batch size is 8 or 16 ???

    model_arc_json = model.to_json()
    open("./result/model_architecture.json","w").write(model_arc_json)
    model.save_weights("./result/weights.hdf5")

    score = model.evaluate(x_test, y_test)
    print("val loss = ",score[0])
    print("val accuracy = ",score[1])