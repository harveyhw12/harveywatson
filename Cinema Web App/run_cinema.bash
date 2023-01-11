#!/bin/bash
FILE=app.db
source env/bin/activate
export FLASK_APP=app

if [ -f "$FILE" ]; then
  python setup.py build_sass sdist
  flask run --host 0.0.0.0
else
  flask populate roles
  flask populate movies
  flask populate screens
  python setup.py build_sass sdist
  flask run --host 0.0.0.0
fi
