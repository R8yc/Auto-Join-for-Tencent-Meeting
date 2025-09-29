@echo off
cd /d %~dp0
powershell -NoExit -ExecutionPolicy Bypass -Command "python auto_wemeet.py"
pause