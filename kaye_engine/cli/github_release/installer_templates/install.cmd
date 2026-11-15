@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0place-payload-into-claude-folder.ps1"
set CODE=%ERRORLEVEL%
echo.
pause
exit /b %CODE%
