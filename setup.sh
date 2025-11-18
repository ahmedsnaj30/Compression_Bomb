#!/bin/bash
# Setup script for Compression Bomb DOS project

echo "[*] Setting up virtual environment..."

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "[+] Virtual environment created"
else
    echo "[+] Virtual environment already exists"
fi

# Activate venv
source venv/bin/activate

echo "[*] Installing dependencies..."
pip install --upgrade pip
pip install flask psutil requests matplotlib dash plotly

echo "[+] Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "    source venv/bin/activate"
echo ""
echo "To deactivate when done:"
echo "    deactivate"