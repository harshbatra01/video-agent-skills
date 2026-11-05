@echo off
REM Outcome price archive: keep this window open (minimise it). It saves prices every 5 minutes into data\archive.
REM Double-click to start, or put a shortcut to this file in the Startup folder (Win+R, shell:startup) to start it with Windows.
cd /d "%~dp0"
title Outcome price archive
python -u archive.py
pause
