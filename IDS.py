#Have to implement and train IDS here
import transform
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, LSTM
from keras.layers import Conv1D, MaxPooling1D
from keras.optimizers import SGD
import tensorflow.compat.v1 as tf
import os
import torch

mnist = transform.data_importer(one_hot=False)
def train(data, file_name, params, num_epochs=50, batch_size=128, train_temp=1, init=None):
    """
    Standard neural network training procedure.
    """
    model = Sequential()

    train_data= data.train.samples.values.reshape(data.train.samples.shape[0], data.train.samples.shape[1], 1)
    validation_data = data.validation.samples.values.reshape(data.validation.samples.shape[0], data.validation.samples.shape[1], 1)
    #print(train_data.shape)
    #print(train_data.shape[1:])
    print(data.train.labels[0:5])

    model.add(Conv1D(params[0], 3,input_shape=train_data.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv1D(params[1], 3))
    model.add(Activation('relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(LSTM(params[2], dropout=0.1))
    model.add(Dropout(0.1))
    model.add(Dense(params[3]))
    model.add(Activation('softmax'))

    # def fn(correct, predicted):
    #     return tf.nn.softmax_cross_entropy_with_logits(labels=correct,
    #                                                    logits=predicted / train_temp)
    #
    # sgd = SGD(lr=0.005, decay=1e-6, momentum=0.9, nesterov=True)

    # model.compile(loss=fn,
    #               optimizer=sgd,
    #               metrics=['accuracy'])
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer="adam",
                  metrics=['accuracy'])

    # model.fit(xtrain, ytrain, batch_size=16, epochs=100, verbose=0)
    model.fit(train_data, data.train.labels,
              batch_size=batch_size,
              validation_data=(validation_data, data.validation.labels),
              epochs=num_epochs,
              shuffle=True)

    if file_name != None:
        # model.save(file_name)
        if not os.path.isdir(file_name):
            os.makedirs(file_name)
        model.save_weights(file_name + "/weight.h5")

    return model

train(mnist, "models/ids", [32, 64, 70, 70], num_epochs=50)