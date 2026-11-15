@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
set CODE=%ERRORLEVEL%
echo.
pause
exit /b %CODE%
