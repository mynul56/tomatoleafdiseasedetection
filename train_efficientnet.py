"""
Train EfficientNetB3 model for Tomato Leaf Disease Detection

This script fine-tunes EfficientNetB3 on a tomato disease dataset.
Dataset structure expected:
    dataset/
        train/
            Healthy/
            Early_Blight/
            Late_Blight/
            ... (other disease classes)
        validation/
            (same structure)
"""

import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# Dataset paths
DATASET_DIR = 'dataset'
TRAIN_DIR = os.path.join(DATASET_DIR, 'train')
VAL_DIR = os.path.join(DATASET_DIR, 'validation')

# Model save path
MODEL_SAVE_PATH = 'models/tomato_disease_model.h5'
os.makedirs('models', exist_ok=True)

# Class names (should match your dataset folders)
CLASS_NAMES = [
    'Bacterial_Spot',
    'Early_Blight',
    'Healthy',
    'Late_Blight',
    'Leaf_Mold',
    'Septoria_Leaf_Spot',
    'Spider_Mites',
    'Target_Spot',
    'Yellow_Leaf_Curl_Virus',
    'Mosaic_Virus'
]

def create_data_generators():
    """Create data generators with augmentation"""
    
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest'
    )
    
    # Validation data (no augmentation, only rescaling)
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    
    validation_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, validation_generator

def build_model(num_classes):
    """Build EfficientNetB3 model with custom head"""
    
    # Load EfficientNetB3 with ImageNet weights
    base_model = EfficientNetB3(
        include_top=False,
        weights='imagenet',
        input_shape=(*IMG_SIZE, 3)
    )
    
    # Freeze base model initially
    base_model.trainable = False
    
    # Build model
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model, base_model

def train_model():
    """Train the model"""
    
    print("=" * 60)
    print("🍅 Tomato Leaf Disease Detection - Model Training")
    print("=" * 60)
    
    # Create data generators
    print("\n📦 Loading dataset...")
    train_generator, validation_generator = create_data_generators()
    
    num_classes = len(train_generator.class_indices)
    print(f"   Classes found: {num_classes}")
    print(f"   Training samples: {train_generator.samples}")
    print(f"   Validation samples: {validation_generator.samples}")
    
    # Build model
    print("\n🏗️  Building EfficientNetB3 model...")
    model, base_model = build_model(num_classes)
    
    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    print(model.summary())
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=7,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Phase 1: Train with frozen base
    print("\n🎯 Phase 1: Training with frozen EfficientNetB3 base...")
    print("=" * 60)
    
    history1 = model.fit(
        train_generator,
        epochs=15,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Phase 2: Fine-tune top layers
    print("\n🔧 Phase 2: Fine-tuning top layers of EfficientNetB3...")
    print("=" * 60)
    
    # Unfreeze top layers
    base_model.trainable = True
    for layer in base_model.layers[:-50]:  # Freeze all except last 50 layers
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE/10),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    history2 = model.fit(
        train_generator,
        epochs=EPOCHS,
        initial_epoch=15,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate final model
    print("\n📊 Evaluating final model...")
    print("=" * 60)
    
    results = model.evaluate(validation_generator)
    print(f"\n✅ Final Validation Accuracy: {results[1]*100:.2f}%")
    print(f"✅ Final Top-3 Accuracy: {results[2]*100:.2f}%")
    
    print(f"\n💾 Model saved to: {MODEL_SAVE_PATH}")
    print("=" * 60)
    
    return model, history1, history2

if __name__ == '__main__':
    # Check if dataset exists
    if not os.path.exists(TRAIN_DIR):
        print(f"❌ Training directory not found: {TRAIN_DIR}")
        print("\nPlease organize your dataset as follows:")
        print("dataset/")
        print("  train/")
        print("    Healthy/")
        print("    Early_Blight/")
        print("    Late_Blight/")
        print("    ... (other classes)")
        print("  validation/")
        print("    (same structure)")
        exit(1)
    
    # Train model
    model, hist1, hist2 = train_model()
    
    print("\n✅ Training complete! You can now use the model in your backend.")
    print(f"   Model location: {MODEL_SAVE_PATH}")
