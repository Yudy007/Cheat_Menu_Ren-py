@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Update_Cheat_Menu.ps1" -targetPath "%~1"
if %ERRORLEVEL% neq 0 (
    echo.
    echo An error occurred during synchronization.
)
echo Press any key to exit...
pause >nul
