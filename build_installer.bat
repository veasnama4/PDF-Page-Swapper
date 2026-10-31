@echo off
setlocal
call build_portable.bat
if errorlevel 1 exit /b 1
where ISCC >nul 2>nul
if errorlevel 1 (
  echo Inno Setup compiler (ISCC.exe) was not found.
  echo Install Inno Setup, then run this file again.
  pause
  exit /b 1
)
ISCC installer.iss
if errorlevel 1 (
  echo Installer build failed.
  pause
  exit /b 1
)
echo.
echo Installer created in the Output folder.
pause
