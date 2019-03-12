# Best to do packaging from system python (due to current venv / pyinstaller bug). So lets do that. 
# Generate a requirements.txt from the pipfile.lock
pipenv lock -r > requirements.txt
# Install the requirements in the system python
pip3 install -r requirements.txt
# Run pyinstaller
pyinstaller test.py --onedir --noupx --debug