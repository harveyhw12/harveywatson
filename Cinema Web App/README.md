# Cinema Project

A multipurpose webapp for a cinema chain, aiming to offer functionality for both customers and staff.

# Running
To run the server, move to `/cinema/`, then at the terminal enter:

`./run_cinema.bash`

This bash script establishes the necessary virtual environment and then populates the database with the minimum required data (e.g. mappings of seats to screens and collects some movies).

It checks if the database file exists. If it doesn't, it runs:

1: `source env/bin/activate`

2: `export FLASK_APP=app`

3: `flask populate roles`

4: `flask populate movies`

5: `flask populate screens`

6: `flask run`

If it does already exist the database will have already been properly populated, so it just runs `flask run`.

# Testing
To run the tests, move to `/cinema/`, then at the terminal enter:

1: `source env/bin/activate`

To run the unit tests, run:

- `python test_app.py`

To run the UI tests, run:
- `python ui_test.py`
# Making card transactions
To simulate a purchase with a bank card use the following dummy details:
* Card number - `4242424242424242`
* Expiry date - any date in the future
* CVC code - any three digits

# Populating the database manually
To populate the database with dummy data, run:

1: `./run_cinema.bash`

2: Create at least one user through the website

3: `flask populate showings`

4: `flask populate transactions`

5: `flask populate reservations`

6: `flask populate tickets`


