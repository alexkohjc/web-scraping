@echo off
echo ============================================================
echo Carousell Scraper Launcher
echo ============================================================
echo.
echo Starting the scraper...
echo This may take 30-60 seconds on first run.
echo.

cd /d "%~dp0dist"
CarousellScraper.exe

echo.
echo ============================================================
echo.
if %ERRORLEVEL% NEQ 0 (
    echo Application exited with an error!
    echo Error code: %ERRORLEVEL%
    echo.
)
echo Press any key to close this window...
pause >nul
