#!/bin/bash

cd "$(dirname "$0")"

# Use virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
python3 -m pip install -U pip setuptools
pip install -U requests sv_ttk pyinstaller

# PyInstaller build the project
pyinstaller --onefile --icon=../lanlogin.png --add-data "../lanlogin.png:." --collect-data sv_ttk --distpath . --workpath build ../lanlogin.py

# Clean trash
[ -d "venv" ] && rm -rf venv
[ -d "dist" ] && rm -rf dist
[ -d "build" ] && rm -rf build
[ -d "__pycache__" ] && rm -rf __pycache__
[ -f "lanlogin.spec" ] && rm lanlogin.spec

echo
echo "Build completed."
