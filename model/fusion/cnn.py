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

from model.util import img_to_dataset, store_checkpoints


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
    batch_size = 250
    train_gen, val_gen, test_gen = img_to_dataset(
        f"/locdisk/data/hoseung2/scenario/{sceanrio}/img/train",
        f"/locdisk/data/hoseung2/scenario/{sceanrio}/img/test",
        batch_size=batch_size,
        image_size=(400, 200),
        num_classes=3
    )
    model = set_model()
    checkpoint_path = "/locdisk/data/hoseung2/model/%s_cnn/cp-{epoch:04d}.ckpt" % (sceanrio)
    cp_callback = store_checkpoints(checkpoint_path, batch_size)
    model.save_weights(checkpoint_path.format(epoch=0))

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        callbacks=[cp_callback],
        steps_per_epoch=len(train_gen),
        epochs=30
    )
    model.save_weights(checkpoint_path.format(epoch=30))
    model.save(f"/locdisk/data/hoseung2/model/{sceanrio}_cnn.h5")
    model.save_weights(checkpoint_path.format(epoch=0))
    loss, accuracy, recall, precision = model.evaluate(test_gen)
    print(f"Test loss: {loss:.4f}")
    print(f"Test accuracy: {accuracy:.4f}")
    print(f"Test recall: {recall:.4f}")
    print(f"Test precision: {precision:.4f}")

    model.summary()

    # tf.keras.utils.plot_model(model, show_shapes=True)

    plt.plot(history.history["loss"])
    plt.plot(history.history["val_loss"])
    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.title(f"{sceanrio}")
    plt.legend()
    plt.show()
    plt.savefig(f"/locdisk/data/hoseung2/model/{sceanrio}_cnn.png")
    print(f"end! {sceanrio}")
    print(f"end! {sceanrio}")