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
```