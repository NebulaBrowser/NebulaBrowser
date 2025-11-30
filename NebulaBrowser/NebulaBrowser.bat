@echo off
cd /d "%~dp0"

where py >nul 2>&1
if %errorlevel%==0 (
    py NebulaBrowser.py
) else (
    where python >nul 2>&1
    if %errorlevel%==0 (
        python NebulaBrowser.py
    ) else (
        where python3 >nul 2>&1
        if %errorlevel%==0 (
            python3 NebulaBrowser.py
        ) else (
            echo Python was not found. Please install Python and add it to PATH.
            pause
            exit /b 1
        )
    )
)

echo.
echo NebulaBrowser closed.
pause