"""
Dataset Preparation Script
Downloads and organizes PlantVillage Tomato Dataset for training
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """
    Create the required directory structure for the dataset
    """
    base_dir = Path('data/tomato_dataset')
    
    # Class names
    classes = [
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
    
    # Create train and val directories
    for split in ['train', 'val']:
        for class_name in classes:
            class_dir = base_dir / split / class_name
            class_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {class_dir}")
    
    print(f"\n✅ Directory structure created at: {base_dir}")
    return base_dir

def split_dataset(source_dir, train_ratio=0.8):
    """
    Split dataset into train and validation sets
    
    Args:
        source_dir: Directory containing the downloaded PlantVillage dataset
        train_ratio: Ratio of training data (default: 0.8)
    """
    import random
    
    source_path = Path(source_dir)
    base_dir = Path('data/tomato_dataset')
    
    if not source_path.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return
    
    # Find all tomato class directories
    tomato_classes = [d for d in source_path.iterdir() if d.is_dir() and 'Tomato' in d.name]
    
    print(f"\n📂 Found {len(tomato_classes)} tomato disease classes")
    
    for class_dir in tomato_classes:
        class_name = class_dir.name
        print(f"\n📁 Processing: {class_name}")
        
        # Get all images
        images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.JPG'))
        random.shuffle(images)
        
        # Calculate split point
        split_point = int(len(images) * train_ratio)
        
        train_images = images[:split_point]
        val_images = images[split_point:]
        
        print(f"   Total: {len(images)} | Train: {len(train_images)} | Val: {len(val_images)}")
        
        # Copy to train directory
        train_dir = base_dir / 'train' / class_name
        train_dir.mkdir(parents=True, exist_ok=True)
        for img in train_images:
            shutil.copy2(img, train_dir / img.name)
        
        # Copy to val directory
        val_dir = base_dir / 'val' / class_name
        val_dir.mkdir(parents=True, exist_ok=True)
        for img in val_images:
            shutil.copy2(img, val_dir / img.name)
    
    print(f"\n✅ Dataset split completed!")
    print(f"   Dataset location: {base_dir}")

def download_from_kaggle():
    """
    Download PlantVillage dataset from Kaggle
    """
    try:
        import kaggle
        
        print("📥 Downloading PlantVillage dataset from Kaggle...")
        print("   (This may take several minutes)")
        
        # Download dataset
        kaggle.api.dataset_download_files(
            'arjuntejaswi/plant-village',
            path='data/plantvillage_download',
            unzip=True
        )
        
        print("✅ Download completed!")
        return 'data/plantvillage_download'
        
    except Exception as e:
        print(f"❌ Error downloading from Kaggle: {e}")
        print("\n💡 Manual Download Instructions:")
        print("   1. Visit: https://www.kaggle.com/datasets/arjuntejaswi/plant-village")
        print("   2. Click 'Download' button")
        print("   3. Extract the zip file")
        print("   4. Run this script with --source flag:")
        print("      python prepare_dataset.py --source /path/to/extracted/dataset")
        return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Prepare tomato dataset for training')
    parser.add_argument('--source', type=str, help='Path to downloaded PlantVillage dataset')
    parser.add_argument('--download', action='store_true', help='Download dataset from Kaggle')
    parser.add_argument('--train-ratio', type=float, default=0.8, help='Training data ratio (default: 0.8)')
    
    args = parser.parse_args()
    
    print("\n" + "🍅"*30)
    print("TOMATO DATASET PREPARATION")
    print("🍅"*30 + "\n")
    
    # Create directory structure
    base_dir = create_directory_structure()
    
    # Download or use provided source
    if args.download:
        source_dir = download_from_kaggle()
        if source_dir:
            split_dataset(source_dir, args.train_ratio)
    elif args.source:
        split_dataset(args.source, args.train_ratio)
    else:
        print("\n📋 Next Steps:")
        print("="*60)
        print("Option 1: Download from Kaggle automatically")
        print("  python prepare_dataset.py --download")
        print("\nOption 2: Use manually downloaded dataset")
        print("  python prepare_dataset.py --source /path/to/plantvillage")
        print("\n💡 To download manually:")
        print("  1. Visit: https://www.kaggle.com/datasets/arjuntejaswi/plant-village")
        print("  2. Download and extract")
        print("  3. Run with --source flag")
        print("="*60)
    
    print("\n✅ Preparation complete!")
    print(f"\nDataset ready at: {base_dir}")
    print("\n📝 Next step: Run training")
    print("  python train.py")
    print("\n" + "🍅"*30 + "\n")

if __name__ == '__main__':
    main()
