# Resource List CRUD


## Running service in virtual env

- Pre-requisite:
```
Python 3.9.10
```

- Create a virtual environment to install dependencies and activate it.
```bash
python3 -m venv env
source env/bin/activate
```

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.
```bash
pip install -r requirements.txt
```

- Run this to make sure your database in sync with latest database changes.
```python
python manage.py migrate
```

- Run this to run the server on Port 8000:
```python
python manage.py runserver
```

- The app will be accessible at `localhost:8000`
