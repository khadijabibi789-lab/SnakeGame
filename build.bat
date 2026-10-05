@echo off
echo Building Snake Game executable...
echo.

pyinstaller --noconfirm SnakeGame.spec

echo.
echo ========================================
echo  Executable created in the "dist" folder
echo  File: dist\SnakeGame.exe
echo ========================================
pause
