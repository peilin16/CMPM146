from models.model import Model


from tensorflow.python.keras import Sequential,layers
from tensorflow.python.keras.optimizers import rmsprop_v2,adam_v2

#from tensorflow.python.keras.optimizers import RMSprop
#from tensorflow.keras import Sequential, layers
#from tensorflow.keras.layers.experimental.preprocessing import Rescaling
#from tensorflow.keras.optimizers import RMSprop, Adam

class BasicModel(Model):
    def _define_model(self, input_shape, categories_count):
        # Your code goes here
        
        # you have to initialize self.model to a keras model
        self.model = Sequential([
            layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
            layers.MaxPooling2D(2,2),

            layers.Conv2D(64, (3,3), activation='relu'),
            layers.MaxPooling2D(2,2),

            layers.Conv2D(128, (3,3), activation='relu'),
            layers.MaxPooling2D(2,2),

            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),  # Helps prevent overfitting
            layers.Dense(categories_count, activation='softmax')  # Multi-class classification
        ])
    
    def _compile_model(self):
        # Your code goes here
        # you have to compile the keras model, similar to the example in the writeup
        self.model.compile(
            
            optimizer=rmsprop_v2.RMSProp(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )