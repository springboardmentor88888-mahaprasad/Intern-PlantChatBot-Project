# ======================================================
# Plant Disease Detection System – Combined Clean Notebook
# (Training + Evaluation + Prediction Backend)
# ======================================================

# This notebook is a CLEAN, FINAL version created by
# combining your multiple Colab files into ONE correct pipeline.
# Suitable for: College submission, viva, backend demo.

# ------------------------------------------------------
# 1. Install & Import Libraries
# ------------------------------------------------------
!pip install -q tensorflow split-folders pillow

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing import image
import splitfolders

# ------------------------------------------------------
# 2. Dataset Paths
# ------------------------------------------------------
RAW_DATASET_PATH = "/content/plantvillage_raw/PlantVillage"
SPLIT_DATASET_PATH = "/content/plantvillage_split"

# ------------------------------------------------------
# 3. Train / Validation Split (only run once)
# ------------------------------------------------------
if not os.path.exists(SPLIT_DATASET_PATH):
    splitfolders.ratio(
        RAW_DATASET_PATH,
        output=SPLIT_DATASET_PATH,
        seed=42,
        ratio=(0.8, 0.2)
    )

TRAIN_DIR = os.path.join(SPLIT_DATASET_PATH, "train")
VAL_DIR = os.path.join(SPLIT_DATASET_PATH, "val")

# ------------------------------------------------------
# 4. Data Augmentation
# ------------------------------------------------------
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_gen = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

NUM_CLASSES = train_gen.num_classes
CLASS_NAMES = list(train_gen.class_indices.keys())

# ------------------------------------------------------
# 5. Model Architecture (Transfer Learning)
# ------------------------------------------------------
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ------------------------------------------------------
# 6. Training
# ------------------------------------------------------
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    ModelCheckpoint("plant_disease_model.h5", save_best_only=True)
]

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=20,
    callbacks=callbacks
)

# ------------------------------------------------------
# 7. Training Visualization
# ------------------------------------------------------
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title('Accuracy')

plt.subplot(1,2,2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Loss')

plt.show()

# ------------------------------------------------------
# 8. Save Class Labels (Backend Requirement)
# ------------------------------------------------------
with open("class_names.txt", "w") as f:
    for name in CLASS_NAMES:
        f.write(name + "\n")

# ------------------------------------------------------
# 9. Prediction Function (Backend Logic)
# ------------------------------------------------------
model = load_model("plant_disease_model.h5")

with open("class_names.txt") as f:
    class_names = [line.strip() for line in f]


def predict_disease(img_path):
    img = image.load_img(img_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)
    confidence = np.max(preds) * 100
    disease = class_names[np.argmax(preds)]

    return disease, confidence

# ------------------------------------------------------
# 10. Demo Prediction
# ------------------------------------------------------
# Example:
# disease, conf = predict_disease('/content/sample_leaf.jpg')
# print(f"Prediction: {disease} | Confidence: {conf:.2f}%")

print("✅ Combined training + backend notebook ready")