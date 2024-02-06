
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from forms import UserLoginForm , UserSignupForm
from models import User  # Correct import statement
from flask_login import current_user
from werkzeug.security import check_password_hash
from models import db
from ..api.routes import site


auth_blueprint = Blueprint("auth", __name__, template_folder="auth_templates")



@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    password = data.get("password")

    if not all([firstName, lastName, email, password]):
        return jsonify({"message": "Missing fields"}), 400

    user_exists = User.query.filter_by(email=email).first() is not None
    if user_exists:
        return jsonify({"message": "Email already registered"}), 409

  
    user = User(first_name=firstName, last_name=lastName, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": f"User account {email} created successfully"}), 201


@auth_blueprint.route("/signin", methods=["POST"])
def signin():
    
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    print("Received credentials:", email, password)

    # Authenticate the user
    logged_user = User.query.filter_by(email=email).first()
    if logged_user and check_password_hash(logged_user.password, password):
        # Create JWT token
        expires = datetime.timedelta(days=7)  # Token expires in one week
        access_token = create_access_token(identity=email, expires_delta=expires)
        
        print("User logged in:", logged_user.email)
        return jsonify({"access_token": access_token, "message": "Login successful"}), 200
    else:
        print("Authentication failed")
        return jsonify({"message": "Email or Password is incorrect"}), 401




