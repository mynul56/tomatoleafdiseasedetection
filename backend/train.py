"""
Training Script for Tomato Leaf Disease Detection
Using ResNet50 with Transfer Learning on PlantVillage Dataset
All 10 Tomato Disease Classes
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.0001

# Dataset paths (adjust these to your dataset location)
DATASET_DIR = 'data/tomato_dataset'
TRAIN_DIR = os.path.join(DATASET_DIR, 'train')
VAL_DIR = os.path.join(DATASET_DIR, 'val')

# Output model path
MODEL_SAVE_PATH = 'tomato_resnet50_model.h5'

# Class names (should match your dataset folder structure)
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

def create_data_generators():
    """
    Create data generators with augmentation for training
    """
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
    
    # Validation data (only rescaling)
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, val_generator

def build_model(num_classes):
    """
    Build ResNet50 model with transfer learning
    """
    print("\n" + "="*60)
    print("🏗️  Building ResNet50 Model with Transfer Learning")
    print("="*60)
    
    # Load ResNet50 with ImageNet weights (without top classification layer)
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=(*IMG_SIZE, 3)
    )
    
    # Freeze base model layers initially
    base_model.trainable = False
    
    print(f"✅ Loaded ResNet50 base model with ImageNet weights")
    print(f"   Total layers in base model: {len(base_model.layers)}")
    
    # Add custom classification head
    x = GlobalAveragePooling2D(name='global_avg_pool')(base_model.output)
    x = Dense(512, activation='relu', name='fc1')(x)
    x = Dropout(0.5, name='dropout1')(x)
    x = Dense(256, activation='relu', name='fc2')(x)
    x = Dropout(0.3, name='dropout2')(x)
    output = Dense(num_classes, activation='softmax', name='predictions')(x)
    
    # Create final model
    model = Model(inputs=base_model.input, outputs=output, name='ResNet50_Tomato')
    
    print(f"✅ Added custom classification head")
    print(f"   • Global Average Pooling")
    print(f"   • Dense(512) + Dropout(0.5)")
    print(f"   • Dense(256) + Dropout(0.3)")
    print(f"   • Dense({num_classes}) [Softmax]")
    print("="*60 + "\n")
    
    return model

def compile_model(model):
    """
    Compile the model with optimizer and loss function
    """
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    print("✅ Model compiled")
    print(f"   Optimizer: Adam (lr={LEARNING_RATE})")
    print(f"   Loss: Categorical Crossentropy")
    print(f"   Metrics: Accuracy, Top-3 Accuracy\n")
    
    return model

def create_callbacks():
    """
    Create training callbacks
    """
    callbacks = [
        # Save best model
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Early stopping
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate on plateau
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    print("✅ Training callbacks configured:")
    print("   • ModelCheckpoint (save best model)")
    print("   • EarlyStopping (patience=10)")
    print("   • ReduceLROnPlateau (factor=0.5, patience=5)\n")
    
    return callbacks

def plot_training_history(history):
    """
    Plot training history
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    axes[0].plot(history.history['accuracy'], label='Train Accuracy')
    axes[0].plot(history.history['val_accuracy'], label='Val Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True)
    
    # Plot loss
    axes[1].plot(history.history['loss'], label='Train Loss')
    axes[1].plot(history.history['val_loss'], label='Val Loss')
    axes[1].set_title('Model Loss')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Training history plot saved to 'training_history.png'")

def fine_tune_model(model, train_generator, val_generator):
    """
    Fine-tune the model by unfreezing some layers
    """
    print("\n" + "="*60)
    print("🔧 Fine-tuning: Unfreezing last layers of base model")
    print("="*60)
    
    # Unfreeze the last 20 layers of base model
    base_model = model.layers[0]
    base_model.trainable = True
    
    # Freeze all layers except the last 20
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE/10),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    print(f"✅ Unfroze last 20 layers")
    print(f"   Learning rate reduced to: {LEARNING_RATE/10}")
    print("="*60 + "\n")
    
    # Train for additional epochs
    history_fine = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=20,
        callbacks=create_callbacks(),
        verbose=1
    )
    
    return history_fine

def main():
    """
    Main training pipeline
    """
    print("\n" + "🍅"*30)
    print("TOMATO LEAF DISEASE DETECTION - MODEL TRAINING")
    print("🍅"*30 + "\n")
    
    print("Configuration:")
    print(f"  • Image Size: {IMG_SIZE}")
    print(f"  • Batch Size: {BATCH_SIZE}")
    print(f"  • Epochs: {EPOCHS}")
    print(f"  • Learning Rate: {LEARNING_RATE}")
    print(f"  • Number of Classes: {len(CLASS_NAMES)}")
    print(f"  • Model Save Path: {MODEL_SAVE_PATH}\n")
    
    # Check if dataset exists
    if not os.path.exists(TRAIN_DIR):
        print(f"❌ Training directory not found: {TRAIN_DIR}")
        print("\n📥 DATASET SETUP REQUIRED:")
        print("="*60)
        print("This script requires the PlantVillage Tomato Dataset.")
        print("\nDataset Structure Required:")
        print("data/tomato_dataset/")
        print("├── train/")
        print("│   ├── Tomato___Bacterial_spot/")
        print("│   ├── Tomato___Early_blight/")
        print("│   ├── Tomato___Late_blight/")
        print("│   ├── Tomato___Leaf_Mold/")
        print("│   ├── Tomato___Septoria_leaf_spot/")
        print("│   ├── Tomato___Spider_mites Two-spotted_spider_mite/")
        print("│   ├── Tomato___Target_Spot/")
        print("│   ├── Tomato___Tomato_Yellow_Leaf_Curl_Virus/")
        print("│   ├── Tomato___Tomato_mosaic_virus/")
        print("│   └── Tomato___healthy/")
        print("└── val/")
        print("    └── [same structure as train/]")
        print("\n🔗 Download PlantVillage Dataset:")
        print("   Kaggle: https://www.kaggle.com/datasets/arjuntejaswi/plant-village")
        print("   Or use: kaggle datasets download -d arjuntejaswi/plant-village")
        print("\n💡 After downloading:")
        print("   1. Extract the dataset")
        print("   2. Organize into train/val folders (80/20 split)")
        print("   3. Place in: data/tomato_dataset/")
        print("   4. Run this script again")
        print("="*60)
        return
    
    # Create data generators
    print("📊 Creating data generators...")
    train_generator, val_generator = create_data_generators()
    
    print(f"\n✅ Data generators created")
    print(f"   Training samples: {train_generator.samples}")
    print(f"   Validation samples: {val_generator.samples}")
    print(f"   Classes found: {len(train_generator.class_indices)}")
    print(f"   Class mapping: {train_generator.class_indices}\n")
    
    # Build model
    model = build_model(num_classes=len(CLASS_NAMES))
    
    # Compile model
    model = compile_model(model)
    
    # Print model summary
    print("📋 Model Summary:")
    print("="*60)
    model.summary()
    print("="*60 + "\n")
    
    # Create callbacks
    callbacks = create_callbacks()
    
    # Train model (transfer learning phase)
    print("🚀 Starting Training (Transfer Learning Phase)...")
    print("="*60)
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    print("\n✅ Transfer learning phase completed!")
    
    # Plot training history
    plot_training_history(history)
    
    # Optional: Fine-tuning phase (uncomment if you want to fine-tune)
    # print("\n🔧 Starting Fine-tuning Phase...")
    # history_fine = fine_tune_model(model, train_generator, val_generator)
    # print("\n✅ Fine-tuning completed!")
    
    # Evaluate final model
    print("\n📊 Evaluating final model on validation set...")
    results = model.evaluate(val_generator, verbose=1)
    
    print("\n" + "="*60)
    print("🎯 FINAL RESULTS")
    print("="*60)
    print(f"Validation Loss: {results[0]:.4f}")
    print(f"Validation Accuracy: {results[1]*100:.2f}%")
    if len(results) > 2:
        print(f"Top-3 Accuracy: {results[2]*100:.2f}%")
    print("="*60)
    
    print(f"\n✅ Model saved to: {MODEL_SAVE_PATH}")
    print(f"   Model size: {os.path.getsize(MODEL_SAVE_PATH) / (1024*1024):.2f} MB")
    
    print("\n🎉 Training completed successfully!")
    print("\n📝 Next Steps:")
    print("   1. Test the model with new images")
    print("   2. Deploy to production (app.py)")
    print("   3. Monitor performance and retrain if needed")
    print("\n" + "🍅"*30 + "\n")

if __name__ == '__main__':
    # Set random seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    # Run training
    main()
