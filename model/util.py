from tensorflow.keras.preprocessing.image import ImageDataGenerator


def img_to_dataset(
    train_path, test_path, batch_size, image_size, num_classes
):

    datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=0.2,
    )

    class_mode = 'binary' if num_classes == 2 else 'categorical'
    train_generator = datagen.flow_from_directory(
        train_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode=class_mode,
        subset='training',
        shuffle=True,
        seed=42
    )

    validation_generator = datagen.flow_from_directory(
        train_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode=class_mode,
        subset='validation',
        shuffle=True,
        seed=42
    )

    test_generator = datagen.flow_from_directory(
        test_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode=class_mode,
        subset='validation',
        shuffle=True,
        seed=42
    )

    return train_generator, validation_generator, test_generator