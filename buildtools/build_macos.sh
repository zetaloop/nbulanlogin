#!/bin/bash

cd "$(dirname "$0")"

# Use virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
python3 -m pip install -U pip setuptools
pip install -U requests sv_ttk pyinstaller

# PyInstaller build the project
pyinstaller --onefile --icon=../lanlogin.icns --add-data "../lanlogin.png:." --collect-data sv_ttk --distpath . --workpath build ../lanlogin.py

# Clean trash
if [ -d "venv" ]; then
    rm -rf venv
fi
if [ -d "dist" ]; then
    rm -rf dist
fi
if [ -d "build" ]; then
    rm -rf build
fi
if [ -d "__pycache__" ]; then
    rm -rf __pycache__
fi
if [ -f "lanlogin.spec" ]; then
    rm lanlogin.spec
fi

echo
echo "Build completed."
