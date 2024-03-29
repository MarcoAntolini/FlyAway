# Instructions for running the application

## Clone the repository

```bash
$: git clone https://github.com/MarcoAntolini/Fly-Away
$: cd Fly-Away
```

## Virtual environment modules installation

```bash
# Unix based systems
$: virtualenv venv
$: source venv/bin/activate

# Windows based systems
$: virtualenv venv
$: .\venv\Scripts\Activate.ps1
```

## Install requirements

```bash
$: pip install -r requirements.txt
```

## Set the FLASK_APP environment variable

```bash
(Unix/Mac)   $: export FLASK_APP=main.py
(Windows)    $: set FLASK_APP=main.py
(Powershell) $: $env:FLASK_APP = ".\main.py"
```

## Set up the DEBUG environment

```bash
(Unix/Mac)   $: export FLASK_DEBUG=True
(Windows)    $: set FLASK_DEBUG=True
(Powershell) $: $env:FLASK_DEBUG = "True"
```

## Run the application

```bash
$: flask run --host=0.0.0.0 --port=5000
```

- --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)

- --port=5000    - specify the app port (default 5000)

Access the app in the browser at <http://127.0.0.1:5000/> or <http://localhost:5000/>
