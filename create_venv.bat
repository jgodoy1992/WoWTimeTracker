@echo off
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created.
call venv\Scripts\activate
echo Virtual environment activated.
echo Installing dependencies...
pip install -r requirements.txt
pause