from models.model import Model
from models.basic_model import BasicModel 
from tensorflow.python.keras import Sequential, layers,models
from tensorflow.python.keras.optimizers import rmsprop_v2,adam_v2
import numpy as np
#from tensorflow.python.keras.layers import Rescaling
#from tensorflow.python.keras.layers.
#from tensorflow.keras import Sequential, layers, models
#from tensorflow.keras.layers.experimental.preprocessing import Rescaling
#from tensorflow.keras.optimizers import RMSprop, Adam

class RandomModel(Model):
    def _define_model(self, input_shape, categories_count):
        # Your code goes here
        # you have to initialize self.model to a keras model
        # very similar to transfered_model.py, the only difference is that you should randomize the weights
        # load your basic model with keras's load_model function
        # freeze the weights of the loaded model to make sure the training doesn't affect them
        # (check the number of total params, trainable params and non-trainable params in your summary generated by train_transfer.py)
        # randomize the weights of the loaded model, possibly by using _randomize_layers
        # use this model by removing the last layer, adding dense layers and an output layer
 
        base_model = BasicModel(input_shape, categories_count).model   
 
        base_model = models.Model(inputs=base_model.input, outputs=base_model.layers[-2].output)
 
        self._randomize_layers(base_model) #对每一层采用随机分配
 
        for layer in base_model.layers:
            layer.trainable = False
 
        new_layers = Sequential([
            layers.Dense(128, activation='relu'),
            layers.Dense(categories_count, activation='softmax')  # Output layer for new task
        ])
 
        self.model = models.Sequential([
            base_model,
            new_layers
        ])
    
    def _compile_model(self):
        # Your code goes here
        # you have to compile the keras model, similar to the example in the writeup
        self.model.compile(
            optimizer=adam_v2.Adam(learning_rate=0.0005),  # Lower LR to avoid overfitting
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )#编译model


    @staticmethod
    def _randomize_layers(model):
        # Your code goes here

        # you can write a function here to set the weights to a random value
        # use this function in _define_model to randomize the weights of your loaded model
        for layer in model.layers:
            if hasattr(layer, 'kernel_initializer'):
                random_weights = [np.random.standard_normal(w.shape) for w in layer.get_weights()]
                layer.set_weights(random_weights)
