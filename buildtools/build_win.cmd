cd %~dp0

REM Clean trash
if exist venv rmdir /s /q venv
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist lanlogin.spec del lanlogin.spec

REM Use virtual environment
python -m venv venv
call .\venv\Scripts\activate.bat

REM Install dependencies
python.exe -m pip install -U pip setuptools
pip install -U requests sv_ttk pywin32 pyinstaller

REM PyInstaller build the project
pyinstaller --onefile --icon=../lanlogin.ico --add-data "../lanlogin.ico;." --collect-data sv_ttk --distpath . --workpath build  ../lanlogin.py

REM Clean trash
if exist venv rmdir /s /q venv
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
if exist lanlogin.spec del lanlogin.spec

echo.
echo Build completed.
