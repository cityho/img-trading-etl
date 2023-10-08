import numpy as np
import pandas as pd
import tensorflow as tf

normalizer = tf.keras.layers.Normalization(axis=-1)

def get_basic_model():
  model = tf.keras.Sequential([
    normalizer,
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1)
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])
  return model


def y_label_convertor(original_list, l_size):
    max_value = l_size
    one_hot_list = []
    for value in original_list:
        one_hot = [0] * (max_value)
        one_hot[value] = 1
        one_hot_list.append(one_hot)

    return one_hot_list