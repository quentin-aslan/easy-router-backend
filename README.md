# Installation
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Run
### Dev Mode
```bash
. .venv/bin/activate
flask run
```

### Production Mode
```bash
. .venv/bin/activate
gunicorn -w 1 app:app
# EX : Pour lancer sur le port 8081 
gunicorn -w 1 -b :8081 app:app
```