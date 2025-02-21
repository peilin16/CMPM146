from keras.utils import image_dataset_from_directory
#from tensorflow.python.keras.applications.mobilenet_v2 import preprocess_input 
from config import train_directory, test_directory, image_size, batch_size, validation_split
import os
def _split_data(train_directory, test_directory, batch_size, validation_split):

    print('train dataset:')
    train_dataset, validation_dataset = image_dataset_from_directory(
        train_directory,
        label_mode='categorical',
        color_mode='rgb',
        batch_size=batch_size,
        image_size=image_size,
        validation_split=validation_split,
        subset="both",
        seed=47
    )


    print('test dataset:')
    test_dataset = image_dataset_from_directory(
        test_directory,
        label_mode='categorical',
        color_mode='rgb',
        batch_size=batch_size,
        image_size=image_size,
        shuffle=False
    )

    return train_dataset, validation_dataset, test_dataset

def get_datasets():
    train_dataset, validation_dataset, test_dataset = \
        _split_data(train_directory, test_directory, batch_size, validation_split)
    return train_dataset, validation_dataset, test_dataset

def get_transfer_datasets():
    # Your code replaces this by loading the dataset
    # you can use image_dataset_from_directory, similar to how the _split_data function is using it
    train_dataset, validation_dataset, test_dataset = None, None, None
    train_dataset = image_dataset_from_directory(
        'transfer_train',
        label_mode='categorical',
        color_mode='rgb',
        batch_size=batch_size,
        image_size=(150,150),
        validation_split=validation_split,
        subset="training",
        seed=47
    )
    validation_dataset = image_dataset_from_directory(
        'transfer_train',
        label_mode='categorical',
        color_mode='rgb',
        batch_size=batch_size,
        image_size=(150,150),
        validation_split=validation_split,
        subset="validation",
        seed=47
    )
    test_dataset = image_dataset_from_directory(
        'transfer_test',
        label_mode='categorical',
        color_mode='rgb',
        batch_size=batch_size,
        image_size=(150,150),
        shuffle=False
    )
    
    return train_dataset, validation_dataset, test_dataset