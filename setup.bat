python -m venv tldrgpt_env
cmd /k "%~dp0/tldrgpt_env/Scripts/activate & pip install -r requirements.txt & python tldrgpt_flask.py"
