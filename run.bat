@echo off
python build/musica.py
if %errorlevel% neq 0 (
    echo.
    echo Application crashed or failed to start.
    echo Printing requirements just in case:
    type build\packages.txt
    pause
)
