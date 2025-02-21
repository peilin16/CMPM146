from models.model import Model


from tensorflow.python.keras import Sequential,layers
from tensorflow.python.keras.optimizers import rmsprop_v2,adam_v2
from tensorflow.python.keras.layers import  Dropout
from keras.layers import BatchNormalization
from keras.layers import Rescaling
#from tensorflow.keras import Sequential, layers
#from tensorflow.keras.layers.experimental.preprocessing import Rescaling
#from tensorflow.keras.optimizers import RMSprop, Adam

class BasicModel(Model):
    def _define_model(self, input_shape, categories_count):
        # Your code goes here
        #通过 增加layers的方式提高准确度
        self.model = Sequential([
            Rescaling(1./255, input_shape=input_shape),
            layers.Conv2D(8, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(8, (3, 3), activation='relu'),
            layers.Conv2D(8, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),  # Helps prevent overfitting
            layers.Dense(categories_count, activation='softmax')  # Multi-class classification
        ]);
 
    
    def _compile_model(self):
        # Your code goes here
        # you have to compile the keras model, similar to the example in the writeup
        self.model.compile(
            optimizer=rmsprop_v2.RMSProp(learning_rate=0.0002),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        );