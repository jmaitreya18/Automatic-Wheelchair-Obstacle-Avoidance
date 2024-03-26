# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f9nnNvemB87xcOYoe1lBUYJmvsgaONZN
"""

import cv2
import numpy as np
import os
from google.colab import drive
drive.mount('/content/drive')
os.makedirs('/content/drive/MyDrive/synthetic_data/train', exist_ok=True)
os.makedirs('/content/drive/MyDrive/synthetic_data/validation', exist_ok=True)

# Create directories if they don't exist
os.makedirs('synthetic_data/train', exist_ok=True)
os.makedirs('synthetic_data/validation', exist_ok=True)
import shutil

shutil.make_archive('synthetic_data', 'zip', 'synthetic_data')

# Function to create synthetic obstacle images
def create_obstacle_image(size=(224, 224), num_obstacles=5):
    image = np.ones((size[0], size[1], 3), dtype=np.uint8) * 255  # White background
    for _ in range(num_obstacles):
        obstacle_size = np.random.randint(20, 50)  # Random obstacle size
        obstacle_color = tuple(np.random.randint(0, 256, size=3).tolist())  # Random obstacle color in BGR format
        obstacle_pos = (np.random.randint(0, size[1] - obstacle_size), np.random.randint(0, size[0] - obstacle_size))  # Corrected position
        cv2.rectangle(image, obstacle_pos, (obstacle_pos[0] + obstacle_size, obstacle_pos[1] + obstacle_size),
                      obstacle_color, -1)
    return image

# Generate synthetic data for training and validation
for i in range(100):  # Generate 100 images for training
    image = create_obstacle_image()
    cv2.imwrite(f'/content/drive/MyDrive/synthetic_data/train/obstacle_{i}.jpg', image)

for i in range(20):  # Generate 20 images for validation
    image = create_obstacle_image()
    cv2.imwrite(f'/content/drive/MyDrive/synthetic_data/obstacle_{i}.jpg', image)

import cv2
import numpy as np
import os
from google.colab import drive
drive.mount('/content/drive')

# Define the path to the directory where you want to save the synthetic data on Google Drive
drive_path = '/content/drive/MyDrive/synthetic_data/'

# Create directories if they don't exist on Google Drive
os.makedirs(drive_path + 'train', exist_ok=True)
os.makedirs(drive_path + 'validation', exist_ok=True)

# Function to create synthetic obstacle images
def create_obstacle_image(size=(224, 224), num_obstacles=5):
    image = np.ones((size[0], size[1], 3), dtype=np.uint8) * 255  # White background
    for _ in range(num_obstacles):
        obstacle_size = np.random.randint(20, 50)  # Random obstacle size
        obstacle_color = tuple(np.random.randint(0, 256, size=3).tolist())  # Random obstacle color in BGR format
        obstacle_pos = (np.random.randint(0, size[1] - obstacle_size), np.random.randint(0, size[0] - obstacle_size))  # Corrected position
        cv2.rectangle(image, obstacle_pos, (obstacle_pos[0] + obstacle_size, obstacle_pos[1] + obstacle_size),
                      obstacle_color, -1)
    return image

# Generate synthetic data for training and validation
for i in range(100):  # Generate 100 images for training
    image = create_obstacle_image()
    cv2.imwrite(drive_path + f'train/obstacle_{i}.jpg', image)

for i in range(20):  # Generate 20 images for validation
    image = create_obstacle_image()
    cv2.imwrite(drive_path + f'validation/obstacle_{i}.jpg', image)

import cv2
import numpy as np
import os
from google.colab import drive
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Mount Google Drive
drive.mount('/content/drive')

# Define the path to the directory where you want to save the synthetic data on Google Drive
drive_path = '/content/drive/MyDrive/synthetic_data/'

# Create directories if they don't exist on Google Drive
os.makedirs(drive_path + 'train', exist_ok=True)
os.makedirs(drive_path + 'validation', exist_ok=True)

# Function to create synthetic obstacle images
def create_obstacle_image(size=(224, 224), num_obstacles=5):
    image = np.ones((size[0], size[1], 3), dtype=np.uint8) * 255  # White background
    for _ in range(num_obstacles):
        obstacle_size = np.random.randint(20, 50)  # Random obstacle size
        obstacle_color = tuple(np.random.randint(0, 256, size=3).tolist())  # Random obstacle color in BGR format
        obstacle_pos = (np.random.randint(0, size[1] - obstacle_size), np.random.randint(0, size[0] - obstacle_size))  # Corrected position
        cv2.rectangle(image, obstacle_pos, (obstacle_pos[0] + obstacle_size, obstacle_pos[1] + obstacle_size),
                      obstacle_color, -1)
    return image

# Generate synthetic data for training and validation
for i in range(100):  # Generate 100 images for training
    image = create_obstacle_image()
    cv2.imwrite(f'{drive_path}/train/obstacle_{i}.jpg', image)

for i in range(20):  # Generate 20 images for validation
    image = create_obstacle_image()
    cv2.imwrite(f'{drive_path}/validation/obstacle_{i}.jpg', image)

# Load synthetic data
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    f'{drive_path}/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary')

# Define model architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // 32,
    epochs=10
)

# Save trained model
model.save('/content/drive/MyDrive/synthetic_model.h5')

import os
from google.colab import drive
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Mount Google Drive
drive.mount('/content/drive')

# Define the path to the directory where you saved the synthetic data on Google Drive
drive_path = '/content/drive/MyDrive/synthetic_data/'

# List the contents of the train and validation directories
print("Contents of the training directory:")
print(os.listdir(drive_path + 'train'))
print("Contents of the validation directory:")
print(os.listdir(drive_path + 'validation'))

# Load synthetic data
train_datagen = ImageDataGenerator(rescale=1./255)

# Generate the ImageDataGenerator objects for training and validation data
train_generator = train_datagen.flow_from_directory(
    drive_path + 'train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# Print some diagnostic information
print("Number of training samples:", train_generator.samples)
print("Number of classes:", train_generator.num_classes)

# Print the class indices
print("Class indices:", train_generator.class_indices)

import cv2
import numpy as np
import os
from google.colab import drive
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Mount Google Drive
drive.mount('/content/drive')

# Define the path to the directory where you saved the synthetic data on Google Drive
drive_path = '/content/drive/MyDrive/synthetic_data/'

# Load synthetic data
train_datagen = ImageDataGenerator(rescale=1./255)

# Define the directory paths for training and validation data
train_dir = os.path.join(drive_path, 'train')
validation_dir = os.path.join(drive_path, 'validation')
import pandas as pd

# Create a dataframe with file paths and labels
train_files = [drive_path + 'train/' + filename for filename in os.listdir(drive_path + 'train')]
validation_files = [drive_path + 'validation/' + filename for filename in os.listdir(drive_path + 'validation')]

train_df = pd.DataFrame({'filename': train_files, 'label': 'obstacle'})
validation_df = pd.DataFrame({'filename': validation_files, 'label': 'obstacle'})

# Load data using ImageDataGenerator.flow_from_dataframe
train_generator = train_datagen.flow_from_dataframe(
    train_df,
    x_col='filename',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

validation_generator = train_datagen.flow_from_dataframe(
    validation_df,
    x_col='filename',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)


# Define model architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // 32,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // 32
)

# Save trained model
model.save('/content/drive/MyDrive/synthetic_model.h5')

import cv2
import numpy as np
import os
from google.colab import drive
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Mount Google Drive
drive.mount('/content/drive')

# Define the path to the directory where you want to save the synthetic data on Google Drive
drive_path = '/content/drive/MyDrive/synthetic_data/'

# Create directories if they don't exist on Google Drive
os.makedirs(drive_path + 'train/obstacle', exist_ok=True)
os.makedirs(drive_path + 'train/no_obstacle', exist_ok=True)
os.makedirs(drive_path + 'validation/obstacle', exist_ok=True)
os.makedirs(drive_path + 'validation/no_obstacle', exist_ok=True)

# Function to create synthetic obstacle images
def create_synthetic_image(size=(224, 224), num_obstacles=5, with_obstacle=True):
    image = np.ones((size[0], size[1], 3), dtype=np.uint8) * 255  # White background

    # Add obstacles if specified
    if with_obstacle:
        for _ in range(num_obstacles):
            obstacle_size = np.random.randint(20, 50)  # Random obstacle size
            obstacle_color = tuple(np.random.randint(0, 256, size=3).tolist())  # Random obstacle color in BGR format
            obstacle_pos = (np.random.randint(0, size[1] - obstacle_size), np.random.randint(0, size[0] - obstacle_size))  # Corrected position
            cv2.rectangle(image, obstacle_pos, (obstacle_pos[0] + obstacle_size, obstacle_pos[1] + obstacle_size),
                          obstacle_color, -1)

    return image

# Generate synthetic data for training and validation
for i in range(100):  # Generate 100 images with obstacles for training
    image = create_synthetic_image(with_obstacle=True)
    cv2.imwrite(f'{drive_path}/train/obstacle/obstacle_{i}.jpg', image)

for i in range(20):  # Generate 20 images with obstacles for validation
    image = create_synthetic_image(with_obstacle=True)
    cv2.imwrite(f'{drive_path}/validation/obstacle/obstacle_{i}.jpg', image)

for i in range(100):  # Generate 100 images without obstacles for training
    image = create_synthetic_image(with_obstacle=False)
    cv2.imwrite(f'{drive_path}/train/no_obstacle/no_obstacle_{i}.jpg', image)

for i in range(20):  # Generate 20 images without obstacles for validation
    image = create_synthetic_image(with_obstacle=False)
    cv2.imwrite(f'{drive_path}/validation/no_obstacle/no_obstacle_{i}.jpg', image)

# Load synthetic data using ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    f'{drive_path}/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

validation_generator = train_datagen.flow_from_directory(
    f'{drive_path}/validation',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# Define model architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // 32,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // 32
)

# Save trained model
model.save('/content/drive/MyDrive/synthetic_model.h5')

model.evaluate(validation_generator)

import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('/content/drive/MyDrive/synthetic_model.h5')

# Function to preprocess images
def preprocess_image(image):
    # Resize image to match model input size (224x224)
    resized_image = cv2.resize(image, (224, 224))
    # Normalize pixel values to [0, 1]
    normalized_image = resized_image / 255.0
    # Expand dimensions to match model input shape (add batch dimension)
    preprocessed_image = np.expand_dims(normalized_image, axis=0)
    return preprocessed_image

# Function to perform inference on the captured frame
def perform_inference(frame):
    # Preprocess the captured frame
    preprocessed_frame = preprocess_image(frame)
    # Perform inference using the loaded model
    predictions = model.predict(preprocessed_frame)
    # Assuming binary classification, get the predicted class label
    predicted_class = "obstacle" if predictions[0][0] > 0.5 else "no obstacle"
    # Display the predicted class label on the frame
    cv2.putText(frame, predicted_class, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame

# Capture video from the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Perform inference on the captured frame
    frame_with_predictions = perform_inference(frame)

    # Display the frame with predictions
    cv2.imshow('Camera Feed', frame_with_predictions)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()