@echo off
setlocal
cd /d "%~dp0"

set "MSG=%~1"
if "%MSG%"=="" set "MSG=Update site content and templates"

python scripts\deploy.py "%MSG%"
endlocal
