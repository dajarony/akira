#!/bin/bash
# Akira SASE Cyberwar MVP - Installation Script

set -e

echo "🚀 Akira SASE Cyberwar MVP - Installation Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root
if [[  -eq 0 ]]; then
   echo -e "❌ This script should not be run as root"
   exit 1
fi

# Check Python version
echo -e "🔍 Checking Python version..."
python_version=
required_version="3.11"

if [ "" != "" ]; then
    echo -e "❌ Python 3.11+ required. Found: "
    exit 1
fi

echo -e "✅ Python  detected"

# Check if nmap is installed
echo -e "🔍 Checking for nmap..."
if ! command -v nmap &> /dev/null; then
    echo -e "⚠️ nmap not found. Installing..."
    
    # Detect OS and install nmap
    if [[ "" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y nmap
        elif command -v yum &> /dev/null; then
            sudo yum install -y nmap
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y nmap
        else
            echo -e "❌ Unable to install nmap automatically. Please install manually."
            exit 1
        fi
    elif [[ "" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install nmap
        else
            echo -e "❌ Homebrew not found. Please install nmap manually."
            exit 1
        fi
    else
        echo -e "❌ Unsupported OS. Please install nmap manually."
        exit 1
    fi
else
    echo -e "✅ nmap found"
fi

# Create virtual environment
echo -e "🏗️ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo -e "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "⚙️ Creating .env file..."
    cp .env.example .env
    echo -e "⚠️ Please edit .env file with your API keys and configuration"
fi

# Create necessary directories
echo -e "📁 Creating directories..."
mkdir -p logs mapa-global cambios

# Set permissions
echo -e "🔒 Setting permissions..."
chmod +x main.py

# Create firebase credentials placeholder
if [ ! -f firebase-credentials.json ]; then
    echo -e "🔥 Creating Firebase credentials placeholder..."
    echo '{}' > firebase-credentials.json
    echo -e "⚠️ Please replace firebase-credentials.json with your actual Firebase service account key"
fi

echo ""
echo -e "✅ Installation completed successfully!"
echo ""
echo -e "📋 Next steps:"
echo -e "1. Edit .env file with your API keys:"
echo -e "   nano .env"
echo ""
echo -e "2. Add your Firebase credentials:"
echo -e "   # Replace firebase-credentials.json with your service account key"
echo ""
echo -e "3. Start Akira:"
echo -e "   source venv/bin/activate"
echo -e "   python main.py"
echo ""
echo -e "4. Access the API:"
echo -e "   http://localhost:8000/docs"
echo ""
echo -e "🛡️⚔️ Akira SASE ready for ethical cybersecurity operations!"

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo ""
    echo -e "🐳 Docker detected. You can also run with Docker:"
    echo -e "   docker build -t akira-sase ."
    echo -e "   docker run -p 8000:8000 akira-sase"
fi

echo ""
echo -e "⚠️ ETHICAL USE ONLY - Never attack systems without explicit authorization"
