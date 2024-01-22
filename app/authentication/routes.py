
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from forms import UserLoginForm , UserSignupForm
from models import User  # Correct import statement
from flask_login import current_user
from werkzeug.security import check_password_hash
from models import db
from ..api.routes import site


auth = Blueprint("auth", __name__, template_folder="auth_templates")


@auth.route("/", methods=["GET", "POST"])
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserSignupForm()
    if request.method == "POST" and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        print(email, password)

        user = User(first_name, last_name, email, password)

        db.session.add(user)
        db.session.commit()

        print("User added to DB:", user.email)

        flash(f"You have successfully created a user account {email}", "user-created")
        return redirect(url_for("auth.signin")) 
    return render_template("signup.html", form=form)

@auth.route("/signin", methods=["GET", "POST"])
def signin():
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print("Received credentials:", email, password)

        logged_user = User.query.filter(User.email == email).first()
        print("Found user:", logged_user, logged_user.password)
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user, remember=True)
            print("User logged in:", current_user)
            flash("You were successfully logged in", "auth-success")
            return redirect(url_for("site.profile"))  # Check the route name here
        else:
            flash("Your Email/Password is incorrect", "auth-failed")
            print("User not found")
            return redirect(url_for("auth.signin"))
    print("error")

    return render_template("signin.html", form=form)



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", "logout-success")
    return redirect(url_for("auth.signin"))