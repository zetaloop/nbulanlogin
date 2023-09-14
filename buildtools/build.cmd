cd %~dp0

REM Remove the existing environment and build directories if they exist
if exist venv rmdir /s /q venv
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist LANLogin.spec del LANLogin.spec

REM Create a new virtual environment
python -m venv venv

REM Activate the virtual environment
call .\venv\Scripts\activate.bat

REM Install dependencies
python.exe -m pip install -U pip setuptools
pip install -U requests sv_ttk pywin32 pyinstaller

REM Run PyInstaller to build the project
pyinstaller --onefile --windowed --icon=../lanlogin.ico --add-data "../lanlogin.ico;." --collect-data sv_ttk --distpath . --workpath build  ../LANLogin.py

REM Remove the virtual environment, build, and PyInstaller bootloader directories
if exist venv rmdir /s /q venv
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
if exist LANLogin.spec del LANLogin.spec

echo.
echo Build completed.
pause