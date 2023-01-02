#!/bin/bash
echo Script starting!
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
"env/bin/python3" -m pip install --upgrade pip
pip3 install wheel
pip3 install -r requirements.txt
clear
echo Done!
echo Run "python3 extracter.py" on terminal to start the extraction script