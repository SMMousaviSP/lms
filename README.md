# Learning Management System
This project was developed with flask as the Database and Internet Engineering
final project, because of the limited time and the purpose of this project
which was to work with databases in a website, I did not consider some security
features which should be considered in the production phase.

For running this on your computer first make sure you have `python3.6` or later
, then install `virtualenv` package.
```
pip install virtualenv
```

Create a virtual environment in main directory of the project (same folder as
this file) preferably with a name like `venv`, `env`, `.venv` or `.env` so
`.gitignore` file can ignore it without any modification, I assumed you're
gonna use `.venv`.
```
virtualenv .venv
```

Activate your virtual environment:
```
source .venv/bin/activate
```

Or if you're still using windows:
```
.\venv\Scripts\activate
```

Then install all of the project's dependencies without affecting anything on
your computer.
```
pip install -r requirements.txt
```

You should set 2 environment variable, `FLASK_APP` and `FLASK_DEBUG`,
in GNU/Linux or macOS:
```
export FLASK_APP=main.py
export FLASK_DEBUG=1
```
In windows:
```
set FLASK_APP=main.py
set FLASK_DEBUG=1
```
`FLASK_APP` is the name of the flask app file, and `FLASK_DEBUG` should be 0 or
1, if it's 1 we have access to hot reload and some more features in development
phase.

In the app directory copy `local_settings.py.sample` to `local_settings.py` and
provide required variables for connecting to the database, keep in mind that
for security reasons this file is ignored by `.gitignore`.

In the app directory run the server with this command:
```
flask run
```
