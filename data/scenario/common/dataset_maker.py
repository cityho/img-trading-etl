import numpy as np
import h5py
import time
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical

from utils.args import check_settings
from utils.log import LOGGER
from utils.data import file_upload_to_s3
import gc

def img_to_dataset(setting):
    data_dir = setting["data_dir"]
    batch_size = setting["batch_size"]
    image_size = setting["img_size"]
    num_classes = setting["class_num"]

    datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=0.2,
    )

    class_mode = 'binary' if num_classes == 2 else 'categorical'
    train_generator = datagen.flow_from_directory(
        data_dir+"train",
        target_size=image_size,
        batch_size=batch_size,
        class_mode=class_mode,
        subset='training',
        shuffle=True,
        # seed=42
    )

    validation_generator = datagen.flow_from_directory(
        data_dir+"test",
        target_size=image_size,
        batch_size=batch_size,
        class_mode=class_mode,
        subset='validation',
        shuffle=True
    )

    return train_generator, validation_generator


def store_dataset_to_hdf(
        file_name, train_generator, validation_generator
):
    assert file_name.endswith(".h5"), "file_name extension should be .h5"
    LOGGER.info(f"START file making: {file_name}")
    train_file = file_name #.replace(".h5", "_train.h5")

    train_iter = 5
    val_rate = 0.2
    val_iter = int(train_iter * val_rate)
    with h5py.File(train_file, 'w') as file:
        train = [train_generator.next()[0] for _ in range(train_iter)]
        x_train = np.concatenate(train, axis=0)
        file.create_dataset('x_train', data=x_train)
        train = 0; gc.collect()
        time.sleep(10)

        train = [train_generator.next()[1] for _ in range(train_iter)]
        y_train = np.concatenate(train, axis=0)
        file.create_dataset('y_train', data=y_train)
        train = 0; gc.collect()
        time.sleep(10)

        x_val = [validation_generator.next()[0] for _ in range(val_iter)]
        x_val = np.concatenate(x_val, axis=0)
        file.create_dataset('x_test', data=x_val)
        time.sleep(10)

        y_val = [validation_generator.next()[1] for _ in range(val_iter)]
        y_val = np.concatenate(y_val, axis=0)
        file.create_dataset('y_test', data=y_val)
        time.sleep(10)

    LOGGER.info(f"END file making: {train_file}")

    file_upload_to_s3(train_file, train_file.replace("/locdisk/data/hoseung2/", ""))
    LOGGER.info(f"FILE UPLOADED ON S3")


def run(setting):
    check_settings(setting)
    train_generator, validation_generator = img_to_dataset(setting)
    store_dataset_to_hdf(
        setting["file_name"], train_generator, validation_generator
    )


if __name__ == '__main__':
    setting = {
        "data_dir": "/locdisk/data/hoseung2/scenario/jongga_tomorrow_trenary_kospi200_constituent/img/",
        "img_size": (400, 200),
        "file_name": "/locdisk/data/hoseung2/scenario/small_jongga_tomorrow_trenary_kospi200_constituent.h5",
        "batch_size": 100,
        "class_num": 3
    }
    run(setting)
