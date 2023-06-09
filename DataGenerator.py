import numpy as np
import keras
import cv2, os

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    
    ## 생성자 method
    def __init__(self, list_IDs, labels, batch_size=32, dim=(32,32,32), n_channels=1,
                 n_classes=10, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):  # 에포크 당 배치 수를 반환, 입력 데이터의 크기와 배치 크기를 기반으로 계산
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):  # 인덱스에 해당하는 배치 데이터를 생성하여 반환
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):  # 한번의 에포크가 끝나면 인덱스를 업데이트
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):  # ID list에 대한 실제 데이터 생성, 
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size, self.dim[0] * 4, self.dim[1] * 4, self.n_channels))

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            X[i] = np.load(ID)

            splited = ID.split('|')
            splited[-2] = 'y' + splited[-2][1:] # x_train -> y_train
            y_path = os.path.join(os.sep, *splited)

            # Store class
            y[i] = np.load(y_path)

        return X, y

# +
# class DataGenerator(keras.utils.Sequence):
#     'Generates data for Keras'

#     def __init__(self, list_IDs, labels, batch_size=32, dim=(32, 32, 3), n_channels=1, n_classes=10, shuffle=True):
#         'Initialization'
#         self.dim = dim
#         self.batch_size = batch_size
#         self.labels = labels
#         self.list_IDs = list_IDs
#         self.n_channels = n_channels
#         self.n_classes = n_classes
#         self.shuffle = shuffle
#         self.on_epoch_end()

#     def __len__(self):
#         'Denotes the number of batches per epoch'
#         return int(np.floor(len(self.list_IDs) / self.batch_size))

#     def __getitem__(self, index):
#         'Generate one batch of data'
#         indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
#         list_IDs_temp = [self.list_IDs[k] for k in indexes]
#         X, y = self.__data_generation(list_IDs_temp)
#         return X, y

#     def on_epoch_end(self):
#         'Updates indexes after each epoch'
#         self.indexes = np.arange(len(self.list_IDs))
#         if self.shuffle == True:
#             np.random.shuffle(self.indexes)

#     def __data_generation(self, list_IDs_temp):
#         'Generates data containing batch_size samples'
#         X = np.empty((self.batch_size, *self.dim, self.n_channels))
#         y = np.empty((self.batch_size, self.dim[0] * 4, self.dim[1] * 4, self.n_channels))

#         for i, ID in enumerate(list_IDs_temp):
#             X[i] = np.load(ID)
#             splited = ID.split('/')
#             splited[-2] = 'y' + splited[-2][1:]  # x_train -> y_train
#             y_path = os.path.join(os.sep, *splited)
#             y[i] = np.load(y_path)

#         return X, y
# -




