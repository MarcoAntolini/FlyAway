# how to run the app

```bash
# Clone the sources
git clone <https://github.com/MarcoAntolini/Fly-Away>
cd Fly-Away

# Virtualenv modules installation (Unix based systems)
virtualenv venv
source venv/bin/activate

# Virtualenv modules installation (Windows based systems)
# virtualenv venv
# .\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Set the FLASK_APP environment variable
(Unix/Mac) export FLASK_APP=app.py
(Windows) set FLASK_APP=app.py
(Powershell) $env:FLASK_APP = ".\app.py"

# Set up the DEBUG environment
# (Unix/Mac) export FLASK_ENV=development
# (Windows) set FLASK_ENV=development
# (Powershell) $env:FLASK_ENV = "development"

# Run the application
# --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
# --port=5000    - specify the app port (default 5000)  
flask run --host=0.0.0.0 --port=5000

# Access the app in browser: <http://127.0.0.1:5000/>
```
