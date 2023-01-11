from app import app, models, user_datastore, db, forms
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import and_
from flask_security import login_required, roles_accepted


@app.route('/management', methods=["GET", "POST"])
@login_required
@roles_accepted("manager")
def search_name():
    # all the accounts that come from the search
    accounts = []
    # accounts_of_name = []
    search_form = forms.SearchNameForm()
    type = "none"
    error = False

    if search_form.validate_on_submit():
        first_name = search_form.data["first_name"]
        last_name = search_form.data["last_name"]
        accounts = models.User.query.filter(and_(models.User.first_name == first_name, models.User.last_name == last_name)).all()
        if not accounts:
            error = True
        else:
            error = False

    return render_template('pages/management.html', form=search_form, accounts=accounts, type=type, error=error)


@app.route('/change_permissions', methods=["POST"])
def change_permissions():
    # here I want to take in the form and then use the form to change the account type and then change
    user = models.User.query.filter_by(email=request.form["email"]).first()

    if user.has_role("manager"):
        role = "manager"
    elif user.has_role("staff"):
        role = "staff"
    else:
        role = "customer"

    user_datastore.remove_role_from_user(user, role)
    # change role to manager
    if request.form['type'] == "manager":
        user_datastore.add_role_to_user(user, "manager")
    # change role to staff
    elif request.form['type'] == "staff":
        user_datastore.add_role_to_user(user, "staff")
    # change role to customer
    else:
        user_datastore.add_role_to_user(user, "customer")

    db.session.commit()
    flash("User account role successfully changed.")
    return redirect(url_for('search_name'))
