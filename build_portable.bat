@echo off
setlocal
echo ============================================
echo PDF Page Swapper - Portable EXE build
echo Recommended: Python 3.8.10 (64-bit)
echo ============================================
py -3.8 -m pip install --upgrade pip
py -3.8 -m pip install -r requirements.txt
py -3.8 -m PyInstaller --noconfirm --clean --onefile --windowed --name PDF_Page_Swapper --icon=pdf_page_swapper.ico --add-data "pdf_page_swapper.ico;." pdf_page_swapper.py
if errorlevel 1 (
  echo Build failed. Please check the messages above.
  pause
  exit /b 1
)
echo.
echo Portable app created at: dist\PDF_Page_Swapper.exe
pause
