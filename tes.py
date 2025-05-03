import tensorflow as tf
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Check if directories exist
train_dir = 'data/train'
test_dir = 'data/test'

if not os.path.exists(train_dir):
    raise FileNotFoundError(f"Training directory not found: {train_dir}")
if not os.path.exists(test_dir):
    raise FileNotFoundError(f"Test directory not found: {test_dir}")

# Check if directories contain subdirectories (class folders)
train_subdirs = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
test_subdirs = [d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))]

if not train_subdirs:
    raise ValueError(f"No class subdirectories found in {train_dir}")
if not test_subdirs:
    raise ValueError(f"No class subdirectories found in {test_dir}")

print(f"Found {len(train_subdirs)} classes in training directory: {train_subdirs}")
print(f"Found {len(test_subdirs)} classes in test directory: {test_subdirs}")

# Parameters
image_size = (48, 48)
batch_size = 32
epochs = 10

# Data generators with augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load data with verbose error handling
try:
    train_data = train_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='binary',
        color_mode='grayscale'
    )
    
    test_data = test_datagen.flow_from_directory(
        test_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='binary',
        color_mode='grayscale'
    )
    
    # Verify data was loaded
    if train_data.samples == 0:
        raise ValueError(f"No images found in training directory: {train_dir}")
    if test_data.samples == 0:
        raise ValueError(f"No images found in test directory: {test_dir}")
        
    print(f"Loaded {train_data.samples} training images")
    print(f"Loaded {test_data.samples} test images")
    
except Exception as e:
    print(f"Error loading data: {e}")
    raise

# CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')  # Binary classification
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Training with additional callbacks
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint('eye_state_cnn_checkpoint.h5', save_best_only=True)
]

history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=epochs,
    callbacks=callbacks
)

# Save model
model.save('eye_state_cnn.h5')

print("Training complete! Model saved as 'eye_state_cnn.h5'")
