@echo off
setlocal EnableExtensions
rem ------------------------------------------------------------------
rem convert_aiken_to_gift.bat — run the Python converter in this folder
rem
rem Copyright (C) 2025  Grenoble Ecole de Management &
rem Pierre DAL ZOTTO (aka "DalzAsylum")
rem Licensed under the GPL v3 or later (see <https://www.gnu.org/licenses/>)
rem ------------------------------------------------------------------

set SCRIPT=%~dp0convert_aiken_to_gift.py

where python >nul 2>nul
if %errorlevel%==0 (
  python "%SCRIPT%"
  goto :end
)

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%SCRIPT%"
  goto :end
)

echo [ERROR] Python is not available in PATH. Install it from https://www.python.org/

:end
pause
