@echo off
pip install -r requirements.txt
cd src
python init_db.py
python main.py 