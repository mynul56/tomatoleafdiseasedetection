#!/bin/bash

# Tomato Leaf Disease Detection - Quick Start Script

echo "🍅 Tomato Leaf Disease Detection App"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Flutter is installed
echo "Checking Flutter installation..."
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed or not in PATH"
    echo "Please install Flutter from https://flutter.dev"
    exit 1
fi

echo "✅ Flutter found: $(flutter --version | head -n 1)"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing Flutter dependencies..."
flutter pub get

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "Setup complete! 🎉"
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Start your backend server:"
echo "   cd /home/mynul-islam/projects/backend"
echo "   python main.py"
echo ""
echo "2️⃣  Configure backend URL in lib/services/api_service.dart"
echo ""
echo "3️⃣  Run the app:"
echo "   flutter run"
echo ""
echo "4️⃣  Or run on specific device:"
echo "   flutter devices          # List devices"
echo "   flutter run -d <device>  # Run on specific device"
echo ""
echo "📖 For detailed instructions, see SETUP_GUIDE.md"
echo "======================================"
