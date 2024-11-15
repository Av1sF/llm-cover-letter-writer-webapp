""" imports """
from flask import (
    Blueprint, 
    request, 
    render_template, 
    make_response, 
    redirect)
from models.user import Users
from database.db import db 
from setup import password_hash
from flask_jwt_extended import (
    create_access_token, 
    set_access_cookies, 
    unset_jwt_cookies
    )
import re 

# initate blueprint 
authRoute = Blueprint('user_authentication', __name__, url_prefix="/auth")

""" serve login template """
@authRoute.route('/login', methods=['GET'])
def getLogin():
    response = render_template('auth/login.html')
    return response

""" serve register user template """
@authRoute.route('/register', methods=['GET'])
def getRegisted():
    response = render_template('auth/register.html')
    return response


""" create user Crud """
@authRoute.route('/register', methods=['POST'])
def createUser():
    msg = "" 
    code = 200 

    try:
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
    except:
        # error if wrong cURL request
        msg="Form read error."
        code = 400

    # check if another user with the same email exists and/or username is in our db 
    userExist = Users.query.filter_by(email=email).first()
    usernameExist = Users.query.filter_by(username=username).first()

    if userExist or usernameExist:
        msg = "Email already in use" if not userExist else "Username already in use"
        code = 400
    elif not re.match(r"^\S+@\S+\.\S+$", email):
        msg = "Please enter a valid email"
        code = 400
    elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        # regex is for a password that has lower and uppercase letters, special characters, numbers, and atleast a length of 8
        msg = "Please enter a valid password"
        code = 400
    else:
        # add new user 
        try: 
            newUser = Users(email=email, password=password_hash.getPasswordHash(password), username=username)
            db.session.add(newUser)
            db.session.commit() 
        except: 
            msg = "Unable to create user"
            code = 500
        
        msg = "Created user successfully"
        code = 200

    return render_template('auth/register.html', msg=msg), code


""" Log in user """
@authRoute.route('/login', methods=['POST'])
def createLoginToken(): 
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        # error incase of wrong cURL request 
        return render_template('auth/login.html', msg="Form read error."), 400

    # check if user is registered 
    userExist = Users.query.filter_by(username=username).first()

    if not userExist or not password_hash.verifyPassword(password, userExist.password):
        return render_template('auth/login.html', msg="Username or password is not correct"), 401
    else:
        try:
            # user is logged in and an access token is created, stored as a cookie 
            response = make_response(redirect('/user/protected'))
            access_token = create_access_token(identity=userExist.id)
            set_access_cookies(response, access_token)
            return response, 200
        except Exception as e:
            return render_template('auth/login.html', msg="Server error."), 500

# Logout 
@authRoute.route("/logout", methods=['POST'])
def unsetTokenLogout():
    response = make_response(redirect('/'))
    unset_jwt_cookies(response)
    return response

