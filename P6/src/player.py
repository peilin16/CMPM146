from config import BOARD_SIZE, categories, image_size
from tensorflow.python.keras import models
import numpy as np
import os
import keras

class TicTacToePlayer:
    def get_move(self, board_state):
        raise NotImplementedError()

class UserInputPlayer:
    def get_move(self, board_state):
        inp = input('Enter x y:')
        try:
            x, y = inp.split()
            x, y = int(x), int(y)
            return x, y
        except Exception:
            return None

import random

class RandomPlayer:
    def get_move(self, board_state):
        positions = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board_state[i][j] is None:
                    positions.append((i, j))
        return random.choice(positions)

from matplotlib import pyplot as plt
from matplotlib.image import imread
import cv2

class UserWebcamPlayer:
    def _process_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        width, height = frame.shape
        size = min(width, height)
        pad = int((width-size)/2), int((height-size)/2)
        frame = frame[pad[0]:pad[0]+size, pad[1]:pad[1]+size]
        return frame
    
    def _access_webcam(self):
        import cv2
        cv2.namedWindow("preview")
        vc = cv2.VideoCapture(0)
        #vc.open()
        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
            frame = self._process_frame(frame)
        else:
            rval = False
        while rval:
            cv2.imshow("preview", frame)
            rval, frame = vc.read()
            frame = self._process_frame(frame)
            key = cv2.waitKey(20)
            if key == 13: # exit on Enter
                break

        vc.release()
        cv2.destroyWindow("preview")
        return frame
    """
    def _access_webcam(self):
       
        
        cv2.namedWindow("preview")
        
        # Try different camera indices if the first one fails
        frame = None
        for cam_index in range(3):  # Try cameras 0, 1, and 2
            vc = cv2.VideoCapture(cam_index)
            if vc.isOpened():
                rval, frame = vc.read()
                if rval:
                    break
            vc.release()  # Close if not working
        
        if frame is None:
            print("[ERROR] No available webcam detected.")
            return None  # Return None instead of crashing

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        width, height = frame.shape
        size = min(width, height)
        pad = int((width - size) / 2), int((height - size) / 2)
        frame = frame[pad[0]:pad[0] + size, pad[1]:pad[1] + size]

        cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
        if key == 13:  # Exit on Enter
            vc.release()
            cv2.destroyWindow("preview")

        return frame
    """
    def _print_reference(self, row_or_col):
        print('reference:')
        for i, emotion in enumerate(categories):
            print('{} {} is {}.'.format(row_or_col, i, emotion))
    
    def _get_row_or_col_by_text(self):
        try:
            val = int(input())
            return val
        except Exception as e:
            print('Invalid position')
            return None
    
    def _get_row_or_col(self, is_row):
        try:
            row_or_col = 'row' if is_row else 'col'
            self._print_reference(row_or_col)
            img = self._access_webcam()
            emotion = self._get_emotion(img)
            if type(emotion) is not int or emotion not in range(len(categories)):
                print('Invalid emotion number {}'.format(emotion))
                return None
            print('Emotion detected as {} ({} {}). Enter \'text\' to use text input instead (0, 1 or 2). Otherwise, press Enter to continue.'.format(categories[emotion], row_or_col, emotion))
            inp = input()
            if inp == 'text':
                return self._get_row_or_col_by_text()
            return emotion
        except Exception as e:
            # error accessing the webcam, or processing the image
            raise e
    
    def _get_emotion(self, img) -> int:
        # Your code goes here
        #
        # img an np array of size NxN (square), each pixel is a value between 0 to 255
        # you have to resize this to image_size before sending to your model
        # to show the image here, you can use:
        # import matplotlib.pyplot as plt
        # plt.imshow(img, cmap='gray', vmin=0, vmax=255)
        # plt.show()
        #
        # You have to use your saved model, use resized img as input, and get one classification value out of it
        # The classification value should be 0, 1, or 2 for neutral, happy or surprise respectively

        # return an integer (0, 1 or 2), otherwise the code will throw an error
        # Handle case where no image is captured
        # 🔹 Handle case where no image is captured
        if img is None:
            print("[ERROR] No image captured from webcam.")
            return 0  # Default to 'Neutral'

        # 🔹 Show the captured image (for debugging)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
        plt.title("Captured Image (Preprocessing)")
        plt.show()

        # 🔹 Resize the image to match the model input size
        resized_img = cv2.resize(img, image_size)  # image_size should be (150, 150)
        resized_img = np.expand_dims(resized_img, axis=-1)  # Add channel dimension
        resized_img = np.expand_dims(resized_img, axis=0)   # Add batch dimension
        
        # 🔹 Normalize pixel values (scale from 0-255 to 0-1)
        resized_img = resized_img / 255.0

        # 🔹 Dynamically find the latest trained model
        model_dir = "results/"
        model_files = [f for f in os.listdir(model_dir) if f.endswith(".keras") and "basic_model" in f]
        
        if not model_files:
            print("[ERROR] No saved model found in results/. Ensure you trained and saved the model.")
            return 0  # Default to Neutral

        latest_model = os.path.join(model_dir, sorted(model_files)[-1])  # Get the newest model

        print(f"Loading model: {latest_model}")  # Debugging info

        # 🔹 Load the trained model
        model = models.load_model(latest_model)

         # 🔹 Ensure model is compiled before predicting
        model.compile()  # Some models require compilation before inference

        # 🔹 Debugging: Check Model Input Shape
        print(f"Model Input Shape: {model.input_shape}")
        print(f"Resized Image Shape: {resized_img.shape}")

        # 🔹 Make a prediction
        try:
            predictions = model.predict(resized_img)
            print(f"Predicted Probabilities: {predictions}")
            emotion_index = np.argmax(predictions)  # Returns 0, 1, or 2
            print(f"Predicted Emotion Index: {emotion_index}")
            return int(emotion_index)
        except Exception as e:
            print(f"[ERROR] Prediction failed: {e}")
            return 0  # Default to Neutral if prediction fails
    
    def get_move(self, board_state):
        row, col = None, None
        while row is None:
            row = self._get_row_or_col(True)
        while col is None:
            col = self._get_row_or_col(False)
        return row, col