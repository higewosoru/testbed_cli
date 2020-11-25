#run the application with the python virtual environment interpreter.

source env/bin/activate
pip3 install -r requirements.txt

cd app/
python3 app.py
cd ..

deactivate
