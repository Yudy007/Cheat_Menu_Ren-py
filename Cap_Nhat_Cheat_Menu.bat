@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Cap_Nhat_Cheat_Menu.ps1" -targetPath "%~1"
if %ERRORLEVEL% neq 0 (
    echo.
    echo Co loi xay ra trong qua trinh dong bo.
)
echo Nhan phim bat ky de thoat...
pause >nul
