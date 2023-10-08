import pandas as pd
import time
import os
import h5py
import numpy as np
import tensorflow as tf
import glob
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.layers import Input, LSTM, Conv2D, MaxPooling2D, Flatten, Dense, Concatenate

from model.util import img_to_dataset


def set_model():
    model = Sequential([
        layers.Reshape((400, 200, 3), input_shape=(400, 200, 3)),

        layers.Conv2D(32, (4, 10), padding="same"),
        layers.BatchNormalization(),
        layers.Activation(tf.keras.activations.softmax),
        layers.Dropout(0.5),  # Dropout 추가
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(32, (4, 10), padding="same"),
        layers.BatchNormalization(),
        layers.Activation(tf.nn.relu),
        layers.Dropout(0.5),  # Dropout 추가
        layers.MaxPooling2D(2),

        layers.Dense(256),
        layers.Activation(tf.keras.activations.softmax),

        layers.Conv2D(64, (2, 2), padding="same"),
        layers.BatchNormalization(),
        layers.Activation(tf.nn.relu),
        layers.MaxPooling2D((2, 2)),

        layers.Dense(256),
        layers.BatchNormalization(),
        layers.Activation(tf.nn.relu),

        layers.Flatten(),
        layers.Dense(256),
        layers.Activation(tf.nn.relu),

        layers.Dense(128),
        layers.Activation(tf.nn.relu),

        layers.Dense(128),
        layers.Activation(tf.nn.relu),

        layers.Dense(3, activation='softmax')  # 출력 뉴런 개수를 1로 변경하여 이진 분류 모델로 설정
    ])
    model.compile(
        optimizer='adam', loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Recall(), tf.keras.metrics.Precision()]
    )
    return model


def run_model(sceanrio):
    train_gen, val_gen, test_gen = img_to_dataset(
        f"/locdisk/data/hoseung2/scenario/{sceanrio}/img/train",
        f"/locdisk/data/hoseung2/scenario/{sceanrio}/img/test",
        batch_size=200,
        image_size=(400, 200),
        num_classes=3
    )
    model = set_model()
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        steps_per_epoch=len(train_gen),
        epochs=20
    )

    loss, accuracy, recall = model.evaluate(test_gen)
    print(f"Test loss: {loss:.4f}")
    print(f"Test accuracy: {accuracy:.4f}")
    print(f"Test recall: {recall:.4f}")
    model.save(f"/locdisk/data/hoseung2/model/{sceanrio}_cnn.h5")
    model.summary()

    tf.keras.utils.plot_model(model, show_shapes=True)

    plt.plot(history.history["loss"])
    plt.plot(history.history["val_loss"])
    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.title(f"{sceanrio}" )
    plt.show()


if __name__ == '__main__':
    sceanrio = "jongga_tomorrow_trenary_kosdaq150_constituent"
    run_model(
        sceanrio
    )

"""
Found 91200 images belonging to 3 classes.
Found 22798 images belonging to 3 classes.
Found 5065 images belonging to 3 classes.
"""