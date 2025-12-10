"""
Quick Training Script - Uses MobileNetV2 for faster training
This is optimized for speed while maintaining good accuracy
"""

import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Quick training configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.001

DATASET_DIR = 'data/tomato_dataset'
TRAIN_DIR = os.path.join(DATASET_DIR, 'train')
VAL_DIR = os.path.join(DATASET_DIR, 'val')
MODEL_SAVE_PATH = 'tomato_resnet50_model.h5'

CLASS_NAMES = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

def quick_train():
    """Fast training with MobileNetV2"""
    
    print("🚀 Quick Training Mode - Using MobileNetV2 for speed")
    print("   Expected training time: 30-60 minutes (with GPU)")
    print()
    
    if not os.path.exists(TRAIN_DIR):
        print("❌ Dataset not found!")
        print("   Run: python prepare_dataset.py --download")
        return
    
    # Data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    val_gen = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    print(f"✅ Found {train_gen.samples} training images")
    print(f"✅ Found {val_gen.samples} validation images")
    print()
    
    # Build model
    base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(*IMG_SIZE, 3))
    base.trainable = False
    
    x = GlobalAveragePooling2D()(base.output)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(len(CLASS_NAMES), activation='softmax')(x)
    
    model = Model(inputs=base.input, outputs=output)
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("✅ Model compiled")
    print()
    
    # Train
    print("🏋️  Training started...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=[
            keras.callbacks.ModelCheckpoint(
                MODEL_SAVE_PATH,
                save_best_only=True,
                monitor='val_accuracy'
            ),
            keras.callbacks.EarlyStopping(
                patience=5,
                restore_best_weights=True
            )
        ]
    )
    
    print(f"\n✅ Training complete!")
    print(f"   Model saved: {MODEL_SAVE_PATH}")
    
    # Evaluate
    results = model.evaluate(val_gen)
    print(f"\n📊 Validation Accuracy: {results[1]*100:.2f}%")
    
if __name__ == '__main__':
    quick_train()
