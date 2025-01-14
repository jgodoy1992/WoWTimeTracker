@echo off
cd /D "%~dp0"
echo Running Virutal environment
call venv\Scripts\activate
echo Running Script
python main.py
pause